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

function removeSidecartItem(e) {
    e.preventDefault();
    let itemId = e.target.getAttribute("remove"),
        configId = e.target.getAttribute("configure");
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    let itemContainer = e.target.parentNode.parentNode.parentNode;

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
            setTimeout(() => {
                itemContainer.style.display = "none";
            }, 500);
            console.log(JSON.stringify(json));
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
} 
