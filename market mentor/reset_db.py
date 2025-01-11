from market_mentor import db  # Replace `your_app_file` with the actual filename where `db` is defined

# Drop all existing tables
db.drop_all()

# Create all tables with the updated schema
db.create_all()

print("Database schema has been reset.")
