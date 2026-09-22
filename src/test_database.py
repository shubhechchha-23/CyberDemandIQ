import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config.database import get_connection


print("=" * 60)
print("CYBERDEMANDEIQ - DATABASE INSPECTION")
print("=" * 60)

try:

    connection = get_connection()

    print("\nPostgreSQL connection successful!")

    cursor = connection.cursor()

    # Check current database
    cursor.execute(
        "SELECT current_database();"
    )

    database_name = cursor.fetchone()[0]

    print("\nConnected database:")
    print(database_name)

    # Check tables
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    )

    tables = cursor.fetchall()

    print("\nTables found:")

    for table in tables:
        print(" -", table[0])

    cursor.close()
    connection.close()

    print("\nDatabase connection closed.")

except Exception as e:

    print("\nDatabase inspection failed!")

    print(
        f"Error: {e}"
    )