#!/usr/bin/env python3
"""
Quick check to see what DATABASE_URL Railway is using
"""
import os
import sys

print("=" * 60)
print("ENVIRONMENT VARIABLE CHECK")
print("=" * 60)

db_url = os.getenv('DATABASE_URL')

if not db_url:
    print("❌ DATABASE_URL is NOT set!")
    sys.exit(1)

print(f"\n✓ DATABASE_URL is set")
print(f"\nFirst 50 chars: {db_url[:50]}")
print(f"Last 30 chars: ...{db_url[-30:]}")

if 'localhost' in db_url:
    print("\n🔴 ERROR: DATABASE_URL contains 'localhost'")
    print("This means .env file is being loaded!")
    sys.exit(1)

if 'railway' in db_url or 'postgres' in db_url:
    print("\n✅ DATABASE_URL looks correct (Railway/Postgres)")
else:
    print("\n⚠️  DATABASE_URL doesn't look like Railway")

print("\nAll environment variables:")
for key in ['DATABASE_URL', 'SUPABASE_URL', 'SECRET_KEY', 'PORT', 'RAILWAY_ENVIRONMENT']:
    value = os.getenv(key)
    if value:
        masked = f"{value[:10]}..." if len(value) > 10 else value
        print(f"  {key}: {masked}")
    else:
        print(f"  {key}: NOT SET")

print("\n" + "=" * 60)
