import mysql.connector
from mysql.connector import Error
import yaml

# Load DB config from YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=config["mysql"]["host"],
            user=config["mysql"]["user"],
            password=config["mysql"]["password"],
            database=config["mysql"]["database"],
        )
        print("Successfully connected to MySQL database")
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
    
if __name__ == "__main__":
    conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"✅ Connected to database: {db_name[0]}")
    except Error as e:
        print(f"❌ Query failed: {e}")
    finally:
        cursor.close()
        conn.close()
