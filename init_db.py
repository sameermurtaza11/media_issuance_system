import mysql.connector

try:
    # Step 1: Connect to MySQL without selecting a database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''  # XAMPP default, change if needed
    )
    cursor = conn.cursor()

    # Step 2: Check if database exists
    cursor.execute("SHOW DATABASES LIKE 'media_issuance'")
    db_exists = cursor.fetchone()

    # Step 3: If DB does not exist, create it and create the table
    if not db_exists:
        print("[DB] Creating 'media_issuance' database...")
        cursor.execute("CREATE DATABASE media_issuance")
        conn.database = 'media_issuance' # type: ignore

        print("[DB] Creating 'media_issuance_records' table...")
        cursor.execute("""
            CREATE TABLE media_issuance_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                media_type VARCHAR(10) NOT NULL,
                media_id VARCHAR(50) NOT NULL,
                recipient_name VARCHAR(100) NOT NULL,
                recipient_pin VARCHAR(20) NOT NULL,
                issue_date DATE NOT NULL,
                issued_by_name VARCHAR(100) NOT NULL,
                issued_by_pin VARCHAR(20) NOT NULL,
                media_category VARCHAR(5) NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[DB] Database and table created successfully.")
    else:
        print("[DB] Database already exists.")
        # Switch to the database to ensure app.py runs smoothly
        conn.database = 'media_issuance' # type: ignore

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"[ERROR] MySQL Error: {err}")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
