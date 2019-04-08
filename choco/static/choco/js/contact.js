var form_open = true;

$(document).ready(function(){
    $('#contact-form').on('submit', function(event){
        event.preventDefault();
        send_contact_message();
    });

    $('#order-call-triangle').on('click', function(event){
        form_open ? close_call_form() : open_call_form()
    })
});

function open_call_form(){
    $('#order-call-content').css({'display':''});
    $('#order-call-modal').css({'padding-right':''});
    $('#order-call-triangle').css({
        'border-width':'',
        'border-color':''
    })

    form_open = true;
}

function close_call_form() {
    $('#order-call-content').css({'display':'none'});
    $('#order-call-modal').css({'padding-right':'25px'});
    $('#order-call-triangle').css({
        'border-width':'20px 0 20px 20px',
        'border-color':'transparent transparent transparent #ffffff'
    })

    form_open = false;
}

function send_contact_message(){
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "/send/",
        type: "POST",
        dataType: "json",
        data: {
            the_name : $('#id_name').val(),
            the_phone : $('#id_phone').val()
        },
        headers:{
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            if(json.result != "OK"){
                alert(json.error);
            }
            else{
                alert("Ваш заказ принят!");
                $('#id_name').val('');
                $('#id_phone').val('');
                close_call_form();
            }

        },
        error: function(xhr, errmsg, err) {
            $("body").removeClass("loading");
            alert("Что-то пошло не так, попробуйте позже");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
