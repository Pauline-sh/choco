"use strict";

window.addEventListener("load", () => {
    let ups = document.getElementsByClassName("quantity-up");
    let downs = document.getElementsByClassName("quantity-down");
    let removeForms = document.getElementsByClassName("cart-remove-item");
    let addCatalogForms = document.getElementsByClassName("cart-add-form");

    for (let btn of ups) {
        btn.addEventListener("click", quantityUp);
    }

    for (let btn of downs) {
        btn.addEventListener("click", quantityDown);
    }

    for (let form of removeForms) {
        form.addEventListener("submit", removeCartItem);
    }

    for (let form of addCatalogForms) {
        form.addEventListener("submit", addCartItem);
    }
})

function quantityUp(e) {
    e.preventDefault();
    let input = e.target.parentNode.firstElementChild;
    let newValue = parseInt(input.value) + 1;

    if (isNaN(newValue) || newValue < input.min) {
        newValue = 1;
    }

    if(e.target.parentNode.hasAttribute("product") && e.target.parentNode.hasAttribute("config")){
        let itemId = e.target.parentNode.getAttribute("product");
        let configId = e.target.parentNode.getAttribute("config");
        console.log("ajax request");
        updateQuantity(itemId, configId, newValue);
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

    if(e.target.parentNode.hasAttribute("product") && e.target.parentNode.hasAttribute("config")){
        let itemId = e.target.parentNode.getAttribute("product");
        let configId = e.target.parentNode.getAttribute("config");

        updateQuantity(itemId, configId, newValue);
    }

    input.value = newValue;
}

function updateQuantity(itemId, configId, newValue){
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    $.ajax({
        url: "/update/" + itemId + "/" + configId + "/",
        type: "POST",
        dataType: "json",
        data: {
            newValue: parseInt(newValue),
        },

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            //console.log(JSON.stringify(json));
            $('#total-items').text(json.total_items);
            $('#total-price-' + itemId + '-' + configId).text(json.total_price);
            //console.log(json.total_price);
        },
        error: function(xhr, errmsg, err) {
            //console.log(xhr.status + ": " + xhr.responseText);
        }
    });
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

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            //console.log(JSON.stringify(json));
            $('#product-' + itemId + '-' + configId).remove();
            $('#total-items').text(json.total_items);
        },
        error: function(xhr, errmsg, err) {
            //console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    console.log("form submitted!");  // sanity check
}

function addCartItem(e){
    e.preventDefault();

    let itemId = e.target.getElementsByClassName("choco-pk")[0].value,
        configId = -1;

    let configClassItems = e.target.getElementsByClassName("config-pk");
    if(configClassItems.length > 0){
        configId = configClassItems[0].firstElementChild.value
        if(!configId)
            configId = -1;
    }
    console.log(configId);

    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let newValue = e.target.getElementsByClassName("quantity")[0].firstElementChild.value;

    $.ajax({
        url: "/add/" + itemId + "/",
        type: "POST",
        dataType: "json",
        data: {
            newValue: newValue,
            configId: configId,
        },

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            console.log(JSON.stringify(json));
            $('#total-items').text(json.total_items);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    console.log("form submitted!");  // sanity check
}
