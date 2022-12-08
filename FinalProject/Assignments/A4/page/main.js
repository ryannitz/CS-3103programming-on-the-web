

$(document).ready(function(){
  var root = "https://cs3103.cs.unb.ca/rnitz/cgi-bin";
  var getSchoolsURL = root+"/getSchools.py?";
  var addSchoolURL = root+"/addSchool.py?";
  var delSchoolURL = root+"/delSchool.py?";
  var listSchoolsURL = root+"/listSchools.py?";


  $('[data-toggle="tooltip"]').tooltip();

  callProvList();

  $("#listProvince").on("change", function () {
    callProvList();
  });

  function callProvList(){
    var queryStr = $('#headerform').serialize();//prov=
    if(queryStr == "prov=ALL"){
      $.get(getSchoolsURL, function(data, status){
        populateTable(data);
      });
    }else{
      $.get(listSchoolsURL+queryStr, function(data, status){
        populateTable(data);
      });
    }
  }

  function populateTable(data){
    var html = "";
    for(var i = 0; i < data.length; i++){
      html += "<tr>"
      var school = data[i]
      Object.keys(school).forEach(function(key) {
        html += "<td>"+school[key]+"</td>"
      });
      html += "<td><i id='delSchool' class='far fa-trash-alt text-danger' data-toggle='tooltip' title='Delete'></i></td></tr>";
    }
    $("#schoolTable > tbody").html(html);
  }

  $(document).on("click", "#delSchool", function(){
    triggerDelSchoolModal(parseInt($(this).parent().parent().children().first().html()));
  });

  var schoolId;
  function triggerDelSchoolModal(id){
    schoolId = id;
    $("#delSchoolModalBody").html("<p>Are you sure you would like to delete school with ID: <strong>"+schoolId+"</strong><p>")
    $("#delSchoolModal").modal()
  }

  $("#delSchool").click(function(){
    var querytStr = "schoolId="+schoolId;
    $.post(delSchoolURL+querytStr, function(data, success){
      createAlert("info", "School record successfully deleted.", 2000);
      //remove element from list or refresh list.
      callProvList();
    })
  });

  $("#delSchoolId").on("change", function(){
    $(this).val() > 0 ? $("#delSchoolButton").removeClass("disabled"):$("#delSchoolButton").addClass("disabled");
  })

  $("#delSchoolButton").click(function(){
    if($("#delSchoolId").val() > 0 && !$(this).hasClass("disabled")){
      triggerDelSchoolModal($("#delSchoolId").val());
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

  $("#addSchool").click(function(e){
    var queryString = $("#addSchoolForm").serialize();
    $.post(addSchoolURL+queryString, function(data, success){
      createAlert("info", "School record successfully added with ID: <strong>"+data+"</strong>", 3000);
      //remove element from list or refresh list.
      callProvList();
    });
  });
});