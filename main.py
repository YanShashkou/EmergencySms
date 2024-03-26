import sqlite3

with sqlite3.connect('ES.db') as dt:
    cursor = dt.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,login TEXT NOT NULL UNIQUE,password TEXT NOT NULL)''')
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(user_id INTEGER,email TEXT NOT NULL)""")
    login_action = input('Login or Register: ').lower().strip()
    if login_action == 'register':
        try:
            login = input('Enter your login:')
            password = input('Enter your password:')
            cursor.execute("""INSERT INTO users(login,password) VALUES(?,?)""",(login,password))
            user_id = cursor.execute('''SELECT user_id FROM users WHERE login=?''',(login,)).fetchone()[0]
            print(user_id)
            is_adding = True
            while is_adding:
                contact_action = input('Do you want to add a contact?(y/n)').lower().strip()
                if contact_action == 'y':
                    email = input('Enter a contact email address:')
                    cursor.execute('''INSERT INTO contacts(user_id,email) VALUES(?,?)''',(user_id,email))
                else:
                    is_adding = False

        except:
            print(f'User {login} already exist')

    elif login_action == 'login':
        login = input('Enter your login:')
        password = input('Enter your password:')
        try:
            user_id = cursor.execute('''SELECT user_id FROM users WHERE login=? and password = ?''',(login,password)).fetchone()[0]
            contacts=cursor.execute('''SELECT email FROM contacts WHERE user_id = ? ''',(user_id,)).fetchall()
            action = input('Send the messages or add contact (send/add): ').lower().strip()
            if action == 'send':
                for contact in contacts:
                    print(f'Sending message to {contact[0]}')
                    # You can use Twillio API here
            elif action == 'add':
                is_adding = True
                while is_adding:
                    contact_action = input('Do you want to add a contact?(y/n)').lower().strip()
                    if contact_action == 'y':
                        email = input('Enter a contact email address:')
                        cursor.execute('''INSERT INTO contacts(user_id,email) VALUES(?,?)''', (user_id, email))
                    else:
                        is_adding = False
        except:
            print(f'Login or Password is wrong, please try again')