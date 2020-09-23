import socket
import sqlite3
from sqlite3 import Error

#Create connection with database fie and return conn if it could connect or an Error
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file) #sqlite3 connect to database
        return conn
    except:
        print ('Error with connection.') #return error if connection fail

#General function to create table via sqlite3, or return error if table can't be execute or cursor can't be created
def create_table (conn,create_sql_table):
    try:
        c = conn.cursor()
        c.execute (create_sql_table) #query to create table
    except Error as e: #return error if query fail
        print (e)

#Create table storedocuments and storagelocation
def main():
    #This link is my local folder location for database file for connection
    database = r"C:\Users\myht6\OneDrive\Desktop\Adventure\Graduate program\Advanced Programming With Python\Assignment\doc_management.db" 
    #Table storedocuments create query with 5 columns
    create_storedocuments = """ CREATE TABLE IF NOT EXISTS storedocuments
                                (storage_id interger PRIMARY KEY,
                                creation_date date,
                                file_name text,
                                file_extension text,
                                calling_link)"""
    #Table storagelocation create query with 2 columns
    create_storagelocation = """CREATE TABLE IF NOT EXISTS storagelocation
                                (storage_id interger,
                                storage_description text)"""
    conn = create_connection(database) #create connection with the database
    if conn is not None: #call create_table function to create those 2 tables or else return an Error that table can't be created
        create_table (conn, create_storedocuments)
        create_table (conn, create_storagelocation)
    else:
        print ('Error, can not create database connection') #return error if creation fail

#create function to insert value to storedocuments table and return cur.lastrowid to make sure the code have put change to the right amount of recordings       
def insert_storedocuments(conn, task):
    sql = """INSERT INTO storedocuments(storage_id,creation_date, file_name, file_extension, calling_link)
            VALUES (?, ?, ?, ?, ?)"""
    cur = conn.cursor() 
    cur.execute (sql, task) 
    return cur.lastrowid # check if the update is correct with any miss update or duplication

#create function to insert value to storagelocation table and return cur.lastrowid to make sure the code have put change to the right amount of recordings   
def insert_storagelocation(conn, task1):
    sql1 = """INSERT INTO storagelocation(storage_id, storage_description)
            VALUES (?, ?)"""
    cur = conn.cursor()
    cur.execute (sql1, task1)
    return cur.lastrowid # check if the update is correct with any miss update or duplication

#Data value to be insert into tables
def value():
    database = r"C:\Users\myht6\OneDrive\Desktop\Adventure\Graduate program\Advanced Programming With Python\Assignment\doc_management.db"
    conn = create_connection (database)
    with conn:
        value1 = (1, '01/20/2020', 'Quotation 2020', 'xlsx', 'https://drive.google.com/file/d/1Z75CROr8W3Bkn_JXQ90ILcMUUQCYzfGx/view?usp=sharing')
        value2 = (2, '03/19/2020', 'SOP 2020', 'docx', 'https://drive.google.com/file/d/1V_2XU7gUrI-mzHpogynkczzXqXRMGeh8/view?usp=sharing')
        value3 = (3, '01/21/2020', 'IOP 2020', 'docx', 'https://drive.google.com/file/d/17Ys00KgImcKuamOZtOIdVSPi4N7BoteQ/view?usp=sharing')
        insert_storedocuments(conn, value1) #insert value 1, 2, 3 to table storeducements
        insert_storedocuments(conn, value2)
        insert_storedocuments(conn, value3)
        value4 = (1, 'onedrive')
        value5 = (2, 'onedrive')
        value6 = (3, 'onedrive')
        insert_storagelocation(conn, value4) #insert value 1, 2, 3 to table storagelocation
        insert_storagelocation(conn, value5)
        insert_storagelocation(conn, value6)

#Connect to my Onedrive server via port 80
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysocket.connect(('drive.google.com',80))

#End user input storage ID number of their expected file or file name they want to retrieve
id = input ('File ID: ')
name = input ('File name: ')

#Create object to call file from Onedrive and show that file overview data information
class request:
    x=0
    def __init__(self, fileid, filename):
        self.id = fileid
        self.name = filename

    #join data from table storedocuments and storagelocation to show file overview infor along with file content when enduser call that file
    def join_table (self):
        database = r"C:\Users\myht6\OneDrive\Desktop\Adventure\Graduate program\Advanced Programming With Python\Assignment\doc_management.db"
        conn = create_connection (database)
        cur = conn.cursor()
        cur.execute("""SELECT d.creation_date, d.file_name, d.file_extension, l.storage_description
                    FROM storedocuments AS d INNER JOIN storagelocation AS l
                    ON d.storage_id = l.storage_id
                    WHERE d.storage_id = ? OR file_name = ?""", (self.id, self.name,))
        join = cur.fetchall() 
        for row in join:
            print(row)

    # This function take file input id nummber to retrieve file Onedrive links in the same table of storedocuments
    # Then it assign the link to data query with variable send and send data to Onedrive server to retrieve file data content
    def storage_id(self):
        database = r"C:\Users\myht6\OneDrive\Desktop\Adventure\Graduate program\Advanced Programming With Python\Assignment\doc_management.db"
        conn = create_connection (database)
        cur = conn.cursor()
        url = cur.execute('SELECT calling_link from storedocuments where storage_id = ?', (self.id,)) #retrive Onedrive link from database that meet with condition of storage_id provided by enduser
        url = str(url) #to assignn data string to send variable, url must be change to string to combine with other strings
        send = 'GET'+ url + 'HTTP/1.0\r\n\r\n' #data to send to Onedriver server
        mysocket.sendall(send.encode()) # send data to server
        while True:
            data = mysocket.recv(512) 
            if len(data)<1: break
            print(data.decode(), end = '') #recieve, decode data content object and print it

    # This function take file name input to retrieve file Onedrive links in the same table of storedocuments
    # Then it assign the link to data query with variable send and send data to Onedrive server to retrieve file data content
    def file_name(self):
        database = r"C:\Users\myht6\OneDrive\Desktop\Adventure\Graduate program\Advanced Programming With Python\Assignment\doc_management.db"
        conn = create_connection (database)
        cur = conn.cursor()
        url = cur.execute('SELECT calling_link from storedocuments where file_name = ?', (self.name,)) #retrive Onedrive link from database that meet with condition of file name provided by enduser
        url = str(url)  #to assignn data string to send variable, url must be change to string to combine with other strings
        send = 'GET'+ url + 'HTTP/1.0\r\n\r\n' #data to send to Onedriver server
        mysocket.sendall(send.encode()) # send data to server
        while True:
            data = mysocket.recv(512)
            if len(data)<1: break
            print(data.decode(), end = '') #recieve, decode data content object and print it

#assign object request. id will be taken from enduser input id, name will be taken from enduser input name          
a = request(id, name)
#Show file overview information which include creation_date, file_name, file_extension from storedocuments table , and storage_description from storagelocation table
#I excluded storage_id colummn because I believe if is not neccessary but in cass of need we can always add it too
a.join_table()
#For this example, I only call a file name to retrieve its content from Onedrive but we always can 
#programming with loop condition so that enduser can proactively add 1 or more searching options to retrieve as many files at the same time as they want
#a.storage_id()
a.file_name()
mysocket.close()
