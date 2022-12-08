#!/bin/env python3
import pymysql.cursors
import settings
import cgitb
import cgi
import sys
cgitb.enable()

# Make the connection
dbConnection = pymysql.connect(settings.DBHOST,
                                        settings.DBUSER,
                                        settings.DBPASSWD,
                                        settings.DBDATABASE,
                                        charset='utf8mb4',
                                        cursorclass= pymysql.cursors.DictCursor)


fs = cgi.FieldStorage()
quoteVal = fs["quoteValue"].value

sql = "addQuote"
# http headers
print ('Content-type: text/html')
print ()

# Run query and get result

try:
        cursor = dbConnection.cursor()
        cursor.execute("call addQuote(\""+quoteVal+"\")")
        dbConnection.commit()

except pymysql.MySQLError as e:
        print('<p>Ooops - Things messed up: </p>')
except Exception as e:
        print('<p>Something big went wrong.</p>')
        print(e)

cursor.close()
dbConnection.close()

#End