import dropbox
from contextlib import closing
import openpyxl
import pymysql
import os
import io
from tkinter import *
from tkinter import messagebox
import logging
import datetime

logging.basicConfig(filename='errors.log', level=logging.INFO)

# Dropbox
oath2 = "redacted"
po_folder = '/ADCo Team Folder/Operations - ALL/Montgomery/Luc File/Inventory/PURCHASE ORDERS'
inv_folder = '/ADCo Team Folder/Operations - ALL/Montgomery/Luc File/Inventory/MONTHLY INVENTORIES'

def Dropbox_Excel_Download(file_folder, file):
    dbx = dropbox.Dropbox(oath2)
    try:
        metadata, res = dbx.files_download(file_folder + file)

        with closing(res) as result:
            byte_data = res.content
            file_stream = io.BytesIO(byte_data)

        workbook = openpyxl.load_workbook(file_stream)
        temp_folder = os.getcwd() + "/temp_files"
        temp_file = temp_folder + "/temp_po.xlsx"
        workbook.save(temp_file)
        os.system('start EXCEL.EXE ' + temp_file)
    except Exception as e:
        messagebox.showerror("Dropbox Error", "There was an error connecting " +
                             " to Dropbox. \n" +
                             "You can manually open this file by going to " +
                             "Dropbox and looking for the file within " +
                             file_folder)
        logging.info(str(datetime.datetime.now()))
        logging.info(str(e) + '\n')


def Dropbox_Excel_Upload(file_folder, temp_file, file_name):
    dbx = dropbox.Dropbox(oath2)
    try:
        file_to = file_folder + "/" + file_name
        with open(str(temp_file), 'rb') as f:
            dbx.files_upload(f.read(), file_to,
                             mode=dropbox.files.WriteMode.overwrite)
    except Exception as e:
        messagebox.showerror("Dropbox Error", "There was an error connecting " +
                             " to Dropbox. \n" +
                             "You can manually open this file by going to " +
                             "Dropbox and looking for the file within " +
                             file_folder)
        logging.info(str(datetime.datetime.now()))
        logging.info(str(e) + '\n')


# AWS RDS
host="redacted"
port="redacted"
dbname="redacted"
user="redacted"
password="redacted"
ssl_path = "redacted"
ssl = "redacted"

class db_info():
    # Used to store database query information
    def __init__(self):
        self.data = []
        self.columns = []

def db_conn():
    try:
        return pymysql.connect(db=dbname, host=host, port=port, user=user,
                               password=password, ssl=ssl)
    except Exception as e:
        messagebox.showerror("Database Connection Error",
                             "There was an error connecting to the database. " +
                             "Please check your internet connection and try " +
                             "again.")
        logging.info(str(datetime.datetime.now()))
        logging.info(str(e) + '\n')

def db_exec(conn, query, get=True, *args):
    args = tuple(args)
    try:
        cur = conn.cursor()
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        if get == True: # Return queried values
            info = db_info()
            info.columns = [x[0] for x in cur.description]
            info.data = [x for x in cur.fetchall()]
            return info
        else:   # Commit changes made by query
            conn.commit()
    except Exception as e:
        messagebox.showerror("Database Connection Error",
                             "There was an error connecting to the database. " +
                             "Please check your internet connection and try " +
                             "again.")
        logging.info(str(datetime.datetime.now()))
        logging.info(str(e) + '\n')
    finally:
        cur.close()
        conn.close()
