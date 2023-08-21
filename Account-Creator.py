import mysql.connector

global db
db = mysql.connector.connect(
    host="localhost",
    user="Aramis",
    passwd="123456",
    database="testDataBase"
)

def signUp():
    userName = input("Enter your username: ")
    password = input("Enter your password: ")

    mycursor = db.cursor(buffered=True)

    mycursor.execute("SELECT * FROM LoginInfo WHERE username = %s AND password = %s", (userName, password))
    matchingLogin = mycursor.fetchone()

    if matchingLogin is None:
        mycursor.execute("INSERT INTO LoginInfo (username, password) VALUES (%s, %s)", (userName, password))
        db.commit()
    else:
        print("User already exists!")

    # Move to the next result set if available
    if mycursor.nextset():
        pass

    mycursor.close()

def login():
    userName = input("Enter your username: ")
    password = input("Enter your password: ")

    mycursor = db.cursor(buffered=True)

    mycursor.execute("SELECT * FROM LoginInfo")
    table_exist = mycursor.fetchone() is not None

    if table_exist:
        mycursor.execute("SELECT * FROM LoginInfo WHERE username = %s AND password = %s", (userName, password))
        matchingLogin = mycursor.fetchone()

        if matchingLogin is not None:
            print("Login successful!")
        else:
            print("Login failed!")

    else:
        print("Login does not exist!")
    # Move to the next result set if available
    if mycursor.nextset():
        pass

    mycursor.close()

def showTable():
    mycursor = db.cursor(buffered=True)

    mycursor.execute("SELECT * FROM LoginInfo")
    rows = mycursor.fetchall()

    for row in rows:
        print(row)

    mycursor.close()

def main():
    running = True
    while running:
        print("1. Sign up")
        print("2. Login")
        print("3. Show table")
        print("4. Exit")
        option = int(input("Enter your option: "))

        if option == 1:
            signUp()
        elif option == 2:
            login()
        elif option == 3:
            showTable()
        elif option == 4:
            print("Thank you")
            running = False

main()
