#!/usr/bin/env python3.6

# Example python script to access a database and return the data as a traditional web page#
import pymysql.cursors
import settings
import cgitb
import cgi
import sys
import json
cgitb.enable()

# Make the connection
dbConnection = pymysql.connect(settings.DBHOST,
                                        settings.DBUSER,
                                        settings.DBPASSWD,
                                        settings.DBDATABASE,
                                        charset='utf8mb4',
                                        cursorclass= pymysql.cursors.DictCursor)


fs = cgi.FieldStorage()
name = fs["name"].value
province = fs["province"].value
language = fs["language"].value
level = fs["level"].value



sql = "createSchool"
# http headers
print ('Content-type: text/json')
print ()

# Run query and get result
try:
        cursor = dbConnection.cursor()
        cursor.callproc(sql,[name,province,language,level]) # stored procedure, with arguments
        row = cursor.fetchone()
        dbConnection.commit() # database was modified, commit the changes
        print(list(row.values())[0])
except pymysql.MySQLError as e:
        print('<p>Ooops - Things messed up: </p>')
except Exception as e:
        print('<p>Something big went wrong.</p>')
        print(e)

cursor.close()
dbConnection.close()

##End