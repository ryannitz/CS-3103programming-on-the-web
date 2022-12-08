var app = new Vue({
    el: "#app",

  //------- data --------
    data: {
        serviceURL: "https://cs3103.cs.unb.ca:8006",
        authURL: "/auth",
        userURL: "/user/",
        usersURL: "/users",
        presentListURL: "/presentlist",
        presentListsURL: "/presentlists/",
        presentURL: "/present",
        presentsByList: "/getPresentsByList/",

        searchUser: "",

        authenticated: false,
        loadingUsers: true,

        processingRequest : false,//for when user makes a request on a modal
        viewingPresentLists: true,

        editingPresentList: false,
        editingPresent: false,
        input: {
            username: "",
            password: ""
        },
        loggedUser : {
            creationDate: null,
            id: null,
            modificationDate: null,
            userEmail: "",
            userName: ""
        },
        delItem : {
            delName: "",
            delType: "",
            delObj: null
        },
        users : [],
        selectedUser : {
            creationDate: null,
            id: null,
            modificationDate: null,
            userEmail: "",
            userName: ""
        },
        presentLists : [],
        selectedPresentList : {
            creationDate: null,
            id: null,
            modificationDate: null,
            presentListDesc: "",
            presentListName: "",
            userEmail: ""
        },
        presents : [],
        selectedPresent : {
            creationDate: null,
            id: null,
            modificationDate: null,
            presentDesc: "",
            presentListId: null,
            presentName: "",
            presentPrice: null,
            userEmail: ""
        }
    },

  //------- methods --------
    methods: {
        login() {
          if (this.input.username != "" && this.input.password != "") {
            var tempUsername = this.input.username;
            axios.post(this.serviceURL+this.authURL, {
                "username": tempUsername,
                "password": this.input.password
            })
            .then(response => {
                if (response.data.status == "success") {
                  var email = tempUsername+"@unb.ca";
                  this.provisionUser(tempUsername, email)
                }
            })
            .catch(e => {
                alert("The username or password was incorrect, try again");
                this.input.password = "";
                console.log(e);
            });
          } else {
            alert("A username and password must be present");
          }
        },

        logout() {
           axios
            .delete(this.serviceURL+this.authURL)
            .then(response => {
                location.reload();
            })
            .catch(e => {
                this.loggedUser = null;
                this.authenticated = false;
                console.log(e);
            });
        },

        provisionUser(username, email){
            axios
            .get(this.serviceURL+this.userURL+email)
            .then(response => {
                this.initWithUser(response.data)
            })
            .catch(e => {
                if(e.response){
                    if(e.response.status == 404){
                        this.createUser(username, email)
                    }else{
                        console.log(e);
                        createAlert("danger", "Unable to provision user", 3000);
                    }
                }
            });
        },

        getUser(email){
            axios
            .get(this.serviceURL+this.userURL+email)
            .then(response => {
                this.selectedUser = response.data;
            })
            .catch(e => {
                console.log(e);
            });
        },

        createUser(username, email){
            axios
            .post(this.serviceURL+this.userURL+email, {
                "userName" : username,
                "userEmail" : email
            })
            .then(response => {
                console.log("user: " + JSON.stringify(response.data));
                this.initWithUser(response.data);
            })
            .catch(e => {console.log(e);
                console.log(e);
                createAlert("danger", "Unable to create user.", 3000);
            });
        },

        initWithUser(data){
            this.loggedUser = data;
            this.selectedUser = data;
            this.authenticated = true;
            console.log("user:" + JSON.stringify(this.loggedUser));
            if(this.loggedUser.id != null){
                this.fetchUsers();//load user sidebar can run asynchronously
                this.fetchPresentListByEmail(this.loggedUser.userEmail)//can run asynchronously
            }else{
                createAlert("danger", "Unable to complete login sequence.", 3000);
            }
        },

        fetchUsers() {
            this.loadingUsers = true;
            axios
            .get(this.serviceURL+this.usersURL)
            .then(response => {
                this.users = response.data;
                console.log("users: " + JSON.stringify(response.data));
                this.loadingUsers = false;
            })
            .catch(e => {
                createAlert("danger", "Unable to load users data.", 3000);
                console.log(e);
                this.loadingUsers = false;
            });
        },

        fetchPresentListByEmail(email){
            axios
            .get(this.serviceURL+this.presentListsURL+email)
            .then(response => {
                console.log("presentlists: " + JSON.stringify(response.data));
                this.presentLists = response.data;
                this.viewingPresentLists = true;
                this.getUser(email);
            })
            .catch(e => {
                createAlert("danger", "Unable get to present lists.", 3000);
                console.log(e);
            });
        },

        createPresentList(){
            this.editingPresentList = false;
            var presentListName = $("#presentListName").val();
            console.log(presentListName)
            var presentListDesc = $("#presentListDesc").val();
            console.log(presentListDesc)
            axios
            .post(this.serviceURL+this.presentListURL, {
                "presentListName" : presentListName,
                "presentListDesc" : presentListDesc,
                "userEmail" : this.loggedUser.userEmail
            })
            .then(response => {
                console.log("presentlist: " + JSON.stringify(response.data));
                this.selectedPresentList = response.data;
                this.presentLists.push(this.selectedPresentList);
                this.viewingPresentLists = false;
                $('#addPresentListModal').modal('hide');
                createAlert("success", "Created present list.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Unable to create present list.", 3000);
            });
        },

        updatePresentList(presentListIn){
            this.editingPresentList = true;
            var presentListName = $("#presentListName").val();
            console.log(presentListName)
            var presentListDesc = $("#presentListDesc").val();
            console.log(presentListDesc)
            axios
            .put(this.serviceURL+this.presentListURL, {
                "presentListId" : presentListIn.id,
                "presentListName" : presentListName,
                "presentListDesc" : presentListDesc,
                "userEmail" : this.loggedUser.userEmail
            })
            .then(response => {
                console.log("presentlist: " + JSON.stringify(response.data));
                this.selectedPresentList = response.data;
                this.fetchPresentListByEmail(presentListIn.userEmail);
                this.viewingPresentLists = true;
                $('#addPresentListModal').modal('hide');
                createAlert("success", "Updated present list.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Unable to update present list.", 3000);
            });
        },

        setDeleteItem(delNameIn, delTypeIn, object){
            this.delItem.delName = delNameIn;
            this.delItem.delType = delTypeIn;
            this.delItem.delObj = object;
        },

        deletePresentList(presentListId, userEmail){
            axios
            .delete(this.serviceURL+this.presentListURL +"/"+presentListId)
            .then(response => {
                //this will only ever be the logged user as they are the only ones who can delete/edit
                this.fetchPresentListByEmail(userEmail);
                createAlert("success", "Deleted present list.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Could not delete present list.", 3000);
            });
        },

        createPresent(presentList){
            var presentName = $("#presentName").val();
            console.log(presentName)
            var presentDesc = $("#presentDesc").val();
            console.log(presentDesc)
            var presentPrice = $("#presentPrice").val();
            console.log(presentPrice)

            axios
            .post(this.serviceURL+this.presentURL, {
                "presentName" : presentName,
                "presentDesc" : presentDesc,
                "presentPrice" : presentPrice,
                "presentListId" : presentList.id,
                "userEmail" : this.loggedUser.userEmail
            })
            .then(response => {
                console.log("present: " + JSON.stringify(response.data));
                this.selectedPresent = response.data;
                this.presents = response.data;
                $('#addPresentModal').modal('hide');
                createAlert("success", "Created present.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Unable to create present.", 3000);
            });
        },

        updatePresent(presentIn){
            var presentName = $("#presentName").val();
            console.log(presentName)
            var presentDesc = $("#presentDesc").val();
            console.log(presentDesc)
            var presentPrice = $("#presentPrice").val();
            console.log(presentPrice)
            var presentListId = $("#presentList").val();
            console.log(presentListId)
            axios
            .put(this.serviceURL+this.presentURL, {
                "presentId": presentIn.id,
                "presentName" : presentName,
                "presentDesc" : presentDesc,
                "presentPrice" : presentPrice,
                "presentListId" : presentIn.presentListId,
                "userEmail" : this.loggedUser.userEmail
            })
            .then(response => {
                console.log("present: " + JSON.stringify(response.data));
                this.selectedPresent = response.data;
                this.presents = response.data;
                $('#addPresentModal').modal('hide');
                createAlert("success", "Updated present.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Unable to update present.", 3000);
            });
        },

        deletePresent(present){
            axios
            .delete(this.serviceURL+this.presentURL +"/"+present.id)
            .then(response => {
                //this will only ever be the logged user as they are the only ones who can delete/edit
                this.getPresentsByPresentList(present.presentListId);
                createAlert("success", "Deleted present.", 3000);
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Could not delete present.", 3000);
            });
        },

        getPresentsByPresentList(presentListId){
            axios
            .get(this.serviceURL+this.presentsByList+presentListId)
            .then(response => {
                console.log("presents: " + JSON.stringify(response.data));
                this.presents = response.data;
                this.viewingPresentLists = false;
            })
            .catch(e => {
                console.log(e);
                createAlert("danger", "Unable to create user.", 3000);
            });
        },

        showDelModal(){
            $("#delModal").modal('show');
        },

        showAddPlModal(){
            $("#addPresentListModal").modal('show');
        },

        showAddPresentModal(){
            $("#addPresentModal").modal('show');
        }

    },

    computed: {
        filteredUsers() {
            return this.users.filter(user => {
                return user.userName.toLowerCase().indexOf(this.searchUser.toLowerCase()) > -1
            })
        }
    }
});

function createAlert(type, text, millis){
    var id = Math.floor((Math.random() * 1000) + 1);
    var alerthtml = '<div id="alert-'+id+'" class="alert alert-'+type+' alert-dismissible text-center fixed-bottom w-75 mx-auto mb-5">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong><i class="fas fa-info-circle"></i></strong> '+
                    text+
                '</div>'
    $("body").append(alerthtml);
    setTimeout(function(){
        $('#alert-'+id).fadeOut(500, function(){
            $('#alert-'+id).remove();
        });
    }, millis)
  }
