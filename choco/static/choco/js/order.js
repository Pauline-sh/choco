$(document).ready(function(){
    $('#order-form').on('submit', function(event){
        event.preventDefault();
        send_order_message();
    });
});

function send_order_message(){
    $("body").addClass("loading");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "send/",
        type: "POST",
        dataType: "json",
        data: {
            the_name : $('#id_name').val(),
            the_city : $('#id_city').val(),
            the_phone_number : $('#id_phone_number').val(),
            the_note : $('#id_note').val(),
        },
        headers:{
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            console.log(json);

            $("body").removeClass("loading");

            if(json.result != "OK"){
                alert(json.error);
            }
            else{
                // тут сделать модалочьку
                console.log(json.cart);
                alert("Ваш заказ успешно отправлен!");
                location.href="/";
            }

        },
        error: function(xhr, errmsg, err) {
            $("body").removeClass("loading");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
