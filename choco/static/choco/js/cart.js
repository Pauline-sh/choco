"use strict";

window.addEventListener("load", () => {
    let ups = document.getElementsByClassName("quantity-up");
    let downs = document.getElementsByClassName("quantity-down");

    for (let btn of ups) {
        btn.addEventListener("click",quantityUp);
    }

    for (let btn of downs) {
        btn.addEventListener("click",quantityDown);
    }
})

function quantityUp(e) {
    e.preventDefault();
    let input = e.target.parentNode.firstElementChild;
    let newValue = parseInt(input.value) + 1;

    if (isNaN(newValue) || newValue < input.min) {
        newValue = 1;
    }

    input.value = newValue;
}

function quantityDown(e) {
    e.preventDefault();
    let input = e.target.parentNode.firstElementChild;
    let newValue = parseInt(input.value) - 1;

    if (isNaN(newValue) || newValue < input.min) {
        newValue = 1;
    }

    input.value = newValue;
}

$(document).ready(function(){
    //$('#cart-remove-item-submit').on('click', function(event){
    $('#cart-remove-item').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        removeCartItem();
    });
});

function removeCartItem() {
    let itemId = $('#choco-pk').val(),
        configId = $('#config-pk').val();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: "/remove/" + itemId + "/" + configId + "/",
        type: "POST",
        dataType: "json",
        data: {
            itemId: itemId,
            configId: configId,
        },

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            console.log(JSON.stringify(json));
            $('#product-' + itemId).remove();
            $('#total-items').text(json.total_items);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

