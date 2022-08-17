from configparser import DuplicateSectionError
import mysql.connector
from mysqlx import IntegrityError
import mysql_config as c
from project1modules import Admin, CurrentUser, Customer, Newuser
import re
from traceback import print_exc
from ast import In, IsNot
import logging
import sys
from abc import ABC, abstractmethod
from logging import exception
import emoji

def main():
    
    try:
        cnx = mysql.connector.connect(user=c.user, password=c.password, host=c.host, database="Project1")
        cursor = cnx.cursor()
    except mysql.connector.Error as mce:
        print(mce.msg)
        return
    except Exception as e:
        print("ERROR: Exiting program")
        return
    
    logging.basicConfig(filename="Project1.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')

    print("*** WELCOME TO ANDREW'S CARD SHOP! ***")

    lst_customerData = loadCustomerData_db(cursor)
    logging.info("Loaded data into lst_customerData...")
    
    while(True):
        cardData = insert_customerData(cursor)
        if cardData != None:
            cnx.commit()
            lst_customerData = loadCustomerData_db(cursor)
            pass

        if cardData==None:
            break
        else:
            logging.info("Inserted a new Data...")
            
        lst_customerData.append(cardData)

    
        if type(cardData)==Newuser:
                add_customer_db = f"INSERT INTO AllCustomers (lastName, firstName, email, Passcode) VALUES ('{cardData._lastName}', '{cardData._firstName}', +'{cardData._email}', {cardData._Passcode})"
                cursor.execute(add_customer_db)
                cnx.commit()
    cnx.commit()
    cursor.close()
    cnx.close()
    logging.info("Things are done")


def loadCustomerData_db(cursor) -> list:
    query = "SELECT CustomerID, lastName, firstName, email, Passcode FROM AllCustomers"

    cursor.execute(query)
    lst_customerData = []

    for record in cursor:
        cardData = None
        if record[3] != None:
            cardData = Newuser(record[1], record[2], record[3], record[4])
        else:
            raise Exception("NO PASSCODE NO ACCOUNT CREATED!")
        lst_customerData.append(cardData)
    
    return lst_customerData

def save_customerData(fname, lst_customerData):
    with open(fname, "w") as f:
        for cardData in lst_customerData:
            if type(cardData) == Newuser:
                f.write(cardData._lastName + "," + cardData._firstName + "," + str(cardData._email) + "," + str(cardData._Passcode) + "," + cardData._productOrdered + ",\n")
            else:
                pass

def insert_customerData(cursor) -> Customer:
    print("\nWelcome Please select an option :")
    print("\t1) I am a current member")
    print("\t2) I am a new member")
    print("\t3) Quit")
    customer_value = input(">>> ")
    if customer_value== "1":
        CurrentUser.login(cursor)
    if customer_value == "2":
        pass
    if customer_value == "3":
        sys.exit()

    while(True):
        print("\nWelcome Please select an option :")
        print("\t1) Create new account")
        print("\t2) Quit")
        input_value = input(">>> ")
        if input_value == "1":
            pass
        if input_value == "2":
            sys.exit()
        while (True):
            try:
                firstName = (input("Creating account... Please enter first name: "))
                firstName.split()
                c=0
                s='[@_!#$%^&*()<>?/\|}{~:]'
                if firstName == "Quit":
                        break
                for i in range(len(firstName)):
                    if firstName[i] in s:
                        c+=1
                    if c:
                        raise ValueError("No special characters!")
                    if any(i.isdigit() for i in firstName):
                        raise ValueError('Name must not contain any digits')
            except ValueError as e:
                print(e)
            except Exception as e:
                print_exc()
                print("Exception was raised... Trying again...")
            else:
                break
        while (True):
            try:
                lastName = str(input("Creating account... Please enter last name: "))
                if lastName == "quit":
                            break
                lastName.split()
                c=0
                s='[@_!#$%^&*()<>?/\|}{~:]'
                for i in range(len(lastName)):
                    if lastName[i] in s:
                        c+=1
                    if c:
                        raise ValueError("No special characters!")
                    if any(i.isdigit() for i in lastName):
                        raise ValueError('Name must not contain any digits')
            except ValueError as e:
                print(e)
            except Exception as e:
                print_exc()
                print("Exception was raised... Trying again...")
            else:
                break
        while True:
                    try:
                        email = (input("Enter your chosen email in a similar format to john@gmail.com: "))
                        if email == "quit":
                            break
                        pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                        match = re.fullmatch(pattern, email)
                        if match:
                            checkemail=f"SELECT * FROM AllCustomers WHERE email='{email}'"
                            cursor.execute(checkemail)
                            record = cursor.fetchone()
                            if record == None:
                                print('email is not taken')
                                
                            else:
                                print('email is unavailable!')
                                raise Exception
                        else: 
                            raise ValueError ("incorrect format please try again! ")
                    except ValueError as e:
                        print(e)
                    except Exception as e:
                        print("Exception was raised... Duplicate email please try again")
                    else:
                        break


        while True:
            try:
                Passcode = (input("Enter your chosen Passcode 4 digits only please "))
                num_format = re.compile(r'^\D{0}[0-9]{4}$\D{0}')
                it_is = re.match(num_format,Passcode)
                if it_is: 
                    print("Passcode accepted")
                else: 
                    raise ValueError('Only numbers and only four digits please!')
            except ValueError as e:
                print(e)
            except Exception as e:
                print_exc()
                print("Exception was raised... Trying again...")
            else:
                break
            
        
        if customer_value == "2":
            cardData = Newuser(lastName,firstName,email,Passcode)
            logging.info("Customer has entered their data and it's now mapped to cardData")
        else:
            cardData = None

        return cardData

if __name__ == "__main__":
    main()