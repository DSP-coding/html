import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_db_connection(self):
        """Create a new database connection."""
        try:
            connection = mysql.connector.connect(**self.db_config)
            print("Database connection established.")
            return connection
        except Error as err:
            print(f"Error connecting to database: {err}")
            return None

    def save_score(self, username, score):
        """Save the user's score to the database."""
        conn = None
        try:
            conn = self.get_db_connection()
            if conn is None:
                raise Exception("Database connection failed.")
                
            cursor = conn.cursor()
            cursor.execute('INSERT INTO scores (username, score) VALUES (%s, %s)', (username, score))
            conn.commit()
            print(f"Score for {username} saved successfully: {score}")  # Debug line
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
