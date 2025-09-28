#!/usr/bin/env python3
"""Quick setup script to initialize project structure"""
import os
from pathlib import Path

def setup_project():
    """Create all necessary directories and init files"""
    
    # Define directory structure
    dirs = [
        "data/icici",
        "data/sbi",
        "custom_parsers",
        "utils",
        "tests"
    ]
    
    # Create directories
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}/")
    
    # Create __init__.py files
    init_files = [
        "custom_parsers/__init__.py",
        "utils/__init__.py", 
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"✓ Created {init_file}")
    
    # Create placeholder for data files
    data_note = """Place your bank statement files here:
- icici_sample.pdf: The bank statement PDF
- result.csv: Expected output CSV with columns: Date, Description, Debit, Credit, Balance
"""
    
    for bank in ["icici", "sbi"]:
        readme_path = Path(f"data/{bank}/README.txt")
        readme_path.write_text(data_note)
        print(f"✓ Created data/{bank}/README.txt")
    
    print("\n✅ Project structure initialized!")
    print("\nNext steps:")
    print("1. Copy your ICICI PDF to: data/icici/icici_sample.pdf")
    print("2. Copy your expected CSV to: data/icici/result.csv")
    print("3. Run: python agent.py --target icici")

if __name__ == "__main__":
    setup_project()