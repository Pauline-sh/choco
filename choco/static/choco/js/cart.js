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

    if (document.querySelector('input[name="order-as-gift"]')) {
        document.querySelector('input[name="order-as-gift"]').checked = false;
        document.querySelector('input[name="order-as-gift"]').addEventListener("change", () => {
            document.querySelector("#package-selection").classList.toggle("hidden");
            switchCartAsGift();
        })
    }

    let cartPackageRadios = document.getElementsByName('package-style');
    for (let packageRadio of cartPackageRadios) {
        packageRadio.checked = false;
        packageRadio.addEventListener("click", setCartPackageStyle);
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
            if (json.total_items >= 2) {
                document.querySelector(".order-as-gift-text").innerHTML = "Заказать как подарок (-10%)";
            } else {
                document.querySelector(".order-as-gift-text").innerHTML = "Заказать как подарок";
            }
            $('#total-items').text(json.total_items);
            $('#price-' + itemId + '-' + configId).text(json.choco_price);
            $('#total-price-' + itemId + '-' + configId).text(json.total_price);
            document.querySelector("#total>span").innerHTML = json.total_cart_price;
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

                    calcSidecartTotal(json.cart);

                    if(json.total_items == 0) {
                        $("#cart-content").append('<div class="cart-empty">Корзина пуста!</div>');
                        document.querySelector('.sidecart-total').remove();
                    }
                }, 500);
                return;
            }

            //removing from the cart page
            let itemContainer = e.target.parentNode.parentNode.parentNode;
            itemContainer.style.opacity = 0;
            document.querySelector("#total>span").innerHTML = json.total_cart_price;

            setTimeout(() => {
                $('#product-' + itemId + '-' + configId).remove();
                if (json.total_items == 1) {
                    document.querySelector(".order-as-gift-text").innerHTML = "Заказать как подарок";
                    return;
                } 

                if (json.total_items == 0) {
                    document.getElementById("gift").remove();
                    document.getElementById("cart-main").remove();
                    document.getElementById("checkout-btn").remove();
                    document.getElementById("total").remove();
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

            calcSidecartTotal(json.cart);

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

function calcSidecartTotal(cart) {
    let total = 0;
    for (let item of Object.keys(cart)) {
        total += Number(cart[item][0].total_price);
    }

    document.querySelector('#sidecart-total-num').innerHTML = total;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCartPackageStyle(e) {
    let gift_switch = document.getElementById("gift-switch");
    let packageId = e.target.value;
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "/cart_as_gift_package/" + packageId + "/",
        type: "POST",
        dataType: "json",

        data: {
            gift_switch: gift_switch.checked,
        },

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            //console.log(json);
            document.querySelector("#total>span").innerHTML = json.total_price;
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function switchCartAsGift(e){
    let cartPackageRadios = document.getElementsByName('package-style');
    for (let packageRadio of cartPackageRadios) {
        packageRadio.checked = false;
    }
    let gift_switch = document.getElementById("gift-switch");
    if(gift_switch.checked === false){
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "/cart_as_gift/",
            type: "POST",
            dataType: "json",
            data: {
                gift_switch: gift_switch.checked,
            },
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function(json) {
                //console.log(json);
                document.querySelector("#total>span").innerHTML = json.total_price;
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}
