#!/usr/bin/env python3
"""
Healthcheck script to verify Railway deployment
Run before starting the app to catch configuration errors early
"""
import os
import sys

def check_env_vars():
    """Check that all required environment variables are set"""
    required_vars = [
        'DATABASE_URL',
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'SUPABASE_JWT_SECRET',
        'SECRET_KEY',
    ]

    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            # Print first/last 10 chars for debugging (hide middle)
            if len(value) > 20:
                masked = f"{value[:10]}...{value[-10:]}"
            else:
                masked = value[:5] + "***"
            print(f"✓ {var}: {masked}")

    if missing:
        print("\n❌ Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        sys.exit(1)

    print("\n✅ All required environment variables are set")

def check_database_url():
    """Verify DATABASE_URL is valid"""
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        if not db_url.startswith('postgresql://'):
            print(f"⚠️  DATABASE_URL should start with 'postgresql://', got: {db_url[:20]}...")
            return False
        print(f"✓ DATABASE_URL format looks valid")
    return True

def main():
    print("=" * 50)
    print("Railway Deployment Health Check")
    print("=" * 50)
    print()

    check_env_vars()
    check_database_url()

    print()
    print("=" * 50)
    print("Ready to start application!")
    print("=" * 50)

if __name__ == "__main__":
    main()
