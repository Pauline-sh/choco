"use strict";

window.addEventListener("load", () => {
    let ups = document.getElementsByClassName("quantity-up");
    let downs = document.getElementsByClassName("quantity-down");

    for (let btn of ups) {
        btn.addEventListener("click",quantityUp);
    }

    for (let btn of downs) {
        btn.addEventListener("click",quantityDown);
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
