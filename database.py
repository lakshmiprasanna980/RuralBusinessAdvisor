import mysql.connector


# ==========================================
# MYSQL CONNECTION
# ==========================================

def get_connection():

    print("Connecting to MySQL server...")

    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="rural_business_advisor",
            connection_timeout=5,
            use_pure=True
        )

        print("MySQL connection successful!")

        return connection

    except Exception as e:

        print("MYSQL ERROR:")
        print(type(e).__name__)
        print(str(e))

        return None
# ==========================================
# SAVE ENTREPRENEUR
# ==========================================

def save_entrepreneur(
    name,
    village,
    district,
    state,
    business,
    investment,
    experience,
    goal
):

    print("1. save_entrepreneur() started")

    connection = None
    cursor = None

    try:

        print("2. Connecting to MySQL...")

        connection = get_connection()

        if connection is None:
            print("ERROR: MySQL connection is None")
            return None

        print("3. MySQL connected")

        cursor = connection.cursor()

        print("4. Cursor created")

        query = """
        INSERT INTO entrepreneurs
        (
            name,
            village,
            district,
            state,
            business,
            investment,
            experience,
            goal
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        values = (
            name,
            village,
            district,
            state,
            business,
            investment,
            experience,
            goal
        )

        print("5. Executing INSERT...")

        cursor.execute(query, values)

        print("6. INSERT executed")

        connection.commit()

        print("7. Data committed")

        entrepreneur_id = cursor.lastrowid

        print(
            "8. Entrepreneur ID:",
            entrepreneur_id
        )

        return entrepreneur_id

    except Exception as e:

        print("ERROR INSIDE save_entrepreneur():")
        print(type(e).__name__)
        print(str(e))

        if connection:
            connection.rollback()

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        print("9. Database connection closed")