#!/usr/bin/env python
"""
Voice Input Feature - Deployment Checklist Script
Run this script to verify all components before deployment
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description=""):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    desc_text = f" ({description})" if description else ""
    print(f"{status} {filepath}{desc_text}")
    return exists


def check_django_app():
    """Verify Django app structure"""
    print("\n🔍 Checking Django App Structure...")
    print("─" * 50)
    
    checks = {
        'voice_feature/__init__.py': 'Module init',
        'voice_feature/apps.py': 'App config',
        'voice_feature/models.py': 'Database models',
        'voice_feature/views.py': 'API views',
        'voice_feature/urls.py': 'URL routing',
        'voice_feature/admin.py': 'Admin interface',
        'voice_feature/tests.py': 'Test suite',
        'voice_feature/migrations/__init__.py': 'Migrations init',
        'voice_feature/migrations/0001_initial.py': 'Initial migration',
    }
    
    all_good = True
    for filepath, desc in checks.items():
        if not check_file_exists(filepath, desc):
            all_good = False
    
    return all_good


def check_static_files():
    """Verify static files"""
    print("\n🔍 Checking Static Files...")
    print("─" * 50)
    
    all_good = check_file_exists('static/js/voice-input.js', 'Voice manager')
    return all_good


def check_templates():
    """Verify template files"""
    print("\n🔍 Checking Template Files...")
    print("─" * 50)
    
    checks = {
        'templates/partials/voice_input_component.html': 'Voice component',
        'templates/expenses/add_expense.html': 'Expense form',
    }
    
    all_good = True
    for filepath, desc in checks.items():
        if not check_file_exists(filepath, desc):
            all_good = False
    
    return all_good


def check_migrations():
    """Verify migration files"""
    print("\n🔍 Checking Migrations...")
    print("─" * 50)
    
    checks = {
        'voice_feature/migrations/0001_initial.py': 'Voice feature migration',
        'expenses/migrations/0003_expense_created_from.py': 'Expense model migration',
    }
    
    all_good = True
    for filepath, desc in checks.items():
        if not check_file_exists(filepath, desc):
            all_good = False
    
    return all_good


def check_documentation():
    """Verify documentation files"""
    print("\n🔍 Checking Documentation...")
    print("─" * 50)
    
    checks = {
        'VOICE_FEATURE_README.md': 'Feature documentation',
        'VOICE_SETUP_GUIDE.md': 'Setup instructions',
        'VOICE_QUICK_REFERENCE.md': 'Quick reference',
        'VOICE_FEATURE_IMPLEMENTATION_SUMMARY.md': 'Implementation summary',
        'VOICE_FEATURE_VERIFICATION.md': 'Verification report',
        'FYP_Documentation_COMPLETE_WITH_SCREENSHOTS.docx': 'FYP Word document',
    }
    
    all_good = True
    for filepath, desc in checks.items():
        if not check_file_exists(filepath, desc):
            all_good = False
    
    return all_good


def check_settings_config():
    """Check if voice_feature is in settings"""
    print("\n🔍 Checking Settings Configuration...")
    print("─" * 50)
    
    with open('expensetracker/settings.py', 'r') as f:
        content = f.read()
        
    if 'voice_feature' in content:
        print("✅ 'voice_feature' found in INSTALLED_APPS")
        return True
    else:
        print("❌ 'voice_feature' NOT found in INSTALLED_APPS")
        return False


def check_urls_config():
    """Check if voice URLs are configured"""
    print("\n🔍 Checking URLs Configuration...")
    print("─" * 50)
    
    with open('expensetracker/urls.py', 'r') as f:
        content = f.read()
        
    if 'voice_feature' in content and "include('voice_feature.urls')" in content:
        print("✅ Voice URLs configured in expensetracker/urls.py")
        return True
    else:
        print("❌ Voice URLs NOT properly configured")
        return False


def check_model_fields():
    """Check if Expense model has created_from field"""
    print("\n🔍 Checking Model Fields...")
    print("─" * 50)
    
    with open('expenses/models.py', 'r') as f:
        content = f.read()
        
    if 'created_from' in content:
        print("✅ 'created_from' field found in Expense model")
        return True
    else:
        print("❌ 'created_from' field NOT found in Expense model")
        return False


def print_deployment_checklist():
    """Print deployment checklist"""
    print("\n" + "=" * 60)
    print("  DEPLOYMENT CHECKLIST")
    print("=" * 60)
    
    checklist = [
        ("Run migrations", "python manage.py migrate"),
        ("Collect static files", "python manage.py collectstatic --noinput"),
        ("Run tests", "python manage.py test voice_feature"),
        ("Check admin panel", "Visit /admin/voice_feature/"),
        ("Test voice feature", "Go to /expenses/add-expenses/"),
        ("Verify database", "Check voice_feature_voiceinputlog table"),
        ("Review logs", "Check for any errors in Django logs"),
        ("Backup database", "Create database backup"),
    ]
    
    for i, (task, command) in enumerate(checklist, 1):
        print(f"\n{i}. {task}")
        print(f"   Command: {command}")


def print_post_deployment_verification():
    """Print post-deployment verification steps"""
    print("\n" + "=" * 60)
    print("  POST-DEPLOYMENT VERIFICATION")
    print("=" * 60)
    
    verification = [
        "1. Test voice input button appears on Add Expense page",
        "2. Microphone permission request shows in browser",
        "3. Speak '500 coffee' and verify form auto-fills",
        "4. Submit expense and verify it appears in list",
        "5. Check Django admin to see VoiceInputLog entry",
        "6. Verify no JavaScript console errors",
        "7. Test on Chrome, Firefox, and Edge",
        "8. Monitor server logs for any errors",
    ]
    
    for step in verification:
        print(f"\n✓ {step}")


def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("  VOICE FEATURE DEPLOYMENT VERIFICATION")
    print("=" * 60)
    print(f"\nTime: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {os.getcwd()}")
    
    all_checks_passed = True
    
    # Run all checks
    all_checks_passed &= check_django_app()
    all_checks_passed &= check_static_files()
    all_checks_passed &= check_templates()
    all_checks_passed &= check_migrations()
    all_checks_passed &= check_documentation()
    all_checks_passed &= check_settings_config()
    all_checks_passed &= check_urls_config()
    all_checks_passed &= check_model_fields()
    
    # Print results
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT")
    else:
        print("❌ SOME CHECKS FAILED - REVIEW REQUIRED")
    print("=" * 60)
    
    # Print deployment instructions
    print_deployment_checklist()
    print_post_deployment_verification()
    
    # Summary
    print("\n" + "=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print("""
1. Review VOICE_SETUP_GUIDE.md for detailed instructions
2. Run: python manage.py migrate
3. Run: python manage.py test voice_feature
4. Start server: python manage.py runserver
5. Test voice feature in browser
6. Check admin panel for voice logs
7. Review VOICE_QUICK_REFERENCE.md for user guide
8. Deploy to production when ready
    """)
    
    return 0 if all_checks_passed else 1


if __name__ == '__main__':
    sys.exit(main())
