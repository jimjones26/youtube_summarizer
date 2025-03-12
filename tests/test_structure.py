import os
from pathlib import Path

def test_project_directory_structure_exists():
    """Test that required directories and files exist"""
    # Verify directories
    assert Path("src").is_dir(), "'src' directory not found"
    assert Path("tests").is_dir(), "'tests' directory not found" 
    assert Path("data").is_dir(), "'data' directory not found"
    
    # Verify main entry point
    assert Path("src/main.py").is_file(), "'src/main.py' file not found"
