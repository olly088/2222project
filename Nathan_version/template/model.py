'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    return page_view("register")

#---------------------------------------------

def register_add(username, password):
    '''
        register_add
        Returns the view for the register_add
    '''
    database_args = 'users.db' # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase(database_args)
    sql_db.add_user(username, sql_db.hash_salt_password(password), 0)

    return page_view("register_complete")

#---------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    database_args = 'users.db' # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase(database_args)
    
    # By default assume good creds
    username_exists = True
    login = True
    
    username_exists = sql_db.check_username(username)
    if not username_exists:
        err_str = "Incorrect Username"
        return page_view("invalid", reason=err_str)


    login = sql_db.check_credentials(username, password)
    
    # # if username != "admin": # Wrong Username
    # err_str = "Incorrect Username or password"
    # #     login = False
    
    # if password != "password": # Wrong password
    #     err_str = "Incorrect Password"
    #     login = False
        
    if login: 
        return page_view("valid", name=username)
    else:
        err_str = "Incorrect Password"
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)

def retrieve_friends(username):
    database_args = 'users.db' # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase(database_args)
    sql_db.get_all(username)
