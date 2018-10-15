"use strict";

window.addEventListener("load", () => {
    document.getElementById("open-cart").addEventListener("click", openCart);
    document.getElementById("close-cart").addEventListener("click", closeCart);

    addRemovalEvents();
})

function openCart(e) {
    e.preventDefault();

    if (window.location.pathname == "/cart/") {
        $('html, body').animate({
            scrollTop: $("#cart-main").offset().top
        }, 500);
        return;
    }

    document.getElementById("side-cart").style.transform = "translateX(-100%)";
}

function closeCart(e) {
    e.preventDefault();
    document.getElementById("side-cart").style.transform = "";
}

function addRemovalEvents() {
    let removeForms = document.getElementsByClassName("cart-remove-item");
    for (let form of removeForms) {
        form.addEventListener("submit", removeCartItem);
    }
}

function removeSidecartItem(e) {
    e.preventDefault();
    let itemId = this.getAttribute("remove");
    let configId = this.getAttribute("configure");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let itemContainer = this.parentNode.parentNode.parentNode;

    $.ajax({
        url: "/remove/" + itemId + "/" + configId + "/",
        type: "POST",
        dataType: "json",
        data: {
            itemId: itemId,
            configId: configId,
        },
        
        headers:{
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            itemContainer.style.opacity = 0;
            document.getElementById("total-items").innerHTML = json.total_items;

            setTimeout(() => {
                itemContainer.removeAttribute("id");
                itemContainer.remove();

                if(json.total_items == 0){
                    $("#cart-content").append('<div class="cart-empty">Корзина пуста!</div>');
                }
            }, 500);

        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
} 

function reloadSideCart(new_item, static_dir){
    let sideCartContent = document.getElementById("side-cart").getElementsByClassName("cart-content")[0];

    // update quantity if already in cart
    if(document.querySelector("#sidecart-item-" + new_item.product.id + '-' + new_item.configuration)) {
        $('#sidecart-quantity-' + new_item.product.id + '-' + new_item.configuration).text("Количество: " + new_item.quantity);
        return;
    }
            
    // delete empty cart message
    if(sideCartContent.firstElementChild.className.indexOf("cart-empty") != -1) {
        sideCartContent.firstElementChild.remove();
    }
                
    // append new item
    let img_src = "default.png";
    if(new_item.product.choco_dir){
        img_src = new_item.product.choco_dir + '/' + new_item.product.choco_pic;
    }

    let config_str = "";
    if(new_item.conf_object.weight){
        config_str = '<div>Вес: ' + new_item.conf_object.weight + ' г</div>'
    }

    let new_item_child = makeTemplate(new_item.product.id, new_item.configuration,
                                      static_dir, img_src, new_item.product.choco_name,
                                      config_str, new_item.quantity,
                                      new_item.total_price);

    $("#cart-content").append(new_item_child);
    addRemovalEvents();
}

function makeTemplate(id, config, static_dir, img, name, config_str, quantity, price) {
    return ('<div class="cart-item" id="sidecart-item-' + id + '-' + config + '">' +
                '<div class="wrapper">' +
                    '<div class="cart-item-image">' +
                        '<img src="' + static_dir + img + '"/>' +
                    '</div>' +
                    '<div class="cart-item-info">' +
                        '<div>' + name + '</div>' +
                        config_str +
                        '<div id="sidecart-quantity-' + id + '-' + config + '">Количество: ' + quantity + '</div>' +
                        '<div>Цена: ' + price + ' RUB</div>' +
                    '</div>' +
                    '<div class="delete-cross-wrap">' +
                        '<form class="cart-remove-item sidecart" action="" method="post">' +
                            '<input name="csrfmiddlewaretoken" type="hidden" ' +
                            'value="' + document.querySelector("[name=csrfmiddlewaretoken]").value + '">' +
                            '<input type="hidden" class="choco-pk" value="' + id + '">' +
                            '<input type="hidden" class="config-pk" value="' + config + '">' +
                            '<input type="submit" value="✕">' +
                        '</form>' +
                    '</div>' +
                '</div>' +
            '</div>');
}
