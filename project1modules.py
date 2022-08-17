from abc import ABC, abstractmethod
from logging import exception
import mysql_config as c
import mysql.connector
import logging
import sys
class Customer(ABC):
    def __init__(self, lastName,firstName,email,Passcode):
        self._lastName = str(lastName)
        self._firstName = str(firstName)
        self._email = str(email)
        self._Passcode = int(Passcode)
        
    
    def setlastName(self, lastName,firstName):
        self._lastName = str(lastName)
        self._firstName = str(firstName)
    
    def getlastName(self):
        return self._lastName

    def setfirstName(self,firstName):
        self._firstName = str(firstName)
    
    def getfirstName(self):
        return self._firstName
    
    def __str__(self):
        return "lastName: " + self._lastName + ", firstName: " + self._firstName  + ", email: " + self._email + ", Passcode: " + str(self._Passcode)

    def accountcheck(self):
        input_value_email = (input('Enter email: \n'))
        input_value_passcode = (input('Enter Passcode: \n'))
        lines_list = open('p1.csv').read().splitlines()
        lst_customerData = []
        account_dict_list = lst_customerData
        for line in lines_list:
                    acc_dict = {}
                    acc_string_split = line.split(',')
                    acc_dict['last_name'] = acc_string_split[0]
                    acc_dict['first_name'] = acc_string_split[1]
                    acc_dict['email'] = acc_string_split[2]
                    acc_dict['Passcode'] = acc_string_split[3]
                    acc_dict['Product'] = acc_string_split[4]
                    account_dict_list.append(acc_dict)
        key,value = 'email',str(input_value_email)
        dictList = [ myDict for myDict in account_dict_list if myDict.get(key) == value ]
        if (dictList[0]["email"] == str(input_value_email)) and ((dictList[0]["Passcode"] == (input_value_passcode))):
            print("true")
            lastName = dictList[0]['last_name']
            firstName = dictList[0]['first_name']
            email = str(dictList[0]['email'])
            Passcode = int((dictList[0]['Passcode']))
            productOrdered = (dictList[0]['Product'])
            print("You have successfully logged in ")
            print(firstName)
            print(lastName)
            print(email)
            print(Passcode)
            print(productOrdered)
        else:
            print("Sorry wrong combination of email and password entered ")
class Newuser(Customer):

    def sleep(self):
        print("***snore***")
    
    def email_format_validation(input):
        while True:
            try:
                email = (input("Enter your chosen email in a similar format to john@gmail.com: "))
                pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                match = re.fullmatch(pattern, email)
                if match:
                    print("correct input")
                    return match
                else: 
                    raise ValueError ("incorrect format please try again! ")
            except ValueError as e:
                print(e)
            except Exception as e:
                print_exc()
                print("Exception was raised... Trying again...")
            else:
                break
    
class CurrentUser(Customer):

    def login(cursor):
        cnx = mysql.connector.connect(user=c.user, password=c.password, host=c.host, database="Project1")
        cursor = cnx.cursor()
        count=0
        print("PLease note that after 3 unsuccessful attempts of a user login you will be prompted to create a new account!")
        while(count < 3):
            print('Enter email: ')
            login_email = input()
            print('Enter Pascode: ')
            login_passcode= input()
            checkemail=f"SELECT * FROM AllCustomers WHERE email='{login_email}' AND Passcode = '{login_passcode}'"
            cursor.execute(checkemail)
            record = cursor.fetchone()
            if record == None:
                print('email and passcode combination does not exist please try again')
                count += 1
            else:
                lastName=record[1]
                firstName=record[2]
                email=record[3]
                print("Thank you for logging in",firstName,lastName, "email:",email)
                print("Welcome",firstName, "please select an option for the type of user you are:")
                logging.info("User has successfully logged in")
                print("\t1) Normal User")
                print("\t2) Admin")
                user_input=input()
                if user_input=="2":
                    print("Please enter admin password: ")
                    adminpassword=input()
                    if adminpassword=="1234":
                        logging.info("Admin has successfully logged in")
                        while(True):
                            print("\nWelcome admin please select an option for the type of action to perform:")
                            print("\t1) Update User Data!")
                            print("\t2) Insert Products!")
                            print("\t3) Delete Products Or Users")
                            print("\t4) Display total orders")
                            print("\t5) Show all customer data")
                            print("\t6) Exit the program")
                            

                            
                            admin_input=input()
                            if admin_input=="1":
                                    query = "SELECT CustomerID, LastName, FirstName, email, passcode FROM Allcustomers"
                                    cursor.execute(query)
                                    for record in cursor:
                                        print(f"\t{record[0]}: lastname: {record[1]}, firstname: {record[2]}, email: {record[3]}, passcode: {record[4]}")
                                    customer_to_modify = input("Enter the CustomerID for the account you wish to update ")
                                    col_to_modify = input("Select an attribute to modify (lastName, firstName, email, passcode): ")
                                    modified_value = input(f"What do you want to change {col_to_modify} to?")
                                    if col_to_modify == 'passcode':
                                        update_statement = f"UPDATE Allcustomers SET {col_to_modify}={modified_value} WHERE CustomerID={customer_to_modify}"
                                    else:
                                        update_statement = f"UPDATE Allcustomers SET {col_to_modify}='{modified_value}' WHERE CustomerID={customer_to_modify}"
                                    cursor.execute(update_statement)
                                    cnx.commit()
                                    print("You have sucessfully updated",col_to_modify, "to", modified_value)
                                    logging.info("Admin has updated user data")
                            if admin_input=="2":
                                query = f"SELECT * FROM cardinventory"
                                cursor.execute(query)
                                for record in cursor:
                                    print(f"\tInventoryID: {record[0]}: Product: {record[1]}, Price: {record[2]}, releaseyear: {record[3]}")
                                name_of_product = input("Enter the name of the product you wish to add: ")
                                price_of_product = input("Enter the price of the product: ")
                                release_of_product = input(f"What year was the product produced in?")
                            
                                update_statement = f"INSERT INTO cardinventory(Product, Price, releaseyear)VALUES({name_of_product}, {price_of_product}, {release_of_product})"
                                
                                cursor.execute(update_statement)
                                cnx.commit()
                                print("You have sucessfully added",name_of_product , "to the inventory database")
                                logging.info("Admin has added to inventory table")
                            if admin_input=="3":
                                query = "SELECT CustomerID, LastName, FirstName, email, passcode FROM Allcustomers"
                                cursor.execute(query)
                                for record in cursor:
                                    print(f"\t{record[0]}: lastname: {record[1]}, firstname: {record[2]}, email: {record[3]}, passcode: {record[4]}")
                                customer_to_delete = input("Enter the CustomerID for the account you wish to delete ")
                                adminpass=input("To confirm this deletion please enter admin password")
                                if adminpass=="1234":
                                    update_statement = f"DELETE FROM Allcustomers WHERE CustomerID={customer_to_delete}"
                                    cursor.execute(update_statement)
                                    cnx.commit()
                                    print("You have sucessfully deleted CustomerID",customer_to_delete)
                                    logging.info("Admin has deleted user data")
                                else:
                                    print("cannot continue to delete without correct admin password")
                                    logging.info("Admin has failed to delete user data")
                            if admin_input=="4":
                                query = f"SELECT OrderID, email, orderProduct, Productprice FROM pokemonorders"
                                cursor.execute(query)
                                for record in cursor:
                                    print(f"\t OrderID: {record[0]}: email: {record[1]}, Product: {record[2]}, price: {record[3]}")
                            if admin_input=="6":
                                logging.info("Admin has exited the program")
                                print("Closing program...")
                                sys.exit()
                            if admin_input=="5":
                                query = "SELECT CustomerID, LastName, FirstName, email, passcode FROM Allcustomers"
                                cursor.execute(query)
                                for record in cursor:
                                    print(f"\t{record[0]}: lastname: {record[1]}, firstname: {record[2]}, email: {record[3]}, passcode: {record[4]}")
                if user_input=="1":
                    while(True):
                        print("\nWelcome", firstName, "please select an option for the type of action to perform:")
                        print("\t1) Order a product")
                        print("\t2) Display order history")
                        print("\t3) Display order total")
                        print("\t4) Update your information")
                        print("\t5) Exit the program")
                        input_value=input()
                        if input_value=="5":
                            print("Thank you for using our application")
                            cursor.close()
                            cnx.close()
                            logging.info("Customer has exited the program")
                            sys.exit()
                        if input_value=="2":
                            query = f"SELECT orderProduct FROM pokemonorders WHERE email='{email}'"
                            cursor.execute(query)
                            for record in cursor:
                                print(f"\tProduct Ordered: {record[0]}")
                        if input_value=="3":
                            query = f"SELECT SUM(ProductPrice) FROM pokemonorders WHERE email='{email}'"
                            cursor.execute(query)
                            for record in cursor:
                                print(f"\tTotal spent on our products: {record[0]}")
                        if input_value=="4":
                            query = f"SELECT CustomerID, LastName, FirstName, email, passcode FROM Allcustomers WHERE email='{email}'"
                            cursor.execute(query)
                            for record in cursor:
                                print(f"\t CustomerID: {record[0]}: lastname: {record[1]}, firstname: {record[2]}, email: {record[3]}, passcode: {record[4]}")
                            col_to_modify = input("Select an attribute to modify (lastName, firstName, email, passcode): ")
                            modified_value = input(f"What do you want to change {col_to_modify} to?")
                            if col_to_modify == 'passcode':
                                update_statement = f"UPDATE Allcustomers SET {col_to_modify}={modified_value} WHERE email='{email}'"
                            else:
                                update_statement = f"UPDATE Allcustomers SET {col_to_modify}='{modified_value}' WHERE email='{email}'"
                            cursor.execute(update_statement)
                            cnx.commit()
                            print("You have sucessfully updated",col_to_modify, "to", modified_value)
                            logging.info("Customer has updated their information")
                        if input_value == "1":
                                print("\n Which year would you like to order from?")
                                print("\t1) 2022")
                                print("\t2) 2021")
                                print("\t3) 2020")
                                year_value=input()
                                if year_value =="1":
                                    query = "SELECT InventoryID, Product, Price, releaseyear FROM cardinventory WHERE releaseyear=2020"
                                    cursor.execute(query)
                                    for record in cursor:
                                            print(f"\t InventoryID: {record[0]}: Product: {record[1]}, Price: {record[2]}, releaseyear: {record[3]}")
                                    print("\n Which would you like to order? Example Pokemon-Pokemon go is input 1 and has a cost of 90 dollars ")
                                    print("\t1 Pokemon-Pokemon Go")
                                    print("\t2 Pokemon-Astral Radiance")
                                    print("\t3 Pokemon-Brilliant Stars")
                                    print("\t4 Pokemon-Lost Origin")
                                    order_input=input()
                                    if order_input=="1":
                                        productprice=90
                                        productOrdered="Pokemon-Pokemon Go"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="2":
                                        productprice=120
                                        productOrdered="Pokemon-Astral Radiance"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="3":
                                        productprice=135
                                        productOrdered="Pokemon-Brilliant Stars"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="4":
                                        productprice=140
                                        productOrdered="Pokemon-Lost Origins"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    print("What would you like to do next?")
                                    print("\t1 Return to main customer menu")
                                    print("\t2 Exit the program")
                                    user_choice=input()
                                    if user_choice=="1":
                                        continue
                                    elif user_choice=="2":
                                        logging.info("Customer has exited the program")
                                        sys.exit()
                                    
                                if year_value =="2":
                                    query = "SELECT InventoryID, Product, Price, releaseyear FROM cardinventory WHERE releaseyear=2021"
                                    cursor.execute(query)
                                    for record in cursor:
                                            print(f"\t InventoryID: {record[0]}: Product: {record[1]}, Price: {record[2]}, releaseyear: {record[3]}")
                                    print("\n Which would you like to order?")
                                    print("\t1 Pokemon-Fusion Strike")
                                    print("\t2 Pokemon-Celebrations")
                                    print("\t3 Pokemon-Evolving Skies")
                                    print("\t4 Pokemon-Battle Styles")
                                    print("\t5 Pokemon-Shining Fates")
                                    print("\t6 Pokemon-Champions Path")
                                    print("\t7 Return to the main customer menu")

                                    order_input=input()
                                    if order_input=="1":
                                        productprice=90
                                        productOrdered="Pokemon-Fusion Strike"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="2":
                                        productprice=200
                                        productOrdered="Pokemon-Celebrations"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="3":
                                        productprice=160
                                        productOrdered="Pokemon-Evolving Skies"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="4":
                                        productprice=70
                                        productOrdered="Pokemon-Battle Styles"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="5":
                                        productprice=155
                                        productOrdered="Pokemon-Shining Fates"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="6":
                                        productprice=55
                                        productOrdered="Pokemon-Champions Path"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has ordered a product")
                                    if order_input=="7":
                                        logging.info("Customer has returned to the main menu")
                                        continue
                                    print("What would you like to do next?")
                                    print("\t1 Return to main customer menu")
                                    print("\t2 Exit the program")
                                    user_choice=input()
                                    if user_choice=="1":
                                        continue
                                    elif user_choice=="2":
                                        print("exiting program...")
                                        logging.info("Customer has exited the program")
                                        sys.exit()
                                if year_value =="3":
                                    query = "SELECT InventoryID, Product, Price, releaseyear FROM cardinventory WHERE releaseyear=2020"
                                    cursor.execute(query)
                                    for record in cursor:
                                            print(f"\t InventoryID: {record[0]}: Product: {record[1]}, Price: {record[2]}, releaseyear: {record[3]}")
                                    print("\n Which would you like to order? Example Pokemon-Pokemon go is input 1 and has a cost of 90 dollars ")
                                    print("\t1 Pokemon-Vivid Voltage")
                                    print("\t2 Start Over")
                                    print("\t3 Exit Program")
                                    order_input=input()
                                    if order_input=="1":
                                        productprice=115
                                        productOrdered="Pokemon-Vivid Voltage"
                                        print("You have chosen to order",productOrdered,"for the price of:",productprice)
                                        add_orders_db = f"INSERT INTO pokemonOrders(orderProduct, email, Productprice) VALUES ('{productOrdered}', '{email}',{productprice})"
                                        cursor.execute(add_orders_db)
                                        cnx.commit()
                                        logging.info("Customer has purchased a product")
                                    if order_input=="2":
                                        continue
                                    if order_input=="3":
                                        print("Exiting program...")
                                        logging.info("Customer has exited the program")
                                        sys.exit()
                                    print("What would you like to do next?")
                                    print("\t1 Return to main customer menu")
                                    print("\t2 Exit the program")
                                    if user_choice=="1":
                                        continue
                                    elif user_choice=="2":
                                        logging.info("Customer has exited the program")
                                        sys.exit()
                    
                                        
                    
                
            

class Admin(Customer):
    def adminFeatures():
        print("\nWelcome admin please select an option for the type of action to perform:")
        print("\t1) Create a table")
        print("\t2) Update Products Or User Data!")
        print("\t3) Insert Products!")
        print("\t4) Delete Products Or Users")
