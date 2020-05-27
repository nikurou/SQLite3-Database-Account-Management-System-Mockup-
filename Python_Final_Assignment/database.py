

# Name:         Dylan Chung
# Assignment:   Final Project
# Class:        CS2520.01
# Date:         05/13/2020

'''

 A simple mock sign-in and log-off user account database program which holds various features such as
 account registration, log-in, forgot password, reset password, account deletion, and log-off.
'''




import sqlite3
import re  # Regular expressions

# Conncects to DB, if it exists. Otherwise creates it

conn = sqlite3.connect('userbase.db') #:memory:
c = conn.cursor()


# Create the database table
def initializeDBTable():
    c.execute("""CREATE TABLE user(
             userName text,
             password text,
             DOB text
             )""")

"""
Given a username and password, add the user to the database 
IFF the user does not already exist.
"""
def addUserToDataBase(userName, password, DOB):
    if(checkIfUserExist(userName) == False):
        c.execute("INSERT INTO user VALUES(?, ?, ?)",(userName,password, DOB))
        conn.commit()  # commits the current transaction
    else:
        print("The user already exists. Please try again")

# Only available once logged in or forgot password
def resetPassword(username):
    print("Resetting password........")
    password = setPassword()
    originalPassword = getAccountFromDB(username)[1]

    while password == originalPassword:
        print("Your new password may not be the same as your original password. Please try again.")
        password = setPassword()

    c.execute("""UPDATE user SET password = ? WHERE userName = ?""", (password, username))
    conn.commit()

    print("Password succesfully changed!")

def setPassword():
    print("Password must contain at least one capital letter and one special character (!,@,#,$,%) and one number.")
    while True:
        passw = str(input("Please input a password: "))
        regexPunc = re.compile('[@_!#$%^&*()<>?/\|}{~:]?=*[A-Z]')
        regexNum = re.compile('\d')
        if (regexPunc.search(passw) and regexNum.search(passw)):
            return passw
        else:
            print("Error, password must contain at least one capital letter and one special character (!,@,#,$,%) and one number and length 5")

# returns corresponding user object in the database
def getAccountFromDB(username):
    c.execute("SELECT * FROM user WHERE userName = ?", (username,))
    return c.fetchone()


# return true if user is in db, else return false
def checkIfUserExist(userName):
    account = getAccountFromDB(userName)

    if account is None:
        return False
    else:
        return True

def signUp():
    print("Registering an account? Please enter your desired username and password")

    # Set Username
    while(True):
        try:
            # Make sure username doesn't already exist.
            user = str(input("Username: "))
            if checkIfUserExist(user) is True:
                print("This username is already taken! Please use something else.")
            else:
                break
        except Exception:
            print("Exception Occurred. Please try again")

    # Get password (i.e. at least one capital letter and one special character (!,@,#,$,%) and one number)
    print("Password must contain at least one capital letter and one special character (!,@,#,$,%) and one number and length 5.")
    while True:
        passw = str(input("Please input a password: "))
        p = re.compile('^(?=.*[!@#$%&*?])(?=.*[a-z])(?=.*[A-Z]).{5,}$')
        if p.search(passw):
            break;
        else:
            print("Error, password must contain at least one capital letter and one special character (!,@,#,$,%) and one number and length 5")

    # Get DOB

    r = re.compile('\d{2}/\d{2}/\d{4}')
    while(True):
        DOB = str(input("Date of Birth (mm/dd/xxxx): "))
        if r.match(DOB) is not None:
            break
        else:
            print("DOB must be entered in mm/dd/xxxx format")

    addUserToDataBase(user,passw, DOB)
    print("Successfully registered! Returning to menu page....")
    menu()

def login():
    user = str(input("Username: "))
    passw = str(input("Password: "))

    if getAccountFromDB(user) is None:
        print("\nThe account does not exist. Please try again.\n")
        return menu()
    elif getAccountFromDB(user)[1] == passw:  # Password matches
        print("Login successful, welcome back ", user, "!")
        return insideMenu(user)
    else:
        print("\nThe account you are trying to access does not exist or the password was incorrect. Please try again")
        return menu()


def forgotPassword():
    user = str(input("Input your username: "))
    if checkIfUserExist(user) == True:
        if verifyDOB(user) == True:
            resetPassword(user)
            menu()
    else:
        print("The account you are trying to access does not exist. Returning to menu")
        menu()

def verifyDOB(username):
    r = re.compile('\d{2}/\d{2}/\d{4}')

    for i in range(3):
        DOB = str(input("Date of Birth (mm/dd/xxxx): "))
        if r.match(DOB) is not None:
            return True
        else:
            print("Incorrect format or incorrect date error, remaining attempts: ", 2-i)
    print("Failed to input correct DOB, returning to menu")
    menu()

# Menu options when not logged in
def processCommand(command):
    if command == 1:
        login()
    elif command == 2:
        signUp()
    elif command == 3:
        forgotPassword()
    elif command == 4:
        print("Thank you for using the program. Goodbye")
        return

# Menu options when logged in
def processAccountCommand(command, username):
    if command == 1:
        resetPassword(username)
        insideMenu(username)
    elif command == 2:
        deleteAccountFromDB(username)
    elif command == 3:
        print("Log off successful! Until we meet again, ", username, "!")
        menu()

def deleteAccountFromDB(username):
    print("Warning this action cannot be undone!")

    while(True):
        verification = input("Are you want to delete account (Y/N): ")
        if(verification == 'Y'):
            print("Account deletion confirmed, good riddance!")
            c.execute("""DELETE from user where userName = ?""", (username, ))
            conn.commit()
            menu()
        elif(verification == 'N'):
            print("Account deletion cancelled, returning to your account page")
            insideMenu(username)
            break
        else:
            print("Invalid input, try again.")

def menu():
    print("\nHello and welcome to my simple mock user sign up and sign in page!")
    print("-----------------------------------------------------------------------")
    print("1.) Login ")
    print("2.) Don't have an account? Sign up")
    print("3.) Forgot password?")
    print("4.) Exit")
    print("-----------------------------------------------------------------------\n")
    run = True
    while(run):
        try:
            command = int(input("Enter a command: "))
            if(command >= 1 and command <= 4):
                run = False
                print()
                processCommand(command)
            else:
                print("Invalid Input, please try again!")
        except Exception:
            pass

def insideMenu(username):
    print("Successfully signed in!")
    print("-----------------------------------------------------------------------")
    print("1.) Reset Password ")
    print("2.) Delete Account")
    print("3.) Log-Off")
    print("-----------------------------------------------------------------------")
    run = True
    while (run):
        try:
            command = int(input("Enter a command: "))
            if (command >= 1 and command <= 3):
                run = False
                print()
                processAccountCommand(command, username)
            else:
                print("Invalid Input, please try again!")
        except Exception:
            pass



def main():
    try:
        initializeDBTable()
        menu()
    except sqlite3.OperationalError:  # Table user already exists
        menu()
    finally:
        conn.close()

main()