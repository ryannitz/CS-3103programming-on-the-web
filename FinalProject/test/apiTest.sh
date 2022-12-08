#!/bin/bash

#curl -i https://cs3103.cs.unb.ca:$port/auth
# Read username and password
read -r -p "port: " port
read -r -p "username: " username
read -r -s -p "password: " password
email="${username}@unb.ca"

# substitute into the curl command
echo "###########Authenticate User"
lastOutput=$(curl -s -i -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -c cookie-jar http://cs3103.cs.unb.ca:$port/auth)
echo "${lastOutput}"
echo "###########DELETE User"
#delete user (should be last just as clean up on failures. This will clear all pl/presents asociated with the test user).
lastOutput=$(curl -s -i -X DELETE http://cs3103.cs.unb.ca:$port/user/$email)
echo "${lastOutput}"


#
# TEST USER CRUD
#
# Create user
echo "###########Create user"
lastOutput=$(curl -s -i -X POST -b cookie-jar -H "Content-Type: application/json" -d '{"userName": "'$username'", "userEmail": "'$email'"}' http://cs3103.cs.unb.ca:$port/user/$email)
echo "$lastOutput"

#Get user/email
echo "###########Get user"
lastOutput=$(curl -s -i http://cs3103.cs.unb.ca:$port/user/$email)
echo "$lastOutput"

#Get users
echo "###########Get users"
lastOutput=$(curl -s -i http://cs3103.cs.unb.ca:$port/users)
echo "$lastOutput"

#Update user
echo "###########Update user"
lastOutput=$(curl -s -i -X PUT -b cookie-jar -H "Content-Type: application/json" -d '{"userName": "'$username'-updated", "userEmail": "'$email'"}' http://cs3103.cs.unb.ca:$port/user/$email)
echo "$lastOutput"



#
# TEST PRESENTLIST CRUD
#
#create Present List
echo "###########Create Present List"
lastOutput=$(curl -s -i -X POST -b cookie-jar -H "Content-Type: application/json" -d '{"presentListName": "TestList", "presentListDesc": "TestList for testing", "userEmail":"'$email'"}' http://cs3103.cs.unb.ca:$port/presentlist)
echo "$lastOutput"
plId=$(echo "$lastOutput" | grep -m 1 'id' | tail -1 | cut -d':' -f2 | cut -d',' -f1 | xargs)
echo "${plId}"

#update presentList
echo "###########Update present list"
lastOutput=$(curl -s -i -X PUT -b cookie-jar -H "Content-Type: application/json" -d '{"presentListId":'$plId',"presentListName": "TestList-updated", "presentListDesc": "TestList for testing - updated", "userEmail":"'$email'"}' http://cs3103.cs.unb.ca:$port/presentlist)
echo "$lastOutput"

#get presentListByUserEmail:
echo "###########Get present list"
lastOutput=$(curl -s -i http://cs3103.cs.unb.ca:$port/presentlists/$email)
echo "$lastOutput"


#
# TEST PRESENT CRUD
#
#create present (on an existing present)
echo "###########Create Present"
lastOutput=$(curl -s -i -X POST -b cookie-jar -H "Content-Type: application/json" -d '{"presentName": "TestPresent", "presentDesc": "Test Present for testing", "presentPrice": "10.20", "presentListId": '$plId', "userEmail": "'$email'"}' http://cs3103.cs.unb.ca:$port/present)
echo "$lastOutput"
pId=$(echo "$lastOutput" | grep -m 1 'id' | tail -1 | cut -d':' -f2 | cut -d',' -f1 | xargs)

#update present
echo "###########Update Present"
lastOutput=$(curl -s -i -X PUT -H "Content-Type: application/json"  -b cookie-jar -d '{"presentId":'$pId', "presentName": "TestPresent-update", "presentDesc": "TestPresent for testing", "presentPrice": "101.50", "presentListId": '$plId', "userEmail": "'$email'"}' http://cs3103.cs.unb.ca:$port/present)
echo "$lastOutput"

#get present:
echo "###########Get Present"
lastOutput=$(curl -s -i http://cs3103.cs.unb.ca:$port/present/$pId)
echo "$lastOutput"


#
# CLEANUP
#
#delete present
echo "###########Delete Present"
lastOutput=$(curl -s -i -X DELETE -b cookie-jar http://cs3103.cs.unb.ca:$port/present/$pId)
echo "$lastOutput"

#delete presentList
echo "###########Delete Present List"
lastOutput=$(curl -s -i -X DELETE -b cookie-jar http://cs3103.cs.unb.ca:$port/presentlist/$plId)
echo "$lastOutput"

#delete user (should be last just as clean up on failures. This will clear all pl/presents asociated with the test user).
echo "###########Delete User"
echo "curl -s -i -X DELETE -b cookie-jar http://cs3103.cs.unb.ca:$port/user/$email"
lastOutput=$(curl -s -i -X DELETE -b cookie-jar http://cs3103.cs.unb.ca:$port/user/$email)
echo "$lastOutput"