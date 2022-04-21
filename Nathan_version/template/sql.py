from operator import truediv
import sqlite3

import uuid
import hashlib
# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                print(string)
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # new_password = 'admin'
        # Add our admin user
        self.add_user('admin', admin_password, 1)
        # self.add

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin):
        sql_query = """
                SELECT max(id)
                FROM USERS
            """
        
        # sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        r = self.cur.fetchone()
        print(r)
        id = 1
        if (r[0] != None):
            id = r[0] + 1       
         
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin})
            """

        sql_cmd = sql_cmd.format(id=id, username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT password
                FROM USERS
                WHERE username = '{username}'
            """
        
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        r = self.cur.fetchone()
        pw_digest, salt = r[0].split(":")
        provided_pw_digest = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        return pw_digest == provided_pw_digest

    def check_username(self, username):
        sql_query = """
                SELECT 1
                FROM USERS
                WHERE username = '{username}'
            """
        
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        if self.cur.fetchone():
            return True
        else:
            return False  

    def get_all(self, username):
        sql_query = """
            SELECT *
            FROM USERS
            WHERE username != '{username}'
            """
        sql_query = sql_query.format(username=username)
        self.execute(sql_query)
        records = self.cur.fetchall()
        return records



    # Hash and salt passwords, store salt with pw in database
    def hash_salt_password(self, plaintext):
        salt = uuid.uuid4().hex
        # print("plaintext: " + plaintext + "\n")
        # print("Salt: " + salt + "\n")
        # print("plaintext hashed: " + hashlib.sha256(plaintext.encode()).hexdigest() + "\n")
        salted_pw_digest = hashlib.sha256(salt.encode() + plaintext.encode()).hexdigest() + ":" + salt
        # print("salted plaintext hashed: " + salted_pw_digest + "\n")
        # print("plaintext: " + plaintext + "\n")
        return salted_pw_digest

