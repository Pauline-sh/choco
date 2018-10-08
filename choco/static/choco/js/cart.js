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
        //console.log("ajax request");
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
            $('#price-' + itemId + '-' + configId).text(json.choco_price);
            $('#total-price-' + itemId + '-' + configId).text(json.total_price);
            //console.log(json.total_price);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
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
            if(json.total_items == 0){
                document.getElementById("cart-main").remove();
                document.getElementById("checkout-btn").remove();
                $("#main-cart-content").append('<div class="cart-empty">Корзина пуста!</div>');
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    //console.log("form submitted!");  // sanity check
}

function isInt(value) {
  return !isNaN(value) &&
         parseInt(Number(value)) == value &&
         !isNaN(parseInt(value, 10));
}

function addCartItem(e){
    e.preventDefault();

    let itemId = e.target.getElementsByClassName("choco-pk")[0].value,
        configId = -1;

    let configClassItems = e.target.getElementsByClassName("config-pk");
    if(configClassItems.length > 0){
        configId = configClassItems[0].firstElementChild.value
        if(!isInt(configId))
            configId = -1;
    }
    //console.log(configId);

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
            console.log(JSON.stringify(json.new_item));
            $('#total-items').text(json.total_items);
            reloadSideCart(json.new_item, json.static_dir);

            openCart(e);
            setTimeout(() => {closeCart(e)},1500);
        },
        error: function(xhr, errmsg, err) {
            //console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    //console.log("form submitted!");  // sanity check
}

function reloadSideCart(new_item, static_dir){
    let sideCartContentClass = document.getElementById("side-cart").getElementsByClassName("cart-content");
    if(sideCartContentClass.length > 0){
        let sideCartContent = sideCartContentClass[0];

        if(document.querySelector("#sidecart-item-" + new_item.product.id + '-' + new_item.configuration) == null){
            if(sideCartContent.firstElementChild.classList.contains("cart-empty")){
                // delete empty cart message
                sideCartContent.firstElementChild.remove();
            }
                // append new item
                let img_src = "default.png";
                if(new_item.product.choco_dir){
                    img_src = new_item.product.choco_dir + '/' + new_item.product.choco_pic;
                }

                let new_item_str = '<div class="cart-item" id="sidecart-item-' + new_item.product.id + '-' + new_item.configuration + '">' +
                                        '<div class="wrapper">' +
                                            '<div class="cart-item-image">' +
                                                '<img src="' + static_dir + img_src + '"/>' +
                                            '</div>' +
                                            '<div class="cart-item-info">' +
                                                '<div>' + new_item.product.choco_name + '</div>' +
                                                '<div>Вес: ' + new_item.conf_object.choco_weight + '</div>' +
                                                '<div id="sidecart-quantity-' + new_item.product.id + '-' + new_item.configuration + '">Количество: ' + new_item.quantity + '</div>' +
                                                '<div>Цена: ' + new_item.total_price + ' RUB</div>' +
                                            '</div>' +
                                            '<div class="delete-cross-wrap">' +
                                                '<a href="#" class="delete-cross" remove="' + new_item.product.id + '" configure="' + new_item.configuration + '">✕</a>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>';

                $("#cart-content").append(new_item_str);

                let crosses = document.getElementsByClassName("delete-cross");
                for (let cross of crosses) {
                    cross.addEventListener("click", removeSidecartItem);
                }
        }
        else{
            // update quantity
            $('#sidecart-quantity-' + new_item.product.id + '-' + new_item.configuration).text("Количество: " + new_item.quantity);
        }
    }
}

/*
function makeTemplate(id, config, ) {

}
*/