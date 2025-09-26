from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

def create_connection(db_name, db_user, db_password, db_host='localhost', db_port=5432):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL established successfully")
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print(f"Query executed successfully, {cursor.rowcount} rows affected")
        return cursor.rowcount
    except Exception as e:
        connection.rollback()
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()


def execute_read_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        # connection.commit()
        rows = cursor.fetchall()
        print(f"Read Query executed successfully, {cursor.rowcount} rows fetched")
        return rows
    except Exception as e:
        # connection.rollback()
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

if __name__ == "__main__":
    # Load environment variables
    DB_NAME     = os.getenv("Postgres_db")      # e.g., TestDB
    DB_USER     = os.getenv("Postgres_user") or "acro0"
    DB_PASSWORD = os.getenv("Postgres_passwd")
    DB_HOST     = 'localhost'    # default to localhost
    DB_PORT     = int(os.getenv("Postgres_port") or 5432)

    conn = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    if not conn:
        exit(1)
    # Create the employees table if it doesn't exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS public.employees (
        id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hire_date DATE NOT NULL
    );
    """
    execute_query(conn, create_table_sql)

    # Insert sample rows
    insert_sql = """
    INSERT INTO public.employees (first_name, last_name, email, hire_date) VALUES
  ('Daniel', 'Anderson', 'daniel.anderson@example.com', '2023-11-25'),
  ('Olivia', 'Martinez', 'olivia.martinez@example.com', '2023-12-05'),
  ('James', 'Rodriguez', 'james.rodriguez@example.com', '2024-01-10'),
  ('Sophia', 'Garcia', 'sophia.garcia@example.com', '2024-02-15'),
  ('Matthew', 'Lee', 'matthew.lee@example.com', '2024-03-20')
ON CONFLICT (email) DO NOTHING;
    """
    read_sql = """
    SELECT * FROM public.Employees;
    """
    # affected = execute_query(conn, insert_sql)
    affected = execute_read_query(conn,read_sql)
    if affected is not None:
        print("Operation success \n",affected)
    else:
        print("operation failed")
    conn.close()
    print("PostgreSQL connection closed")