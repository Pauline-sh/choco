$(document).ready(function(){
    $('#contact-form').on('submit', function(event){
        event.preventDefault();
        send_contact_message();
    });
});

function send_contact_message(){
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
            console.log(json);
            console.log("success");

            $("body").removeClass("loading");
            if(json.result != "OK"){
                alert(json.error);
            }
            else{
                // тут сделать модалочьку
                alert("Ваше сообщение успешно отправлено!");
                location.href="/";
            }

        },
        error: function(xhr, errmsg, err) {
            $("body").removeClass("loading");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
