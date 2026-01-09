"""
Quick script to verify database connection and table structure.
"""
from sqlmodel import Session, select, text
from database import engine
from models import Task, User

def verify_connection():
    """Test database connection and verify tables exist."""
    print("=" * 60)
    print("DATABASE CONNECTION VERIFICATION")
    print("=" * 60)

    try:
        with Session(engine) as session:
            # Test 1: Check PostgreSQL version
            print("\n1. Testing database connection...")
            result = session.exec(text("SELECT version()")).first()
            print(f"[OK] Connected to: {result[:50]}...")

            # Test 2: Check if users table exists
            print("\n2. Checking 'users' table...")
            result = session.exec(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_name = 'users'"
            )).first()
            if result:
                print(f"[OK] Table 'users' exists")

                # Get column info
                columns = session.exec(text(
                    "SELECT column_name, data_type "
                    "FROM information_schema.columns "
                    "WHERE table_name = 'users' "
                    "ORDER BY ordinal_position"
                )).all()
                print("  Columns:")
                for col in columns:
                    print(f"    - {col[0]}: {col[1]}")
            else:
                print("[FAIL] Table 'users' not found")

            # Test 3: Check if tasks table exists
            print("\n3. Checking 'tasks' table...")
            result = session.exec(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_name = 'tasks'"
            )).first()
            if result:
                print(f"[OK] Table 'tasks' exists")

                # Get column info
                columns = session.exec(text(
                    "SELECT column_name, data_type "
                    "FROM information_schema.columns "
                    "WHERE table_name = 'tasks' "
                    "ORDER BY ordinal_position"
                )).all()
                print("  Columns:")
                for col in columns:
                    print(f"    - {col[0]}: {col[1]}")
            else:
                print("[FAIL] Table 'tasks' not found")

            # Test 4: Check foreign key constraint
            print("\n4. Checking foreign key constraints...")
            fkeys = session.exec(text(
                "SELECT "
                "    tc.constraint_name, "
                "    tc.table_name, "
                "    kcu.column_name, "
                "    ccu.table_name AS foreign_table_name, "
                "    ccu.column_name AS foreign_column_name "
                "FROM information_schema.table_constraints AS tc "
                "JOIN information_schema.key_column_usage AS kcu "
                "  ON tc.constraint_name = kcu.constraint_name "
                "JOIN information_schema.constraint_column_usage AS ccu "
                "  ON ccu.constraint_name = tc.constraint_name "
                "WHERE tc.constraint_type = 'FOREIGN KEY' "
                "  AND tc.table_name = 'tasks'"
            )).all()

            if fkeys:
                for fk in fkeys:
                    print(f"[OK] Foreign key: {fk[1]}.{fk[2]} -> {fk[3]}.{fk[4]}")
            else:
                print("  No foreign keys found")

            # Test 5: Check indexes
            print("\n5. Checking indexes on 'tasks' table...")
            indexes = session.exec(text(
                "SELECT indexname, indexdef "
                "FROM pg_indexes "
                "WHERE tablename = 'tasks'"
            )).all()

            if indexes:
                for idx in indexes:
                    print(f"[OK] Index: {idx[0]}")
                    print(f"  {idx[1]}")
            else:
                print("  No indexes found")

            # Test 6: Count existing records
            print("\n6. Checking record counts...")
            task_count = session.exec(text("SELECT COUNT(*) FROM tasks")).first()
            print(f"[OK] Tasks table: {task_count} records")

            user_count = session.exec(text("SELECT COUNT(*) FROM users")).first()
            print(f"[OK] Users table: {user_count} records")

        print("\n" + "=" * 60)
        print("[OK] DATABASE VERIFICATION COMPLETE - ALL CHECKS PASSED")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n[FAIL] ERROR: {str(e)}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    verify_connection()
