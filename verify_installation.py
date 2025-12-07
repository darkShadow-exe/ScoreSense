"""
Installation Verification Script
Run this to check if all dependencies are properly installed.
"""

import sys

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_modules():
    """Check if all required modules are installed."""
    print("\nChecking required modules...")
    
    modules = {
        'flask': 'Flask',
        'matplotlib': 'Matplotlib',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn'
    }
    
    all_ok = True
    
    for module_name, display_name in modules.items():
        try:
            __import__(module_name)
            print(f"✓ {display_name} - Installed")
        except ImportError:
            print(f"✗ {display_name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Check if all required files and directories exist."""
    print("\nChecking project structure...")
    
    import os
    
    required_items = [
        ('app.py', 'file'),
        ('requirements.txt', 'file'),
        ('templates', 'dir'),
        ('static', 'dir'),
        ('core', 'dir'),
        ('models', 'dir'),
        ('db', 'dir'),
    ]
    
    all_ok = True
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for item, item_type in required_items:
        path = os.path.join(base_dir, item)
        
        if item_type == 'file':
            exists = os.path.isfile(path)
        else:
            exists = os.path.isdir(path)
        
        if exists:
            print(f"✓ {item} - Found")
        else:
            print(f"✗ {item} - MISSING")
            all_ok = False
    
    return all_ok

def check_templates():
    """Check if all HTML templates exist."""
    print("\nChecking HTML templates...")
    
    import os
    
    templates = [
        'index.html',
        'add_student.html',
        'student_list.html',
        'edit_student.html',
        'stats.html',
        'command.html'
    ]
    
    all_ok = True
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    
    for template in templates:
        path = os.path.join(templates_dir, template)
        if os.path.isfile(path):
            print(f"✓ {template} - Found")
        else:
            print(f"✗ {template} - MISSING")
            all_ok = False
    
    return all_ok

def check_core_modules():
    """Check if all core Python modules exist."""
    print("\nChecking core modules...")
    
    import os
    
    core_modules = [
        'nlu.py',
        'stats.py',
        'graphs.py',
        'predict.py'
    ]
    
    all_ok = True
    base_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.join(base_dir, 'core')
    
    for module in core_modules:
        path = os.path.join(core_dir, module)
        if os.path.isfile(path):
            print(f"✓ {module} - Found")
        else:
            print(f"✗ {module} - MISSING")
            all_ok = False
    
    return all_ok

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("  SCORE ANALYSER - Installation Verification")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Required Modules", check_modules()))
    results.append(("Project Structure", check_project_structure()))
    results.append(("HTML Templates", check_templates()))
    results.append(("Core Modules", check_core_modules()))
    
    print("\n" + "=" * 60)
    print("  VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:<25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYou're ready to run the application:")
        print("  python app.py")
        print("\nOr use the quick start script:")
        print("  run.bat (Windows)")
    else:
        print("\n❌ SOME CHECKS FAILED!")
        print("\nTo fix missing modules, run:")
        print("  pip install -r requirements.txt")
        print("\nIf files are missing, ensure you have all project files.")
    
    print()
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
