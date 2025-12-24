import zipfile
import os
import sys

ZIP_FILE = "combined.zip"   # 🔄 changed
EXTRACT_DIR = "main"

password = os.environ.get("ZIP_PASSWORD")

if not password:
    print("❌ ZIP_PASSWORD is missing in GitHub Secrets!")
    sys.exit(1)

print("🔐 Trying to unlock ZIP…")

try:
    with zipfile.ZipFile(ZIP_FILE, 'r') as z:
        z.extractall(EXTRACT_DIR, pwd=password.encode())
    print("✅ ZIP extracted successfully!")
except Exception as e:
    print("❌ Failed to extract ZIP:", e)
    sys.exit(1)
