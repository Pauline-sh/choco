$(document).ready(function(){
    $('#contact-form').on('submit', function(event){
        event.preventDefault();
        send_message();
    });
});

function send_message(){
    $("body").addClass("loading");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "send/",
        type: "POST",
        dataType: "json",
        data: {
            the_name : $('#id_name').val(),
            the_email : $('#id_email').val(),
            the_subject : $('#id_subject').val(),
            the_message : $('#id_message').val(),
        },
        headers:{
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            $('#id_name').val('').css('outline: none;');
            $('#id_email').val('');
            $('#id_subject').val('');
            $('#id_message').val('');

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check

            $("body").removeClass("loading");
            location.href="/";

        },
        error: function(xhr, errmsg, err) {
            $("body").removeClass("loading");
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
