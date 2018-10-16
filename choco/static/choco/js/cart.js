"use strict";

window.addEventListener("load", () => {
    let ups = document.getElementsByClassName("quantity-up");
    let downs = document.getElementsByClassName("quantity-down");
    let addCatalogForms = document.getElementsByClassName("cart-add-form");

    for (let btn of ups) {
        btn.addEventListener("click", quantityUp);
    }

    for (let btn of downs) {
        btn.addEventListener("click", quantityDown);
    }

    for (let form of addCatalogForms) {
        form.addEventListener("submit", addCartItem);
    }

    addRemovalEvents();
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
            $('#total-items').text(json.total_items);
            $('#price-' + itemId + '-' + configId).text(json.choco_price);
            $('#total-price-' + itemId + '-' + configId).text(json.total_price);
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
            document.getElementById("total-items").innerHTML = json.total_items;

            //removing from sidecart
            if (e.target.className.indexOf("sidecart") != -1) {
                let itemContainer = e.target.parentNode.parentNode.parentNode;
                itemContainer.style.opacity = 0;
    
                setTimeout(() => {
                    itemContainer.removeAttribute("id");
                    itemContainer.remove();
    
                    if(json.total_items == 0) {
                        $("#cart-content").append('<div class="cart-empty">Корзина пуста!</div>');
                    }
                }, 500);
                return;
            }

            //removing from the cart page
            let itemContainer = e.target.parentNode.parentNode.parentNode;
            console.log(itemContainer);
            itemContainer.style.opacity = 0;

            setTimeout(() => {
                $('#product-' + itemId + '-' + configId).remove();
                if(json.total_items == 0) {
                    document.getElementById("cart-main").remove();
                    document.getElementById("checkout-btn").remove();
                    $("#main-cart-content").append('<div class="cart-empty">Корзина пуста!</div>');
                }
            }, 500);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
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
            $('#total-items').text(json.total_items);
            reloadSideCart(json.new_item, json.static_dir);
            
            let closeTimer = null;
            if (document.getElementById("side-cart").style.transform == "") {
                openCart(e);
                closeTimer = setTimeout(() => {closeCart(e)},1500);
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
