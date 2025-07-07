#!/usr/bin/env python3
"""
Validation script to check the backend structure and imports.
"""

import os
import sys
import importlib.util
from pathlib import Path


def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)


def check_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def main():
    """Main validation function."""
    backend_dir = Path(__file__).parent

    print("🔍 Validating ShikshaSetu Backend Structure...")
    print("=" * 60)

    # Check required files
    required_files = [
        "main.py",
        "celery_app.py",
        "requirements.txt",
        "app/__init__.py",
        "app/core/__init__.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/core/auth.py",
        "app/core/cache.py",
        "app/core/logging.py",
        "app/models/__init__.py",
        "app/models/models.py",
        "app/models/scholarship.py",
        "app/models/user.py",
        "app/services/__init__.py",
        "app/services/scraping_service.py",
        "app/services/scholarship_service.py",
        "app/services/user_service.py",
        "app/services/application_service.py",
        "app/services/notification_service.py",
        "app/services/validation_service.py",
        "app/services/analytics_service.py",
        "app/services/ai_service.py",
        "app/tasks/__init__.py",
        "app/tasks/scraping_tasks.py",
        "app/tasks/validation_tasks.py",
        "app/tasks/notification_tasks.py",
        "app/utils/__init__.py",
        "app/utils/text_processing.py",
        "app/utils/date_parser.py",
        "app/utils/amount_parser.py",
        "app/utils/link_validator.py",
        "app/utils/deduplication.py",
        "app/schemas.py",
    ]

    print("📁 Checking required files...")
    missing_files = []
    syntax_errors = []

    for file_path in required_files:
        full_path = backend_dir / file_path

        if not check_file_exists(full_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")

            # Check syntax for Python files
            if file_path.endswith('.py'):
                is_valid, error = check_python_syntax(full_path)
                if not is_valid:
                    syntax_errors.append((file_path, error))
                    print(f"⚠️  Syntax error in {file_path}: {error}")

    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    total_files = len(required_files)
    found_files = total_files - len(missing_files)

    print(f"📁 Files: {found_files}/{total_files} found")
    print(f"❌ Missing: {len(missing_files)} files")
    print(f"⚠️  Syntax errors: {len(syntax_errors)} files")

    if missing_files:
        print("\n📋 Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")

    if syntax_errors:
        print("\n🐛 Syntax errors:")
        for file_path, error in syntax_errors:
            print(f"  - {file_path}: {error}")

    # Check Docker files
    print("\n🐳 Checking Docker files...")
    docker_files = ["Dockerfile", "../Dockerfile", "../docker-compose.yml"]

    for file_path in docker_files:
        full_path = backend_dir / file_path
        if check_file_exists(full_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")

    # Check environment files
    print("\n🔧 Checking environment files...")
    env_files = ["../.env", "../.env.example"]

    for file_path in env_files:
        full_path = backend_dir / file_path
        if check_file_exists(full_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")

    # Final status
    print("\n" + "=" * 60)

    if not missing_files and not syntax_errors:
        print("🎉 VALIDATION PASSED! All required files are present and valid.")
        print("✨ The backend structure is ready for development.")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up environment variables (.env file)")
        print("3. Run database migrations")
        print("4. Start the development server")
        return 0
    else:
        print("❌ VALIDATION FAILED! Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("1. Create missing files")
        print("2. Fix syntax errors")
        print("3. Check import statements")
        print("4. Verify file permissions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
