

/**
 * TODO: 
 * 
 * Check if user is authed as the first JS check. Redirect to login page if not authed.
 * 
 * handle edit user
 * 
 * handle delete presentlist (disable add present button if no present lists)
 * handle edit presentlist
 * 
 * handle create present
 * handle delete present
 * handle edit present
 * 
 * 
 * format and add price to present list template.
 * create present template
 *
 */
$(document).ready(function(){


  function resized(){
      if($("#userListContainer").position() != undefined){
        var userListOffset = $("#userListContainer").position().top + 100;
        if($(".left-col").width() <= 200){
          $(".main-col").addClass("ml200");
        }else{
          $(".main-col").removeClass("ml200");
        }
        $("#userListContainer").height($(window).height()-userListOffset);
      }
  }
  resized();
  $(window).resize(function(){
    resized();
  })




  $("form").submit(function(e){
    e.preventDefault();
  });

  $('[data-toggle="tooltip"]').tooltip();

  $("#showPassword").click(function(){
    $(this).toggleClass("fa-eye-slash");
    $(this).toggleClass("fa-eye");
    var passwordType = $("#password").attr("type");
    $("#password").attr("type", passwordType=="password"?"text":"password");
});


});