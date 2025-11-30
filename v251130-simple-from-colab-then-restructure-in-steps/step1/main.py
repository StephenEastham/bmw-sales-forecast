"""Main execution script - Step 1.

This step focuses on setting up the project structure, configuration,
and basic utility functions. We verify that the environment is ready
for future development steps.
"""
import sys
from pathlib import Path

# Import from our new modules
from config import (
    PROJECT_ROOT, OUTPUT_DIR, DATA_CSV_URL, DATA_CSV_FILE
)
from utils import clean_outputs, print_section, zip_all_outputs

def test_infrastructure():
    print_section("STEP 1: INFRASTRUCTURE & CONFIGURATION TEST")
    
    # 1. Verify Configuration
    print(f"✅ Project Root: {PROJECT_ROOT}")
    print(f"✅ Output Directory: {OUTPUT_DIR}")
    print(f"✅ Data URL Configured: {DATA_CSV_URL[:50]}...")
    
    # 2. Verify Utils - Clean
    print("\nTesting clean_outputs()...")
    clean_outputs()
    
    # 3. Verify Utils - File Operations
    print("\nTesting file generation in Output Directory...")
    test_file = OUTPUT_DIR / "test_infrastructure.txt"
    try:
        with open(test_file, "w") as f:
            f.write("This is a test file to verify Step 1 infrastructure.")
        print(f"✅ Created test file: {test_file.name}")
    except Exception as e:
        print(f"❌ Failed to create file: {e}")
        
    # 4. Verify Utils - Zip
    print("\nTesting zip_all_outputs()...")
    try:
        zip_path = zip_all_outputs()
        print(f"✅ Zip archive created successfully at: {zip_path.name}")
    except Exception as e:
        print(f"❌ Failed to zip outputs: {e}")

if __name__ == "__main__":
    test_infrastructure()
    print("\nStep 1 Complete: Infrastructure is ready for Data Module (Step 2).")
