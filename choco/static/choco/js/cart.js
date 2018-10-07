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
            reloadSideCart(json.new_item, json.static_dir);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

    console.log("form submitted!");  // sanity check
}

// TODO:: sidecart reload, two cases 1. cart was empty 2. cart had no such items 3. sidecart had such item (update quantity)
function reloadSideCart(new_item, static_dir){
    let sideCartContentClass = document.getElementById("side-cart").getElementsByClassName("cart-content");
    if(sideCartContentClass.length > 0){
        let sideCartContent = sideCartContentClass[0];
        // cart was empty
        if(sideCartContent.firstElementChild.classList.contains("cart-empty")){
            console.log("cart was empty");
            console.log(static_dir);
            let img = document.createElement("img");
            img.setAttribute("src", static_dir + "default.png")
            sideCartContent.append(img);
        }
        else{
            console.log("cart had items");
            console.log(new_item);
            let new_item_str = '<div class="cart-item"><div class="wrapper"><div class="cart-item-image">';
            new_item_str += '<img src="' + static_dir + 'default.png"/>'
            new_item_str += '</div></div></div>';
            $("#cart-content").append(new_item_str);
        }
/*
            new_item_str = '<div class="cart-item"><div class="wrapper"><div class="cart-item-image">';
            if(!new_item.product.choco_pic){
                new_item_str += <img src="{% static 'choco/choco_pics/default.png' %}"/>
            }
            else{

            }
            new_item_str += '</div></div></div>';
            sideCartContent.append(
                <div class="cart-item">
                    <div class="wrapper">
                        <div class="cart-item-image">
                            {% if not product.choco_pic %}
                                <img src="{% static 'choco/choco_pics/default.png' %}"/>
                            {% else %}
                                {% with "choco/choco_pics/"|add:product.choco_dir|add:"/"|add:product.choco_pic as main_pic %}
                                    <img src="{% static main_pic %}"/>
                                {% endwith %}
                            {% endif %}
                        </div>
                        <div class="cart-item-info">
                            <div>{{ product.choco_name }}</div>
                            {% with configuration=item.conf_object %}
                                <div>Вес: {{ configuration.choco_weight }}</div>
                            {% endwith %}
                            <div>Количество: {{ item.quantity }}</div>
                            <div>Цена: {{ item.total_price }} RUB</div>
                        </div>
                        <div class="delete-cross-wrap">
                            <a href="#" class="delete-cross" remove="{{product.id}}" configure="{{item.configuration}}">✕</a>
                        </div>
                    </div>
                </div>
            );
        }
        */
    }
}
