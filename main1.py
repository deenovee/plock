import csv
import sqlite3
from password_manager_app import PasswordManagerApp

conn = sqlite3.connect('lockin.db')
c = conn.cursor()

# Create passwords table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords (acct text, email text, p text, update_timestamp text)''')

# Check for phrases table existence and create if not exist
c.execute('''CREATE TABLE IF NOT EXISTS phrases (id INTEGER PRIMARY KEY AUTOINCREMENT, phrase text)''')

# Check for pins table existence and create if not exist
c.execute('''CREATE TABLE IF NOT EXISTS pins (id INTEGER PRIMARY KEY AUTOINCREMENT, pin text)''')

conn.commit()
conn.close()

# Function to retrieve phrases from the database
def retrieve_phrases():
    conn = sqlite3.connect('lockin.db')
    c = conn.cursor()
    c.execute("SELECT phrase FROM phrases")
    phrases = [row[0] for row in c.fetchall()]
    conn.close()
    return phrases

# Function to retrieve pins from the database
def retrieve_pins():
    conn = sqlite3.connect('lockin.db')
    c = conn.cursor()
    c.execute("SELECT pin FROM pins")
    pins = [row[0] for row in c.fetchall()]
    conn.close()
    return pins

# Function to prompt user to enter phrases from a CSV file
def enter_phrases_from_csv():
    path = input("Enter the path to the CSV file containing phrases: ")
    phrases = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            phrases.extend(row)
    
    # Save each phrase to the database
    conn = sqlite3.connect('lockin.db')
    c = conn.cursor()
    for phrase in phrases:
        c.execute("INSERT INTO phrases (phrase) VALUES (?)", (phrase,))
    conn.commit()
    conn.close()

# Function to prompt user to enter pins from a CSV file
def enter_pins_from_csv():
    path = input("Enter the path to the CSV file containing pins: ")
    pins = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            pins.extend(row)
    
    # Save each pin to the database
    conn = sqlite3.connect('lockin.db')
    c = conn.cursor()
    for pin in pins:
        c.execute("INSERT INTO pins (pin) VALUES (?)", (pin,))
    conn.commit()
    conn.close()

# Check if phrases list is empty, if so prompt user to enter phrases from CSV
phrases = retrieve_phrases()
if not phrases:
    enter_phrases_from_csv()

# Check if pins list is empty, if so prompt user to enter pins from CSV
pins = retrieve_pins()
if not pins:
    enter_pins_from_csv()


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
