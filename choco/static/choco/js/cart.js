"use strict";

window.addEventListener("load", () => {
    let ups = document.getElementsByClassName("quantity-up");
    let downs = document.getElementsByClassName("quantity-down");
    let removeForms = document.getElementsByClassName("cart-remove-item");

    for (let btn of ups) {
        btn.addEventListener("click",quantityUp);
    }

    for (let btn of downs) {
        btn.addEventListener("click",quantityDown);
    }

    for (let form of removeForms) {
        form.addEventListener("submit",removeCartItem);
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

function removeCartItem(e) {
    e.preventDefault();

    let itemId = e.target.getElementsByClassName("choco-pk")[0].value;
    let configId = e.target.getElementsByClassName("config-pk")[0].value;
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

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

    console.log("form submitted!");  // sanity check
}

