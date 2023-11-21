"""
Author: Jared Lam
Date: 11/30/2021
Project 4: Transactions
Class: CS 457
"""
#Using python 2 version since it compatible with my program. It can also work 3.10 version
#Interact with the file system
import os, re #Provides regular expression mathcing operations that are found the same in Perl
from contextlib import contextmanager #This allows requires for opening multiple multiple_file
"""
This Project 4 is hard and I couldn't print output of some of it I discuss this
in my documentation. I try my best to figure the flow of my code but I couldn't
figure it out the time I have
"""
"""
The first implement function for this project is the main function to
summarize all the function require for this project
"""
def main():
    #This is where the database location to interact with the directory for this project
    globalsourceDir = ""
    workDir = ""
    lock = ["table"]
    flagLock = 0
    index = 1

    try:
        #Making sure that it is available to create for a file if it doesn't exist
        if not os.path.exists("./locks"):
            os.makedirs("./locks")

        while True:
            command = ""

            #Printing lock and flagLock
            if flagLock is 1:
                if index is not len(lock):
                    command = lock[index]
                    index += 1
                else:
                    removeLock = "./locks/" + lock[0]
                    if os.path.isfile(removeLock):
                        os.remove(removeLock)
                    lock = ["table"]
                    index = 1
                    flagLock = 0

            if flagLock is not 1:
                #Instructions tells us not to parse the command lines starting with --index
                while not ";" in command and not "--" in command:
                    #Using the string method strip allows remove spaces at the beginning and at the end of the string
                    command += raw_input().strip('\r')  #We used the function raw_input to get the values from the user and signals the program to stop and wait for the user input the values for .sql multiple_file that was prvoided for us
                command = command.split(";")[0]  #We are getting rid of ; from the command


            command_string = str(command) #Takes the string of the parse command lines
            command_string = command_string.upper() #Making the parse command line to be upper case letters

            #print command_string

            #Pass the parse line that starts with --
            if "--" in command:
                pass #Null statement meaning that we don't read it at all
            #Call the function alterTable if user has input ALTER TABLE
            elif "ALTER TABLE" in command_string:
                alterTable(command)
            #Call the function transactionLock if the user has input BEGIN TRANSACTION
            elif "BEGIN TRANSACTION" in command_string:
                lock, flagLock = transactionLock(lock, flagLock)
            #Call the function createDB if user has input CREATE DATABASE
            elif "CREATE DATABASE" in command_string:
                createDB(command)
            #Call the function createTable if user has input CREATE TABLE
            elif "CREATE TABLE" in command_string:
                createTable(command)
            #Call the function deleteFrom if the user has input DELETE FROM
            elif "DELETE FROM" in command_string:
                deleteFrom(command)
            #Call the function dropDB if user has input DROP DATABASE
            elif "DROP DATABASE" in command_string:
                dropDB(command)
            #Call the function dropTable if user has input DROP TABLE
            elif "DROP TABLE" in command_string:
                dropTable(command)
            #Call the function insertInto if the user has input INSERT INTO
            elif "INSERT INTO" in command_string:
                insertInto(command)
            #Call the function select if user has input SELECT
            elif "SELECT" in command_string:
                select(command, command_string)
            #Call the function update if the user has input UPDATE
            elif "UPDATE" in command_string:
                update(command)
            #Call the function useDB if user has input USE
            elif "USE" in command_string:
                useDB(command)
            #If user has input .EXIT
            elif ".EXIT" in command:
                #print the statement when exiting
                print ("All done.")
                exit() #exit the while loop since it is false

    except (EOFError, KeyboardInterrupt) as exit:  #Exit script elegantly
        print ("\n All done.")

"""
The second implement function for this project is multiple_fileManager and its primary
function is to open multiple multiple_file and making sure the file are closed
"""
@contextmanager #This function is a decorator that can be used to define a factory function for with statement context managers, withoutput needing to create a class or separate __enter__() and __exit__() methods.
def fileManager(files, mode='rt'):
    files = [open(file, mode) for file in files]
    yield multiple_file #A generator function is defined like a normal function, but whenever it needs to generate a value, it does so with the yield keyword rather than return
    for file in files:
        file.close()

"""
The third implement function for this project is useEnable and its primary
purpose function is to catch errors when the database isn't enabled. Also they
are main function for this project
"""
def useEnable():  #Catch the error when a database hasn't been enabled
    if globalsourceDir is "":
        raise ValueError("The table database hasn't selected yet. Please try again.")
    else: #Checks if this is the right directory if not then fix the directory so it will be the same directory as the user instructed
        global workDir
        workDir = os.path.join(os.getcwd(), globalsourceDir) #Path of the file/table directory

"""
The fourth implement function for this project is getColumn and they are main
function for this project
"""
def getColumn(data):
    columnIndex = data[0].split(" | ")
    for x in range(len(columnIndex)):
        columnIndex[x] = columnIndex[x].split(" ")[0]
    return columnIndex

"""
The fifth implement function for this project is separateLine and they are main
function for this project
"""
def separateLine(line):
    lineTester = line.split(" | ")
    for x in range(len(lineTester)):  #x represent column and making sure that each column has an entry
        lineTester[x] = lineTester[x].split(" ")[0]
    return lineTester

"""
The sixth implement function for this project is combineJoinWhere and they
are main function for this project. They are in test script that we need to
implement it
"""
def combineJoinWhere(search, table_variables, data, joinType = 'inner'):
    count = 0
    output = []
    flag = 0 #Flag means configuration handles
    number_of_tables = len(data) #len methods is built-in function that can be used to calculate the length of any iterable object
    pairData = []
    columnClear = ""

    #Gather all the data inside of the column and check to see if they have a pairs
    if "=" in search:  #Evaluate operator
        if "!=" in search:
            row_col = search.split(" !=")[0]
        else:
            left = search.split(" =")[0]
            left = left.split(".")[1]
            right = search.split("= ")[1]
            right = right.split(".")[1]
    if number_of_tables == 2:
        table_from_my_left = data[0]
        table_from_my_right = data[1]
    else:
        print "Join can only accept two tableSelect"
        return -1, -1

    left_of_the_data = []
    right_of_the_data = []
    left_of_the_column = getColumn(table_from_my_left[0])
    right_of_the_column = getColumn(table_from_my_right[0])

    for lines in table_from_my_left:
        separate_line = separateLine(lines)
        left_of_the_data.append(separate_line[left_of_the_column.index(left)])
    for line in table_from_my_right:
        separate_line = separateLine(lines)
        right_of_the_data.append(separate_line[right_of_the_column.index(right)])

    #If inner and outer join finds a pair in the data
    for x in range(len(left_of_the_data)): #x represent column
        for y in range(len(right_of_the_data)): #y represent row
            if left_of_the_data[x] == right_of_the_data[y]:
                table_from_my_left[x] = table_from_my_left[x].strip('\n')
                output.append(table_from_my_left[x] + ' | ' + table_from_my_right[y])
                count += 1
                if joinType == 'left':
                    pairData.append(table_from_my_left[x])

    if joinType == 'left':
        number_of_data = len(right_of_the_column)
        for x in range(number_of_data):
            columnClear += ' | '
        for x in range(len(left_of_the_data)):
            #Delete the table key
            if not left_of_the_column[0] in table_from_my_left[x]:
                #Can't run if there is no more pair in the data
                if not table_from_my_left[x] in pairData:
                    output.append(table_from_my_left[x].strip('\n') + columnClear)
                    count += 1
    return count, output

"""
The seventh implement function for this project is whereCommand and they are main
function for this project. They are in test script that we need to implement it
"""
def whereCommand(search, action, data, up_val=""):
    count = 0
    columnIndex = getColumn(data)
    featureName = columnIndex
    inputData = list(data)
    output = []
    flag = 0 #Flag means configuration handles

    #Look at the operator (evaluate)
    if "=" in search:
        if "!=" in search:
            row_col = search.split(" !=")[0]
            flag = 1
        else:
            row_col = search.split(" =")[0]

        search = search.split("= ")[1]
        if "\"" in search or "\'" in search: #Making the variable clearly
            search = search[1:-1]
        for lines in data: #Reading the lines in the test script
            lineTest = separateLine(lines)
            if search in lineTest:
                columnIndex = featureName.index(row_col)
                lineIndex = lineTest.index(search)
                #Making sure we have the right column using the method of checking
                if lineIndex == columnIndex:
                    if action == "delete": #delete from command from test script
                        del inputData[inputData.index(lines)]
                        output = inputData
                        count += 1
                    if action == "select": #select command from test script
                        output.append(inputData[inputData.index(lines)])
                    if action == "update": #update command from test script
                        feature, field = up_val.split(" = ")
                        print (feature, field)
                        if feature in featureName:
                            separate_line = separateLine(lines)
                            separate_line[featureName.index(feature)] = field.strip().strip("'")
                            inputData[inputData.index(lines)] = ' | '.join(separate_line)
                            output = inputData
                            count += 1

    #Look at the operator (evaluate)
    elif ">" in search:
        row_col = search.split(" >")[0]
        search = search.split("> ")[1]
        for lines in data: #looking at the lines in the test script
            lineTest = line.split(" | ")
            for x in range(len(lineTest)):   #x represent column so we can check each items
                lineTest[x] = lineTest[x].split(" ")[0]
                try:
                    #Seeing the numeric values in the test script
                    lineTest[x] = float(lineTest[x])  #Looks for value
                    if lineTest[x] > float(search):
                        temporary_column = columnIndex.index(row_col)
                        if x == temporary_column:
                            if action == "delete": #delete from command from test script
                                #Finds the matching word and gets rid of it
                                del inputData[inputData.index(lines)]
                                output = inputData
                                count += 1
                            if action == "select": #select command from test script
                                output.append(inputData[inputData.index(lines)])
                            if action == "update":
                                print ("It has been updated.")
                except ValueError:
                    continue #goes through a loop again
    if flag:
        output = list(set(data) - set(output))
    return count, output

"""
The eighth implement function for this project is alterTable and its primary
function is change the user specific table and looks error if there is any.
This is consider as update table as functionality for this project since we want
to make change for the user to see that it works
"""
def alterTable(input): #input is user has enter a command line
    try: #Allows us to test a block of code for errors of the changed alter table function
        #Making sure we are in the right directory
        useEnable()
        #This allows us to acquire the string once the table has been changed
        table_name = input.split("ALTER TABLE ")[1]
        table_name = table_name.split(" ")[0].lower()
        name_file = os.path.join(workDir, table_name)
        if os.path.isfile(name_file): #Checks whether the specified path is an existing regular file
            #Looking for the string "ADD" and works for first project
            if "ADD" in input:
                #The string "a" will be combine to the end of the file
                with open(name_file, "a") as table:  # Use A to append data to end of the file
                    change_string = input.split("ADD ")[1]
                    #Writing the new database for the table as instructor in this project
                    table.write(" | " + change_string)
                    print ("Table " + table_name + " modified.")
        else:
            #Print the error messagae that the table has been deleted
            print ("!Failed to alter table " + table_name + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The ninth implement function for this project is transactionLock and they
are main function for this project since the project is based on this topic
"""
def transactionLock(lock, flagLock):
    try:
        name_file = ""
        multiple_file = []
        useEnable()  #Making sure that the database has been selected
        print("Transaction starts.")
        while True:
            command = ""

            while not ";" in command and not "--" in command:
                command += raw_input().strip('\r')  #We used the function raw_input to get the values from the user and signals the program to stop and wait for the user input the values for .sql files that was prvoided for us

            if "commit;" in command: #This means that there is an error and that it can't be changed when someone is using it
                break

            command = command.split(";")[0]  #We are getting rid of ; from the command
            command_string = str(command)  #Conduct the command line
            lock.append(command_string)

            if "UPDATE" in command_string.upper():
                name_table = re.split("UPDATE ", lock[1], flags=re.IGNORECASE)[1]  #Search the updated string to use for name_table
                name_table = re.split("SET", name_table, flags=re.IGNORECASE)[0].lower().strip()
                name_file = name_table + ".lock"
                multiple_file = os.listdir("./locks")
                lock[0] = name_file

                path = "./locks/" + name_file
                f = open(path, "w") #w stand for write inside the file
                f.close()
                flagLock = 1

        if name_file in multiple_file:
            print "Error: Table", name_table, "is locked!" #Print the output of error statement
            print "Transaction abort."
            return ["table"], 0
        return lock, flagLock

    except IndexError:
        print ("The transaction has an error and can't no longer be fixed.")

    except ValueError as error:
        print (error.args[0])

"""
The tenth implement function for this project is createDB which stands for
creation database and it creates a user to specified database and see if there
is any errors or not
"""
def createDB(input): #input is user has enter a command line
    #Creating database if it doesn't exist in the system
    try: #Allows us to test a block of code for errors of the creation database function
        #This allows us to store the string after the phrase "CREATE DATABASE"
        directory = input.split("CREATE DATABASE ")[1]  #We are using the split function that allows us to split the string into a list
        #Checking to see if this specific database exist or not
        if not os.path.exists(directory):
            #We are going to created a database directory
            os.makedirs(directory)
            #Print the statement to show that the database directory has been created
            print ("Database " + directory + " created.")
        else:
            #Print the statement for the user to see if the database has been created or not
            print ("!Failed to create database " + directory + " because it already exists.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The database name that you enter is not found at the moment. Please try again!")

"""
The eleventh implement function for this project is createTB which stands for
creation table and creates a specific table for the users and looks for errors
"""
def createTable(input): #input is user has enter a command line
    try: #Allows us to test a block of code for errors of the creation table function
        #Making sure we are in the right directory
        useEnable()
        #This allows us to acquire the string once the table has been createDB
        directory2 = re.split("CREATE TABLE ", input, flags=re.IGNORECASE)[1]  #Using the split function that allows us to split the string into a list
        #Makes the string lower case letters
        directory2 = directory2.split("(")[0].lower()
        name_file = os.path.join(workDir, directory2)
        if not os.path.isfile(name_file): #Checks whether the specified path is an existing regular file
            #Creates a table by using the existing file as a table
            with open(name_file, "w") as table:  # Create a file within folder to act as a table
                print ("Table " + directory2 + " created.")
                #start the argument
                if "(" in input:  #This is for the expected output after entering the command lines from .sql multiple_file
                    #We create a list for the output to a file to demonstrate it
                    output = []
                    #Delete (
                    data = input.split("(", 1)[1]
                    #Delete )
                    data = data[:-1]
                    track = data.count(",")  #how many comma are in test script
                    for x in range(track + 1):
                        #Putting the command_argument to a list for printing output so the user can see
                        output.append(data.split(", ")[x])
                    #Rewrites the database specific for the user to recreate for the table that the user created already
                    table.write(" | ".join(output))
        else:
            #Print the error messagae that the table has been created
            print ("!Failed to create table " + directory2 + " because it already exists.")
    except IndexError:  #This means that my code is trying to access an index that is invalid and hnadles the error
        print ("!Failed to create table because no table name is specified.")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The twelfth implement function for this project is deleteFrom and its primary
function is to delete the record within the table
"""
def deleteFrom(input): #input is user has enter a command line
    try: #Allows us to test a block of code for errors of the changed delete from table function
        #Making sure we are in the right directory
        useEnable()
        #This allows us to acquire the string used in the table name
        table_name = re.split("DELETE FROM ", input, flags=re.IGNORECASE)[1]  #it doesn't matter if it is upper or lower case it will match for this command
        table_name = table_name.split(" ")[0].lower()
        name_file = os.path.join(workDir, table_name)
        if os.path.isfile(name_file): #Checks whether the specified path is an exsiting regular file
            with open(name_file, "r+") as tableRecord:
                read_data = tableRecord.readlines()#readlines returns a list containing each line in the file as a list item
                itemDeletion = re.split("WHERE ", input, flags=re.IGNORECASE)[1] #it doesn't matter if it is upper or lower case it will match for this command
                count, output = whereCommand(itemDeletion, "delete", read_data)
                tableRecord.seek(0) #seek sets the file's current position at the offset
                tableRecord.truncate()
                for lines in output:
                    tableRecord.write(lines) #will write the lines that are getting deleted into another file
                if count > 0:
                    print count, " records deleted."
                else:
                    print "No records have been deleted."
        else:
            #Print the error messagae that the table has been deleted
            raise ValueError("!Failed to delete table " + table_name + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])
"""
The thirteenth implement function for this project is dropDB which stands for drop
database and throws away what the user has created a specific database and looks for
errors
"""
def dropDB(input): #input is user has enter a command line
    #User deletes the database directory that it doesn't want or there isn't any directory that has been existed
    try: #Allows us to test a block of code for errors of the deleteion database function
        #This allows us to store the string after the phrase "DROP DATABASE"
        directory = input.split("DROP DATABASE ")[1]  #We are using the split function that allows us to split the string into a list
        #Checking to see if this specific database exist
        if os.path.exists(directory):
            #To make sure there isn't anything in the folder and we can remove the folder
            for valueRemove in os.listdir(directory):  #listdir returns a list containing the names of the entries in the directory given by path
                os.remove(directory + "/" + valueRemove) #removes it from the list
            os.rmdir(directory) #rmdir uses to remove or delete a empty directory
            #Print the statement to show that the database directory has been deleted
            print ("Database " + directory + " deleted.")
        else:
            #Print the statement for the user to see if the database has been deleted
            print ("!Failed to delete database " + directory + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The database name that you enter is not found at the moment. Please try again!")


"""
The fourteenth implement function for this project is dropTable and its primary
function is to drop a specific table for the users and looks for errors in case
the user is doing something that helps with this function
"""
def dropTable(input): #input is user has enter a command line
    try: #Allows us to test a block of code for errors of the deletion table function
        #Making sure we are in the right directory
        useEnable()  # Check that a database is selected
        #This allows us to acquire the string once the table has been dropped
        directory2 = input.split("DROP TABLE ")[1].lower()  #Using the split function that allows us to split the string into a list
        #Find a table that the user has created
        directory_table = os.path.join(workDir, directory2)
        if os.path.isfile(directory_table): #Checks whether the specified path is an existing regular file
            #Removing the table for the user
            os.remove(directory_table)
            print ("Table " + directory2 + " deleted.")
        else:
            #Print the error messagae that the table has been deleted
            print ("!Failed to delete Table " + directory2 + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The fifteenth implement function for this project is insertInto and its primary
function is to insert a record within the table
"""
def insertInto(input): #input is user has enter a command line
    try: #Allows us to test a block of code for errors of the changed insert into table function
        #To check if the database has been enabled and is selected as well
        useEnable()
        #Find table name
        table_name = input.split(" ")[2].lower()
        name_file = os.path.join(workDir, table_name)
        if os.path.isfile(name_file):
            if "values" in input:
                #Insert it into a open file
                with open(name_file, "a") as tableRecord:
                    output = []  #Making a list into the output file
                    insert_data = input.split("(", 1)[1]  #removing (
                    insert_data = insert_data[:-1]  #removing )
                    track = insert_data.count(",")  #keeping track of the arugment being made
                    for x in range(track + 1):
                        #putting the arument to see the output of it
                        output.append(insert_data.split(",")[x].lstrip())  #Removes any leading characters
                        if "\"" == output[x][0] or "\'" == output[x][0]:
                            output[x] = output[x][1:-1]
                    tableRecord.write("\n")
                    #output the file
                    tableRecord.write(" | ".join(output))
                    print ("1 new record inserted.")
            else:
                print ("!Failed to insert into " + table_name + "because there were no specified arguments for it.")
        else:
            print ("!Failed to insert into " + table_name + " because it does not exist")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The insert into table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The sixteenth implement function for this project is select and its primary
function is to query the user specific table and looks error if there is any
"""
def select(input, inputCommand): #input is user has enter a command line
    try:
        #Making sure we are in the right directory
        useEnable()
        name_table = re.split("FROM ", input, flags=re.IGNORECASE)[1].lower()  #Search a string to use for name_table
        if "WHERE" in inputCommand:
            name_table = re.split("WHERE", name_table, flags=re.IGNORECASE)[0]
            if " " in name_table:
                name_table = name_table.split(" ")[0]
        name_file = os.path.join(workDir, name_table)
        output = ""
        if os.path.isfile(name_file):
            with open(name_file, "r+") as tableSelect:
                if "WHERE" in inputCommand: #Search the keyword "WHERE" for all side_command
                    itemSelection = re.split("WHERE ", input, flags=re.IGNORECASE)[1]
                    select_data = tableSelect.readlines()
                    count, output = whereCommand(itemSelection,"select",select_data)
                    for lines in output:
                        print lines
                if "SELECT *" in inputCommand:
                    if not output == "":  #Checks if the output is allocated
                        for lines in output:
                            print lines
                    else: #If no restriction when WHERE print
                        output = tableSelect.read()
                        print output
                else: #If no feature required just output
                    command_argument = re.split("SELECT", input, flags=re.IGNORECASE)[1]
                    side_command = re.split("FROM", command_argument, flags=re.IGNORECASE)[0]
                    side_command = side_command.split(",")
                    if not output == "":  #Checks if the output is allocated
                        lines = output
                    else:
                        lines = tableSelect.readlines()
                        select_data = lines
                    for line in lines:
                        results = []
                        for feature in side_command:
                            feature = feature.strip() #Removes any leading and trailing characters
                            columnIndex = getColumn(select_data) #Return information in the select data from the column table
                            if feature in columnIndex:
                                new_lines = separateLine(line)
                                results.append(new_lines[columnIndex.index(feature)].strip())
                        print " | ".join(results)
        else:
            print ("!Failed to query table " + table_name + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and hnadles the error
        print ("The select table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error:
        print (error.args[0])

"""
The seventeenth implement function for this project is update and its primary
function is to update the record into the table database
"""
def update(input): #input is user has enter a command line
    try:
        #Making sure we are in the right directory
        useEnable()
        #This allows us to use the table for database
        table_name = re.split("UPDATE ", input, flags=re.IGNORECASE)[1] #it doesn't matter if it is upper or lower case it will match for this command
        table_name = re.split("SET", table_name, flags=re.IGNORECASE)[0].lower().strip()
        name_file = os.path.join(workDir, table_name)
        if os.path.isfile(name_file): #Checks whether the specified path is an existing regular file
            #Since table has been created we will use r+
            with open(name_file, "r+") as updateTable:
                #Find matches within the features
                update_data = updateTable.readlines()
                itemUpdate = re.split("WHERE ", input, flags=re.IGNORECASE)[1]
                value = re.split("SET ", input, flags=re.IGNORECASE)[1]
                value = re.split("WHERE ", value, flags=re.IGNORECASE)[0]
                count, output = whereCommand(itemUpdate, "update", update_data, value)
                updateTable.seek(0)
                updateTable.truncate()
                for lines in output:
                    if not "\n" in lines:
                        lines += "\n"
                    updateTable.write(lines)
                if count > 0:
                    print count, "record modified."
                    print "Transaction committed."
                else:
                    print "No record modified."
        else:
            #Print the error messagae that the table has been deleted
            print ("!Failed to update table " + table_name + " because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and hnadles the error
        print ("The update table database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The eighteenth implement function for this project is useDB which stands for use
database and its primary function is to use the user input and looks
for error if there is any
"""
def useDB(input): #input is user has enter a command line
    try:
        global globalsourceDir
        #Using the database for the useDB when storing the string (working with global scope)
        globalsourceDir = input.split("USE ")[1]
        if os.path.exists(globalsourceDir): #Checks whetheer the specified path is an exsiting regular file
            #Print the statement for the use database
            print ("Using database " + globalsourceDir + ".")
        else:
            #Print the error message that the table has been deleted
            raise ValueError("!Failed to use database because it does not exist.")
    except IndexError: #This means that my code is trying to access an index that is invalid and handles the error
        print ("The database name that you enter is not found at the moment. Please try again!")
    except ValueError as error: #If the code has an error then it will print the argument statement
        print (error.args[0])

"""
The nineteenth implement function for this project is helpSelect and they are
main function for this project since they help select function for table joins
and parsing that focus on inner join, left outer join, and right outer join
"""
def helpSelect(name_file, table, joinType, inputCommand, input):
    table_data = []
    table_search = {}
    name_table = []

#Parsing the table name
    if "JOIN" in inputCommand:
        cut_input = re.split("FROM ", input, flags =re.IGNORECASE)[1]
        #Left table will be [0] no matter what
        if "LEFT" in inputCommand:
            left_table = re.split("LEFT", cut_input, flags=re.IGNORECASE)[0].lower()
            right_table = re.split("JOIN ", cut_input, flags=re.IGNORECASE)[1].lower()
            right_table = re.split("ON", right_table, flags=re.IGNORECASE)[0].strip()
            left_table = re.split(" ", left_table, flags=re.IGNORECASE)[0].strip()
            right_table = re.split(" ", right_table, flags=re.IGNORECASE)[0].strip()
            table_data.append(left_table) #This represent the left table
            table_data.append(right_table) #This represent the right table
            joinType = 'left'

        elif "INNER" in inputCommand:
            left_table = re.split("INNER", cut_input, flags=re.IGNORECASE)[0].lower()
            right_table = re.split("JOIN ", cut_input, flags=re.IGNORECASE)[1].lower()
            right_table = re.split("ON", right_table, flags=re.IGNORECASE)[0].strip()
            left_table = re.split(" ", left_table, flags=re.IGNORECASE)[0].strip()
            right_table = re.split(" ", right_table, flags=re.IGNORECASE)[0].strip()
            table_data.append(left_table) #This represent the left table
            joinType = 'inner'
            table_data.append(right_table) #This represent the right table

        elif "RIGHT" in inputCommand: #Not implemented since we are only focus on inner and left outer join
            table_data = re.split("RIGHT", cut_input, flags=re.IGNORECASE)[0].lower() #This represent the left table
            table_data = re.split("JOIN", cut_input, flags=re.IGNORECASE)[1].lower() #This represent the right table
            joinType = 'right'

    elif "WHERE" in inputCommand:
        name_table = re.split("FROM ", input, flags=re.IGNORECASE)[1].lower()
        name_table = re.split("WHERE", name_table, flags=re.IGNORECASE)[0]

    else: #This is if neither the condition are true
        #Find a string that can be used for name of table
        name_table = re.split("FROM ", input, flags=re.IGNORECASE)[1].lower()
        if "," in name_table:
            for t in re.split(", ", name_table):
                table_data.append(t)
        else:
            table_data.append(name_table)

    if " " in name_table:
        name_table = name_table.strip("\r") #It removes any leftover returns
        name_table = name_table.strip() #Deletes any whitespace

    if "," in name_table:
        for t in re.split(", ", name_table):
            t, tableSelect = re.split(" ", t, flags=re.IGNORECASE) #Gets the left table name
            table_search[tableVariable] = t
            table_data.append(t)
            table.append(tableSelect)

    #Looks for every table name to create each file path
    for nt in table_data: #nt represent name table
        if nt:
            name_file.append(os.path.join(workDir, nt))

    return name_file, table, joinType

if __name__ == '__main__':
	main()
