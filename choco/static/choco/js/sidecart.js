"use strict";

window.addEventListener("load", () => {
    document.getElementById("open-cart").addEventListener("click", openCart);
    document.getElementById("close-cart").addEventListener("click", closeCart);
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