$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth()+1;
    var year = date.getFullYear();
    $("#date").text(day+"/"+month+"/"+year);

    $("#toggleJumbo").click(function(){
        $(this).find("i").toggleClass("rotate180");;
        $("#jumbotron").slideToggle();
    });

    $(".nav-direct").click(function(){
        $(".nav-direct").parent().removeClass("active");
        $(this).parent().addClass("active");
    });

    $(".assignment-header").click(function(){
        $(this).find("i").toggleClass("rotate180");
    });

    $("#contactMenu > div > button.close").click(function () {
        $("#contactMenu").collapse('hide');
    });

    $(".copyTrigger").click(function(){
        var copyTarget = $(this).attr("data-target");
        $("#invisible").val($(copyTarget).html()).select();
        document.execCommand("copy");
        var alertText = "Copied: <b>"+$(copyTarget).html()+"</b> to clipboard!";
        createAlert("info", alertText, 3000);
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

    function responsiveNav(){
        //bootstrap container resize widths (for 1080p)
        if($(window).width() < 992){
            $(".respToggleNavBrand").hide();
            if($(window).width() < 768){
                $(".respToggleNavLink").hide();
                if($(window).width() < 559){
                    $(".respToggleNavBrand").show();
                    $(".respToggleNavLink").show();
                }
            }else{
                $(".respToggleNavLink").show();
            }
        }else{
            $(".respToggleNavBrand").show();
            $(".respToggleNavLink").show()
        }
    }
    //check the window size on load.
    responsiveNav();
    $(window).resize(responsiveNav);
});