#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import pymysql.cursors
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql
import ssl #include ssl libraries

import cgitb
import cgi
import sys
cgitb.enable()

import settings # Our server and db settings, stored in settings.py

app = Flask(__name__)

# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST

Session(app)



####################################################################################
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

@app.errorhandler(403) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Unauthorized" } ), 403)

####################################################################################
#
# Static Endpoints for humans
#
class Root(Resource):
   # get method. What might others be aptly named? (hint: post)
	def get(self):
		return app.send_static_file('index.html')

def get_user_by_id(id):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getUserById'
		cursor = dbConnection.cursor()
		sqlArgs = (id,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		row = cursor.fetchone() # get the single result
		if row is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return row

def get_user_by_email(email):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getUserByEmail'
		cursor = dbConnection.cursor()
		sqlArgs = (email,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		row = cursor.fetchone() # get the single result
		if row is None:
			return None
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return row

def get_presentlist_by_id(pl_id):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getPresentListById'
		cursor = dbConnection.cursor()
		sqlArgs = (pl_id,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		row = cursor.fetchone()
		if row is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return row 

def get_presentlists_by_email(email):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getPresentListByUserEmail'
		cursor = dbConnection.cursor()
		sqlArgs = (email,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		results = cursor.fetchall()
		if results is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return results 

def get_presents_by_presentListId(id):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getPresentsByPresentList'
		cursor = dbConnection.cursor()
		sqlArgs = (id,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		results = cursor.fetchall()
		if results is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return results 

def get_present_by_id(p_id):
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getPresentById'
		cursor = dbConnection.cursor()
		sqlArgs = (p_id,)
		cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
		row = cursor.fetchone() # get the single result
		if row is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return row # successful

@app.route("/getPresentsByList/<int:id>", methods=["GET"])
def get_presents_by_presentList(id):
	#curl -i -c cookie-jar http://cs3103.cs.unb.ca:5318/getPresentsByList/{id}
	presentLists = json.loads(json.dumps(get_presents_by_presentListId(id)))
	return make_response(jsonify(presentLists), 200) # successful

@app.route("/users", methods=["GET"])
def get_users():
	#curl -i http://cs3103.cs.unb.ca:29145/users
	try:
		dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
		sql = 'getUsers'
		cursor = dbConnection.cursor()
		cursor.callproc(sql) # stored procedure, no arguments
		results = cursor.fetchall()
		if results is None:
			abort(404)
	except:
		abort(500) # Nondescript server error
	finally:
		cursor.close()
		dbConnection.close()
	return make_response(jsonify(results), 200) # successful

class Auth(Resource):
	# Login, start a session and set/return a session cookie
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "cr*ap"}' -c cookie-jar http://cs3103.cs.unb.ca:61340/signin
	def post(self):
		if not request.json:
			abort(400) # bad request
		# Parse the json
		parser = reqparse.RequestParser()
		try:
			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		# Already logged in
		if request_params['username']+"@unb.ca" in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				session['email'] = request_params['username']+"@unb.ca"
				response = {'status': 'success' }
				responseCode = 201
			except (LDAPException, error_message):
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check for a login
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	http://info3103.cs.unb.ca:61340/signin
	def get(self):
		if 'username' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Logout: remove session
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	http://info3103.cs.unb.ca:61340/signin

	def delete(self):
		if 'email' in session:
			session.pop('email', None)
			response = {'status': 'sign out success'}
		else:
			response = {'status': 'no active session'}
		responseCode = 200
		return make_response(jsonify(response), responseCode)

class User(Resource):
	def post(self, userInfo):
        #curl -i -X POST -H "Content-Type: application/json" -d '{"userName": "user2", "userEmail": "user2@fake.com"}' http://cs3103.cs.unb.ca:5318/user/user2@fake.com
			if 'email' not in session:
				abort(403)
			if not request.json or not 'userEmail' in request.json:
				abort(400) # bad request

			userName = request.json['userName']
			userEmail = request.json['userEmail']

			try:
				dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
				sql = 'createUsers'
				cursor = dbConnection.cursor()
				sqlArgs = (userName, userEmail) # Must be a collection
				cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
				dbConnection.commit() # database was modified, commit the changes
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
			return make_response(jsonify(json.loads(json.dumps(get_user_by_email(userInfo)))), 201) # successful resource creation

	def get(self, userInfo):
		#curl -i http://cs3103.cs.unb.ca:5318/user/1
		#curl -i http://cs3103.cs.unb.ca:5318/user/rnitz@fake.com
		if(type(userInfo) == int):
			row = get_user_by_id(userInfo)
		if(type(userInfo) == str):
			row = get_user_by_email(userInfo)
		if(row is None):
			abort(404)
		user = json.loads(json.dumps(row))
		return make_response(jsonify(user), 200) # successful
	

	def put(self, userInfo):
        #curl -i -X PUT -H "Content-Type: application/json" -d '{"userName": "user2-updated", "userEmail": "user2@fake.com"}' http://cs3103.cs.unb.ca:5318/user/user2@fake.com
		#curl -i -X PUT -H "Content-Type: application/json" -d '{"userName": "user1-updated", "userEmail": "user2@fake.com"}' http://cs3103.cs.unb.ca:5318/user/user2@fake.com

		if 'email' not in session:
				abort(403)
		if not request.json or not 'userName' in request.json:
			abort(400) # bad request

		userEmail = userInfo
		if(type(userInfo) == int):
			userEmail = request.json['userEmail']

		userName = request.json['userName']

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userName, userInfo) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify(json.loads(json.dumps(get_user_by_email(userInfo)))), 201) # successful resource creation

	#Don't call this in prod. No ACTUAL use for it. Just don't.
	#Not working the way it should
	def delete(self, userInfo):
		#curl -i -X DELETE http://cs3103.cs.unb.ca:5318/user/3
        #curl -i -X DELETE http://cs3103.cs.unb.ca:5318/user/user2@fake.com

		#Still not wokring??
		# if 'email' not in session:
		# 	abort(403)
		
		if(type(userInfo) == int):
			try:
				jsonStr = json.dumps(get_user_by_id(userInfo))
				userEmail = jsonStr['userEmail']
			except:
				abort(404)
		if(type(userInfo) == str):
			userEmail = userInfo

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userEmail,) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		session.pop('email', None)
		return make_response(jsonify( { "status" : "Successfully deleted user" } ), 200) # successful resource creation

class PresentList(Resource):
	def post(self):
        #curl -i -X POST -H "Content-Type: application/json" -d '{"presentListName": "TestList", "presentListDesc": "TestList for testing", "userEmail":"user2@fake.com"}' http://cs3103.cs.unb.ca:29145/presentlist
			
			if 'email' not in session:
				abort(403)
			if not request.json or not 'presentListName' in request.json:
				abort(400) # bad request

			presentListName = request.json['presentListName']
			presentListDesc = request.json['presentListDesc']
			userEmail = request.json['userEmail']

			try:
				dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
				sql = 'createPresentList'
				cursor = dbConnection.cursor()
				sqlArgs = (presentListName, presentListDesc, userEmail) # Must be a collection
				cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
				row = cursor.fetchone()
				dbConnection.commit() # database was modified, commit the changes
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
			return make_response(jsonify(json.loads(json.dumps(get_presentlist_by_id(row['LAST_INSERT_ID()'])))), 201) # successful resource creation

	def put(self):
		#curl -i -X PUT -H "Content-Type: application/json" -d '{"presentListId":3,"presentListName": "TestList-updated", "presentListDesc": "TestList for testing - updated", "userEmail":"user2@fake.com"}' http://cs3103.cs.unb.ca:5318/presentlist
		if not request.json or not 'presentListId' in request.json:
			abort(400) # bad request

		presentListId = request.json['presentListId']
		presentListName = request.json['presentListName']
		presentListDesc = request.json['presentListDesc']
		userEmail = request.json['userEmail']

		if session['email'] != userEmail:
			abort(403)

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'updatePresentList'
			cursor = dbConnection.cursor()
			sqlArgs = (presentListId, presentListName, presentListDesc, userEmail) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify(json.loads(json.dumps(get_presentlist_by_id(presentListId)))), 200) # successful resource creation

	def get(self, id):	
		#curl -i http://cs3103.cs.unb.ca:5318/presentlist/5
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'getPresentListById'
			cursor = dbConnection.cursor()
			sqlArgs = (id,)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			row = cursor.fetchone() # get the single result
			if row is None:
				abort(404)
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify(row), 200) # successful

	def delete(self, id):
		#curl -i -X DELETE -c cookie-jar http://cs3103.cs.unb.ca:5318/presentlist/5
		if 'email' not in session:
			abort(403)

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'deletePresentList'
			cursor = dbConnection.cursor()
			sqlArgs = (id,) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify( { "status" : "Successfully deleted presentlist" } ), 200) # successful resource creation
		
class PresentLists(Resource):
	#curl -i -c cookie-jar http://cs3103.cs.unb.ca:5318/presentlists/user2@fake.com
	def get(self, userEmail):
		presentLists = json.loads(json.dumps(get_presentlists_by_email(userEmail)))
		return make_response(jsonify(presentLists), 200) # successful

class Present(Resource):
	#curl -i -c cookie-jar http://cs3103.cs.unb.ca:5318/present/1
	def get(self, id):
		result = get_present_by_id(id)
		return make_response(jsonify(result), 200) # successful

	def post(self):
		#curl -i -X POST -H "Content-Type: application/json" -b cookie-jar -d '{"presentName": "TestList", "presentDesc": "TestList for testing", "presentPrice": "10.20", "presentListId": 31, "userEmail": "rnitz@unb.ca"}' http://cs3103.cs.unb.ca:29145/present
			if 'email' not in session:
				abort(403)
			if not request.json or not 'presentName' in request.json:
				abort(400) # bad request

			presentName = request.json['presentName']
			presentDesc = request.json['presentDesc']
			presentPrice = request.json['presentPrice']
			presentListId = request.json['presentListId']
			userEmail = request.json['userEmail']

			try:
				dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
				sql = 'createPresent'
				cursor = dbConnection.cursor()
				sqlArgs = (presentName, presentDesc, presentPrice, presentListId, userEmail) # Must be a collection
				cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
				dbConnection.commit() # database was modified, commit the changes
			except:
				abort(500) # Nondescript server error
			finally:
				cursor.close()
				dbConnection.close()
			return make_response(jsonify(json.loads(json.dumps(get_presents_by_presentListId(presentListId)))), 201) # successful resource creation
	def put(self):
		#curl -i -X PUT -H "Content-Type: application/json"  -b cookie-jar -d '{"presentId":7, "presentName": "TestPresent", "presentDesc": "TestPresent for testing", "presentPrice": "101.20", "presentListId": 31, "userEmail": "rnitz@unb.ca"}' http://cs3103.cs.unb.ca:5318/present
		if not request.json or not 'presentId' in request.json:
			abort(400) # bad request
		if 'email' not in session:
			abort(403)
		presentId = request.json['presentId']
		presentName = request.json['presentName']
		presentDesc = request.json['presentDesc']
		presentPrice = request.json['presentPrice']
		presentListId = request.json['presentListId']
		userEmail = request.json['userEmail']

		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'updatePresent'
			cursor = dbConnection.cursor()
			sqlArgs = (presentId, presentName, presentDesc, presentPrice, userEmail) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify(json.loads(json.dumps(get_presents_by_presentListId(presentListId)))), 200) # successful resource creation
	def delete(self, id):
		#curl -i -X DELETE -c cookie-jar http://cs3103.cs.unb.ca:5318/present/7

		if 'email' not in session:
			abort(403)
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,settings.DB_USER,settings.DB_PASSWD,settings.DB_DATABASE,charset='utf8mb4',cursorclass= pymysql.cursors.DictCursor)
			sql = 'deletePresent'
			cursor = dbConnection.cursor()
			sqlArgs = (id,) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify( { "status" : "Successfully deleted presentlist" } ), 200) # successful resource creation

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Root,'/')
api.add_resource(Auth, '/auth')
api.add_resource(User, '/user/<int:userInfo>', '/user/<string:userInfo>')
api.add_resource(PresentList, '/presentlist', '/presentlist/<int:id>')
api.add_resource(PresentLists, '/presentlists/<string:userEmail>')
api.add_resource(Present, '/present','/present/<int:id>')
#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
