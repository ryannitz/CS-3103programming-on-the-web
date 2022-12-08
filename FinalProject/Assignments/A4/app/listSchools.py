#!/bin/env python3
#
# getSchoolsWeb.py - Rick Wightman, modified September, 2017
#
# Example python script to access a database and return the data as a traditional web page
#
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
province = fs["prov"].value

sql = "getSchoolsByProvince"
# http headers
print ('Content-type: text/json')
print ()

# Run query and get result

try:
        cursor = dbConnection.cursor()
        #cursor.callproc(sql, "NB")
        cursor.execute("call getSchoolsByProvince(\""+province+"\")")
        results = cursor.fetchall()

        print(json.dumps(results))
except pymysql.MySQLError as e:
        print('<p>Ooops - Things messed up: </p>')
except Exception as e:
        print('<p>Something big went wrong.</p>')
        print(e)

cursor.close()
dbConnection.close()

#End