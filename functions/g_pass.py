import math
import random
import string
from cryptography.fernet import Fernet
import os
from functions.load_variables import Variables
import sqlite3

variables = Variables()
key = variables.check_key()

class GPass:
    def __init__(self):
        self.conn = sqlite3.connect("lockin.db")
        self.c = self.conn.cursor()
        self.p_phrase_length = 0
        self.p_pin_length = 0
        self.phrase_list = []
        self.pin_list = []
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']

    def generate_random_string(self):
        letters = list(string.ascii_lowercase)[:14]
        numbers = [str(i) for i in range (1,20)]
        random_string = []
        for _ in range(3):
            random_string.append(random.choice(numbers))
            random_string.append(random.choice(letters))
        return ''.join(random_string[:5])
    
    def g_pass(self, r_string):
        self.phrase_list = []
        self.pin_list = []

        # with open('phrase.txt', 'r') as f:
        #     for line in f:
        #         self.p_phrase_length += 1
        #         self.phrase_list.append(line.strip())

        # with open('pin.txt', 'r') as g:
        #     for line in g:
        #         self.p_pin_length += 1
        #         self.pin_list.append(line.strip())

        self.c.execute("SELECT phrase FROM phrases")
        phrases = self.c.fetchall()
        for phrase in phrases:
            self.phrase_list.append(self.decrypt(phrase[0]))

        # Retrieve pins from the pins table
        self.c.execute("SELECT pin FROM pins")
        pins = self.c.fetchall()
        for pin in pins:
            self.pin_list.append(self.decrypt(pin[0]))

        pw = []
        i = 0
        while i < len(r_string):
            char = r_string[i]
            if char.isdigit():
                if i + 1 < len(r_string) and r_string[i + 1].isdigit():
                    num = int(r_string[i:i+2])
                    pw.append(self.phrase_list[num-1])
                    i += 2
                else:
                    num = int(char)
                    pw.append(self.phrase_list[num-1])
                    i += 1
            elif char.isalpha():
                char_index = self.alphabet.index(char)
                pw.append(self.pin_list[char_index])
                i += 1
            else:
                i += 1
        return ''.join(pw)


    def encrypt(self, pw):
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(pw.encode())
        return ciphered_text
        
    def decrypt(self, ciphered_text):
        cipher_suite = Fernet(key)
        unciphered_text = (cipher_suite.decrypt(ciphered_text)).decode()
        return unciphered_text