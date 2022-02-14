# coding=utf-8
# This is a sample Python script.

# import required module
import getpass
import warnings
import time
import sys
import serial

device = 'com4'
has_been_encrypted = 0

from cryptography.fernet import Fernet, InvalidToken

warnings.filterwarnings(action='ignore',module='.*paramiko.*')


def measure_time():
    dumm


def get_logged_user():
    user =  getpass.getuser()
    return user

def get_key(file_name):
    # opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    # using the generated key
    fernet = Fernet(key)

    return fernet


def encrypt_file(file_name, file_name_key):

    global has_been_encrypted
    fernet = get_key(file_name_key)

    # opening the original file to encrypt
    with open(file_name, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    has_been_encrypted = 1
    print("File encrypted")

def decrypt_file(file_name, file_name_key):
    
    global has_been_encrypted
    # using the key
    fernet = get_key(file_name_key)

    # opening the encrypted file
    with open(file_name, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(file_name, 'wb') as dec_file:
        dec_file.write(decrypted)
    
    has_been_encrypted = 0
    print("File decrypted")

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("User logged in -> {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    name_of_file = "importantStuff.txt"
    name_of_long_file = "LongFile.txt"
    name_of_file_key = "filekey.key"
    user = get_logged_user()
    print_hi(user)
    
    try:
        arduinoCard = serial.Serial(device,9600)
        time.sleep(1)
        print("Arduino com started")
        print('Reading data from Arduino card')
    except:
        print("Arduino card not available")
        
    while True:
        time.sleep(2)
        
        #incoming_data = arduinoCard.read()
        #print(incoming_data)
        try:
            data = arduinoCard.read()
            #print(data)
            if (user == "hse15" and data == b'\x01'):
                #print('Flag1 {} '.format(has_been_encrypted))
                try:
                    print("decrypting")
                    start = time.time()
                    decrypt_file(name_of_long_file, name_of_file_key)
                    end = time.time()
                    print("Elapsed time: {}".format(end - start))
                except InvalidToken:
                    print('File: {} already decrypted'.format(name_of_long_file))

            else:
                #print('Flag2 {} '.format(has_been_encrypted))
                if(has_been_encrypted == 0):
                    print("Start encrypting")
                    start = time.time()
                    encrypt_file(name_of_long_file, name_of_file_key)
                    end = time.time()
                    print("Elapsed time: {}".format(end - start))
                else:
                    print('File {} already encrypted'.format(name_of_long_file))
        except:
            print("Processing")
            
#TODO
#logging
#try different algorithm
#handle big files to encrypt