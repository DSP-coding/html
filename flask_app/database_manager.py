import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, db_config):
        # The constructor accepts the database configuration and stores it in the object
        self.db_config = db_config

    def get_db_connection(self):
        """Create a new database connection."""
        # This method tries to connect to the MySQL database using the config provided
        try:
            connection = mysql.connector.connect(**self.db_config)
            print("Database connection established.")  # Print message if connection is successful
            return connection
        except Error as err:
            # If something goes wrong with the connection, it prints an error message
            print(f"Error connecting to database: {err}")
            return None  # Returns None if connection fails

    def save_score(self, username, score):
        """Save the user's score to the database."""
        conn = None
        try:
            # First, it tries to get a connection to the database
            conn = self.get_db_connection()
            if conn is None:
                raise Exception("Database connection failed.")  # If connection fails, raise an error

            # If connection is successful, insert the username and score into the 'scores' table
            cursor = conn.cursor()
            cursor.execute('INSERT INTO scores (username, score) VALUES (%s, %s)', (username, score))
            conn.commit()  # Commit the changes to the database
            print(f"Score for {username} saved successfully: {score}")  # Debug line to confirm save
        except mysql.connector.Error as err:
            # If there’s a database-specific error (like invalid query), print the error
            print(f"Database error: {err}")
        except Exception as e:
            # Catch any other type of error and print it
            print(f"An error occurred: {e}")
        finally:
            # Close the database connection once the operation is complete
            if conn:
                conn.close()
