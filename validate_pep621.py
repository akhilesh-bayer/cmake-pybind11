#!/usr/bin/env python3
"""
Validation script to check PEP 621 compliance and project setup.

This script validates that the project follows PEP 621 standards and
that all required files are in place.
"""

import os
import sys

# Try to import TOML parser
tomllib = None
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        pass

if tomllib is None:
    print("Warning: Cannot parse TOML files (tomli/tomllib not available)")


def check_pep621_compliance():
    """Check if the project follows PEP 621 standards."""
    print("🔍 Checking PEP 621 compliance...")
    
    issues = []
    
    # Check for required files
    required_files = ['pyproject.toml', 'setup.py', 'README.md', 'LICENSE']
    for file in required_files:
        if not os.path.exists(file):
            issues.append(f"Missing required file: {file}")
        else:
            print(f"✓ Found {file}")
    
    # Check pyproject.toml structure
    if os.path.exists('pyproject.toml') and tomllib:
        try:
            with open('pyproject.toml', 'rb') as f:
                data = tomllib.load(f)
            
            # Check required sections
            required_sections = ['build-system', 'project']
            for section in required_sections:
                if section not in data:
                    issues.append(f"Missing required section in pyproject.toml: [{section}]")
                else:
                    print(f"✓ Found [{section}] section in pyproject.toml")
            
            # Check project metadata
            if 'project' in data:
                project = data['project']
                required_fields = ['name', 'version', 'description']
                for field in required_fields:
                    if field not in project:
                        issues.append(f"Missing required field in [project]: {field}")
                    else:
                        print(f"✓ Found project.{field}: {project[field]}")
                        
                # Check if name matches expected
                if project.get('name') != 'cmakepybind11':
                    issues.append(f"Project name should be 'cmakepybind11', got '{project.get('name')}'")
                        
            # Check build-system
            if 'build-system' in data:
                build_system = data['build-system']
                if 'requires' not in build_system:
                    issues.append("Missing 'requires' in [build-system]")
                if 'build-backend' not in build_system:
                    issues.append("Missing 'build-backend' in [build-system]")
                if build_system.get('build-backend') != 'setuptools.build_meta':
                    issues.append("build-backend should be 'setuptools.build_meta'")
                    
        except Exception as e:
            issues.append(f"Error parsing pyproject.toml: {e}")
    
    # Check setup.py
    if os.path.exists('setup.py'):
        with open('setup.py', 'r', encoding='utf-8') as f:
            setup_content = f.read()
            if 'BinaryDistribution' not in setup_content:
                issues.append("setup.py should define BinaryDistribution class for native extensions")
            if 'InstallPlatlib' not in setup_content:
                issues.append("setup.py should define InstallPlatlib class for proper installation")
    
    return issues


def main():
    """Main validation function."""
    print("🚀 PEP 621 Compliance Validation")
    print("=" * 40)
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    issues = check_pep621_compliance()
    
    print("\n📊 Validation Results")
    print("=" * 20)
    
    if not issues:
        print("🎉 All checks passed! Project is PEP 621 compliant.")
        return 0
    else:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  • {issue}")
        return 1


if __name__ == "__main__":
    exit(main())
