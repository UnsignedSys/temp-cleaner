import os
import shutil
import ctypes
from tqdm import tqdm
from pathlib import Path

def is_admin():
    """Check if the script is running as admin"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clean_folder(path, name):
    """Delete everything inside the given folder"""
    p = Path(path)
    if not p.exists():
        print(f"{name}: folder not found")
        return
    
    items = list(p.iterdir())
    if not items:
        print(f"{name}: already empty")
        return

    print(f"Cleaning {name}...")

    with tqdm(total=len(items), desc=name, unit="item") as bar:
        for item in items:
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
            except Exception as e:
                # ignoring errors silently
                pass
            bar.update(1)

def main():
    sys_root = os.getenv("SystemRoot", "C:\\Windows")
    temp_path = os.path.join(sys_root, "Temp")
    user_temp = os.getenv("TEMP")
    prefetch_path = os.path.join(sys_root, "Prefetch")

    print("\n--- Temp Cleaner ---\n")

    clean_folder(temp_path, "System Temp")
    clean_folder(user_temp, "User Temp")

    if is_admin():
        clean_folder(prefetch_path, "Prefetch")
    else:
        print("Prefetch skipped (need admin rights).")

    input("\nDone. Press Enter to close...")

if __name__ == "__main__":
    main()
