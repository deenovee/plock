import os
from dotenv import load_dotenv
from sh import Password
from functions.load_variables import Variables
from functions.inputs import Inputs
from functions.g_pass import GPass
import datetime
from datetime import datetime as dt, timedelta
import sqlite3
import getpass
import bcrypt

#initialize db
conn = sqlite3.connect('lockin.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords (acct text, email text, p text, update_timestamp text)''')

variables = Variables()
inputs = Inputs()
g_pass = GPass()

def p_menu():
    p_phrase = variables.check_passphrase()

    print("Password Manager\n")
    try:
        passphrase = getpass.getpass(prompt="Please enter passphrase to begin: ")
        if bcrypt.checkpw(passphrase.encode(), p_phrase):
            print("Access granted\n")
            while True:
                try:
                    print("C, R, U, D, exit: (1/2/3/4/5)\n")
                    crud_choice = input("")
                except Exception as e:
                    print(e)
                try:
                    crud_choice = int(crud_choice)
                    if crud_choice == 1:
                        acct = inputs.get_string("Account Name")
                        print('')
                        email = inputs.get_string("Email")
                        print('Already have a code? (y/n):')
                        existing_code = inputs.get_boolean()

                        if existing_code:
                            code_input = inputs.get_string("Existing code")
                            pw = g_pass.g_pass(str(code_input))
                            print('')
                            print('Generating password...\n\n')
                        else:
                            pw = g_pass.g_pass(g_pass.generate_random_string())
                            print('')
                            print('Generating password')

                        update_timestamp = datetime.datetime.now()
                        p = Password(acct, email, pw, update_timestamp)
                        print(f'Account: {p.acct}\nEmail: {p.email}\nPassword: {p.p}\nDate: {p.update_timestamp}\n') 
                        try:
                            c.execute("INSERT INTO passwords (acct, email, p, update_timestamp) VALUES (?, ?, ?, ?)", (p.acct, g_pass.encrypt(p.email), g_pass.encrypt(p.p), p.update_timestamp))
                            conn.commit()
                        except sqlite3.Error as e:
                            print(e)
                        except Exception as e:
                            print(e)

                    if crud_choice == 2:
                        accounts = c.execute("SELECT acct, email, p, update_timestamp FROM passwords")
                        accounts = accounts.fetchall()
                        if len(accounts) <= 0:
                            print("No accounts found.")
                        else:
                            for account in range(len(accounts)):
                                print(f'{account+1}. Account: {accounts[account][0]}')
                        print("Password not on this list? Want to enter a code? (y/n):")
                        existing_code = inputs.get_boolean()
                        if existing_code:
                            code_input = inputs.get_string("Existing code")
                            pw = g_pass.g_pass(str(code_input))
                            print('')
                            print('Generating password...\n\n')
                            print(f'Password: {pw}')
                        else:
                            account_choice = inputs.get_int("Please select an account to view: ")
                            print('')
                            print(f'Account: {accounts[account_choice-1][0]}\nEmail: {g_pass.decrypt(accounts[account_choice-1][1])}\nPassword: {g_pass.decrypt(accounts[account_choice-1][2])}\nDate: {accounts[account_choice-1][3]}\n')
                            
                    if crud_choice == 3:
                        accounts = c.execute("SELECT acct, email, p, update_timestamp FROM passwords")
                        accounts = accounts.fetchall()
                        if len(accounts) <= 0:
                            print("No accounts found.\n")
                        else:
                            for account in range(len(accounts)):
                                print(f'{account+1}. Account: {accounts[account][0]}')

                            account_choice = inputs.get_int("Please select an account to update: ")
                            print('')
                            for i in range(4):
                                print(f'{i+1}. {accounts[account_choice-1][i]}\n')
                            print('Choose an account attribute to update: ')
                            
                            try:
                                update_choice = inputs.get_int("1/2/3/4\n")
                            except ValueError as e:
                                print(e)

                            try:
                                date = datetime.datetime.now()
                                if update_choice == 1:
                                    acct = inputs.get_string("Account Name")
                                    c.execute("UPDATE passwords SET acct = ?, update_timestamp = ? WHERE acct = ?", (acct, date, accounts[account_choice-1][0]))
                                    conn.commit()
                                elif update_choice == 2:
                                    email = inputs.get_string("Email")
                                    c.execute("UPDATE passwords SET email = ? WHERE email = ?", (g_pass.encrypt(email), accounts[account_choice-1][1]))
                                    conn.commit()
                                elif update_choice == 3:
                                    print('Generating password...\n\n')
                                    pw = g_pass.g_pass(g_pass.generate_random_string())
                                    c.execute("UPDATE passwords SET p = ? WHERE p = ?", (g_pass.encrypt(pw), accounts[account_choice-1][2]))
                                    conn.commit()
                                else:
                                    print('Invalid input\n')
                            except ValueError as e:
                                print(e)
                            except sqlite3.Error as e:
                                print(e)
                            except Exception as e: 
                                print(e)


                    if crud_choice == 4:
                        accounts = c.execute("SELECT acct FROM passwords")
                        accounts = accounts.fetchall()
                        if len(accounts) <= 0:
                            print("No accounts found.")
                        else:
                            for account in range(len(accounts)):
                                print(f'{account+1}. Account: {accounts[account][0]}')

                            account_choice = inputs.get_int("Please select an account to update: ")
                            print('')
                            c.execute("DELETE FROM passwords WHERE acct = ?", (accounts[account_choice-1][0],))
                            conn.commit()
                    if crud_choice == 5:
                        conn.close()
                        break
                except ValueError as e:
                    print(e)
        else:
            print("Access denied\n")
            return
    except Exception as e:
        print(e)


if __name__ == "__main__":
    p_menu()

