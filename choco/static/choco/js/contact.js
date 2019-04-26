var form_open = false;
var timer;

$(document).ready(function(){
    if(sessionStorage.getItem('contact_form_open') === "1") {
        open_call_form();
    }

    if(sessionStorage.getItem('site_visited') === null) {
        open_call_form(true);
    
        sessionStorage.setItem('site_visited', '1');

        timer = setTimeout(function() {
            close_call_form();
        }, 10000)
    }

    $('#contact-form').on('submit', function(event){
        event.preventDefault();
        send_contact_message();
    });

    $('#order-call-triangle').on('click', function(event){
        form_open ? close_call_form() : open_call_form()
    })

    var order_call_inputs = document.querySelectorAll('.order-call-input');

    for(var input of order_call_inputs) {
        input.addEventListener('click', function(e) {
            clearTimeout(timer);
        })
    }
});

function open_call_form(skip_flag){
    $('#order-call-content').css({'display':'block'});
    $('#order-call-modal').css({'padding-right':'40px'});
    $('#order-call-triangle').css({
        'border-width':'20px 20px 20px 0',
        'border-color':'transparent #ffffff transparent transparent'
    })

    form_open = true;
    
    if(!skip_flag) {
        sessionStorage.setItem('contact_form_open', '1');
    }
}

function close_call_form() {
    $('#order-call-content').css({'display':''});
    $('#order-call-modal').css({'padding-right':''});
    $('#order-call-triangle').css({
        'border-width':'',
        'border-color':''
    })

    form_open = false;
    sessionStorage.setItem('contact_form_open', '0');
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
