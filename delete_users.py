from app import app
from auth.models import User
from auth import db
import sys

def delete_all_users():
    with app.app_context():
        try:
            # Get count before deletion
            count = User.query.count()
            if count == 0:
                print("No users found in database")
                return
            
            # Confirm deletion
            print(f"WARNING: This will delete ALL {count} users from the database")
            confirmation = input("Type 'DELETE' to confirm: ")
            if confirmation != 'DELETE':
                print("Aborted - no users were deleted")
                return
            
            # Perform deletion
            User.query.delete()
            db.session.commit()
            print(f"Successfully deleted {count} users")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting users: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    delete_all_users()
