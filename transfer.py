import sqlite3
from functions.load_variables import Variables
from functions.g_pass import GPass

g_pass = GPass()
variables = Variables()
key = variables.check_key()

def insert_phrases_from_file(filename):
    # Connect to the database
    conn = sqlite3.connect('lockin.db')
    c = conn.cursor()

    try:
        # Read the lines from the file and insert into the phrases table
        with open(filename, 'r') as file:
            phrases = file.readlines()
            for phrase in phrases:
                # Remove leading and trailing whitespaces and insert into the database
                c.execute("INSERT INTO phrases (phrase) VALUES (?)", (g_pass.encrypt(phrase.strip()),))

        # Commit changes
        conn.commit()
        print("Phrases inserted successfully.")
    except FileNotFoundError:
        print("File not found.")

    # Close the database connection
    conn.close()

# Example usage
if __name__ == "__main__":
    filename = 'gang.txt'
    insert_phrases_from_file(filename)
