"use strict";

window.addEventListener("load", () => {
    document.getElementById("open-cart").addEventListener("click", openCart);
    document.getElementById("close-cart").addEventListener("click", closeCart);

    let crosses = document.getElementsByClassName("delete-cross");
    for (let cross of crosses) {
        cross.addEventListener("click", removeSidecartItem);
    }
})

function openCart(e) {
    e.preventDefault();
    document.getElementById("side-cart").style.width = "30%";

    let items = document.getElementsByClassName("cart-item");
    setTimeout(() => {
        for (let item of items) {
            item.style.whiteSpace = "normal";
        }
    }, 350);
}

function closeCart(e) {
    e.preventDefault();
    document.getElementById("side-cart").style.width = "0";

    let items = document.getElementsByClassName("cart-item");
    for (let item of items) {
        item.style.whiteSpace = "nowrap";
    }
}

function removeSidecartItem(e) {
    e.preventDefault();
    let itemId = e.target.getAttribute("remove");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let itemContainer = e.target.parentNode.parentNode.parentNode;

    $.ajax({
        url: "/remove/" + itemId + "/",
        type: "POST",
        dataType: "json",
        data: {
            itemId: itemId,
        },
        
        headers:{
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            /* красивая анимация goes here */
            itemContainer.style.display = "none";
            console.log(JSON.stringify(json));
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
} 