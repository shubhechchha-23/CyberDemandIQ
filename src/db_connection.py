import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "cyberdemandiq",
    "user": "postgres",
    "password": "your_postgresql_password"
}


def test_connection():

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        cursor = connection.cursor()

        cursor.execute("""
            SELECT current_database(), current_user;
        """)

        result = cursor.fetchone()

        print("=" * 60)
        print("CYBERDEMANDEIQ DATABASE CONNECTION")
        print("=" * 60)

        print(f"Database : {result[0]}")
        print(f"User     : {result[1]}")

        cursor.close()
        connection.close()

        print("\nPostgreSQL connection successful!")

    except Exception as error:

        print("\nDatabase connection failed.")
        print("Error:", error)


if __name__ == "__main__":
    test_connection()