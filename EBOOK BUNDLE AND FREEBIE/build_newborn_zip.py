"""Bundle the 2 newborn PDFs into one ZIP for the $9 Newborn Sleep Starter Kit product."""
import os
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ZIP_OUT = os.path.join(SCRIPT_DIR, "Newborn_Sleep_Starter_Kit.zip")

# Map: source file → name inside the ZIP (clean name for buyer)
FILES = {
    "NewMum_BabySleep_StarterKit.pdf":
        "01 - Newborn Sleep Starter Guide.pdf",
    "newborn_awake_window_tracker.pdf":
        "02 - Newborn Awake Window Tracker.pdf",
}

def main():
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for src, dest_name in FILES.items():
            src_path = os.path.join(SCRIPT_DIR, src)
            if not os.path.exists(src_path):
                print(f"  ⚠ Missing: {src}")
                continue
            z.write(src_path, dest_name)
            print(f"  ✓ Added: {dest_name}")
    size_kb = os.path.getsize(ZIP_OUT) / 1024
    print()
    print(f"  ✅ Created: {ZIP_OUT}")
    print(f"  📦 {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
