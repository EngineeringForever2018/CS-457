"""
Author: Jared Lam
Class: CS 457
Project 1: Metadata Management
Date: 9/14/2021
"""

import os
from shutil import rmtree

#Dir is the abbreviation, which means the database directory
sourceDir = ""
workDir = ""

"""
The first implement function for this project is createDB which stands for
creation database and it creates a user to specified database and see if there
is any errors or not
"""
def createDB(db):  #db stands for database
    #Creating database if it doesn't exist in the system
    try: #Allows us to test a block of code for errors of the creation database function
        #This allows us to store the string after the phrase "CREATE DATABASE"
        directory = db.split("CREATE DATABASE ")[1]
        #Checking to see if this specific database exist or not
        if os.path.exists(directory):
            print "!Failed to create database " + directory + " because it already exists."
        else:
            #creating specified database
            os.makedirs(directory)
            print "Database " + directory + " created."
    except IndexError:
            print "The database name that you enter is not found at the moment. Please try again!"

"""
The second implement function for this project is dropDB which stands for drop
database and throws away what the user has created a specific database and looks for
errors
"""
def dropDB(db):
    #User deletes the database directory that it doesn't want or there isn't any directory that has been existed
    try:
        #This allows us to store the string after the phrase "DROP DATABASE"
        directory = db.split("DROP DATABASE ")[1] #We are using the split function that allows us to split the string into a list
        #This step is to ensure that the specified database exists
        if os.path.exists(directory):
             #Delete an entire directory tree; path must point to a directory.
             rmtree(directory)
             print "Database " + directory + " deleted."
        else:
             #Print the statement for the user to see if the database has been deleted
             print "!Failed to delete database " + directory + " because it does not exist."
    except IndexError:
        print "The database name that you enter is not found at the moment. Please try again!"

"""
The third implement function for this project is createTB which stands for
creation table and creates a specific table for the users and looks for errors
"""
def createTB(db): #db stands for database and TB stands for table database
    try: #Allows us to test a block of code for errors of the changed alter table function
        #Making sure we are in the right directory
        rightDB()
        #This allows us to acquire the string once the table has been createDB
        directory2 = db.split("CREATE TABLE ")[1] #Using the split function that allows us to split the string into a list
        #Makes the string lower case letters
        directory2 = directory2.split(" (")[0].lower()
        position_file = os.path.join(workDir, directory2)
        if not os.path.isfile(position_file): #Checks wheather the specified path is an exsiting regular file
            #Creates a table by using the existing file as a table
            with open(position_file, "w") as table:
                print "Table " + directory2 + " created."
                #start the argument
                if "(" in db: #This is for the expected output after entering the command lines from .sq files
                    #We create a list to the file by loading and sending it
                    list = []
                    #Delete (
                    database = db.split("(",1)[1]
                    #Delete )
                    database = database[:-1]
                    #Replace "," with "|" for expected output for this project
                    database = database.replace(", " , " | ")
                    #Rewrites the database specific for the user to recreate for the table that the user created already
                    table.write(database)
        else:
            #Print the error messagae that the table has been created
            raise ValueError("!Failed to create table " + directory2 + " because it already exists.")
    except IndexError:  #This means that my code is trying to access an index that is invalid and hnadles the error
        print "!Failed to remove table because no table name is specified"
    except ValueError as error: #If the code has an error then it will print the argument statement
        print error.args[0]

"""
The fourth implement function for this project is dropTB which stands for
deletion table and its primary function is to drop a specific table for the
users and looks for errors in case the user is doing something that helps with
this function
"""
def dropTB(db): #db stands for database and TB stands for table database
    try: #Allows us to test a block of code for errors of the changed alter table function
        #Making sure we are in the right directory
        rightDB()
        #This allows us to acquire the string once the table has been dropped
        directory2 = db.split("DROP TABLE ")[1]
        #Find a table that the user has created
        table_user = os.path.join(workDir, directory2)
        #checking if table is correct
        if os.path.isfile(table_user):  #Checks whetheer the specified path is an exsiting regular file
            #Removing the table for the user
            os.remove(table_user)
            print "Table " + directory2 + " deleted."
        else:
            #Print the error messagae that the table has been deleted
            raise ValueError("!Failed to delete table " + directory2 + " because it does not exist.")
    except IndexError:
        print "!Failed to remove table because no table name specified"
    except ValueError as error:
        print error.args[0]


"""
The fifth implement function for this project is alterTB which stands for
alter table and its primary function is change the user specific table and
looks error if there is any. This is consider as update table as functionality
for this project since we want to make change for the user to see that it works
"""
def alterTB(db):
    try: #Allows us to test a block of code for errors of the changed alter table function
        #Making sure we are in the right directory
        rightDB()
        #This allows us to acquire the string once the table has been changed
        table_user= db.split("ALTER TABLE ")[1]
        table_user = table_user.split(" ")[0]
        user_file = os.path.join(workDir, table_user)
        if os.path.isfile(user_file): #Checks whether the specified path is an exsiting regular file
            #Looking for the string "ADD"
            if "ADD" in db:
                #The string "a" will be combine to the end of the file
                with open(user_file, "a") as table:
                    change_string = db.split("ADD ")[1]
                    #Writing the new database for the table as instructor in this project
                    table.write(", " + change_string)
                    print "Table " + table_user + " modified."
        else:
            #Print the error messagae that the table has been deleted
            raise ValueError("!Failed to alter table " + table_user + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print "!Failed to remove table because no table name specified"
    except ValueError as error:  #If the code has an error then it will print the argument statement
        print error.args[0]


"""
The sixth implement function for this project is selectStarSymbol and its primary
function is to query the user specific table and looks error if there is any
"""
def selectStarSymbol(db):
    try: #Allows us to test a block of code for errors of all the table function
        #Making sure we are in the right directory
        rightDB()
        #This allows us to combine the user specific table to see what it looks like
        find_table = db.split("FROM ")[1]
        #The user table
        table_file = os.path.join(workDir, find_table)
        #if table file exists
        if os.path.isfile(table_file): #Checks whetheer the specified path is an exsiting regular file
            #Open the user table file and print out all the statement that has been modified
            with open(table_file,"r+") as table:
                modified_output = table.read()
                print modified_output
        else:
            #Print the error messagae that the table has been deleted
            raise ValueError("!Failed to query table " + find_table + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and hnadles the error
        print "!Failed to remove table because no table name specified"
    except ValueError as error:  #If the code has an error then it will print the argument statement
        print error.args[0]

"""
The seventh implement function for this project is useDB which stands for use
database and its primary function is to use the user specific database and looks
for error if there is any
"""
def useDB(db):
    try:
        global sourceDir
        #Using the database for the useDB
        sourceDir = db.split("USE ")[1]
        if os.path.exists(sourceDir): #Checks whetheer the specified path is an exsiting regular file
            #Print the statement for the use database
            print "Using database " + sourceDir + " ."
        else:
            #Print the error message that the table has been deleted
            raise ValueError("!Failed to use database because it does not exist.")
    except IndexError:
        print "!No database name specified"
    except ValueError:
        print error.args[0]

"""
The eighth implement function for this project is rightDB and its primary
unction is to make sure we are in the right directory
"""
def rightDB():
    if sourceDir is "":
        raise ValueError("!No database selected")
    else: #Checks if this is the right directory if not then fix the directory so it will be the same dirctory as the user instructed
        global workDir
        workDir = os.path.join(os.getcwd(), sourceDir) #Path of the file/table directory

"""
The ninth implement function for this project is the main function to summarize
all the function require for this project
"""
def main():
    try:
        #Instructions for each function that we implement for this project
        print "\n"
        while True:
            command = ""

            #Instructions tells us not to parse the command lines starting with --
            while not ";" in command and not "--" in command:
                command += raw_input() #We used the function raw_input to get the values from the user and signals the program to stop and wait for the user input the values for .sql files that was prvoided for us

            #We are going to follow the test file for the parsing command as instructed for this project
            command = command.split(";")[0]
            command_string= str(command) #Takes the string of the parse command lines
            command_string= command_string.upper() #Making the parse command line to be upper case letters

            #Pass the parse line that starts with --
            if "--" in command:
                pass #Null statement meaning that we don't read it at all
            #Call the function createDB if user has input CREATE DATABASE
            elif "CREATE DATABASE" in command_string:
                createDB(command)
            #Call the function dropDB if user has input DROP DATABASE
            elif "DROP DATABASE" in command_string:
                dropDB(command)
            #Call the function createTB if user has input CREATE TABLE
            elif "CREATE TABLE" in command_string:
                createTB(command)
            #Call the function dropTB if user has input DROP TABLE
            elif "DROP TABLE" in command_string:
                dropTB(command)
            #Call the function alterTB if user has input ALTER TABLE
            elif "ALTER TABLE" in command_string:
                alterTB(command)
            #Call the function selectStarSymbol if user has input SELECT *
            elif "SELECT *" in command_string:
                selectStarSymbol(command)
            #Call the function useDB if user has input USE
            elif "USE" in command_string:
                useDB(command)
            #If user has input .EXIT
            elif ".EXIT" in command_string:
                print "All done."
                exit() #exit the while loop since it is false
    except (EOFError, KeyboardInterrupt) as e:
        print "All done.\n"
        exit()

if __name__ == '__main__':
    main()
