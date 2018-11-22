"use strict";

class CatalogModal {
    constructor() {
        this.modalNode = document.getElementById("catalog-modal");
        this.modalContent = $("#catalog-modal-main");

        this.modalNode.getElementsByClassName("close-modal-outside")[0].addEventListener("click", () => {
            this.hide();
        })
    }

    show() {
        this.modalNode.style.display = "block";
    }

    hide() {
        this.modalNode.style.display = "";
        this.clear();
    }

    fill(data) {
        for (let item of data) {
            this.modalContent.append(this.makeTemplate(item));
        }
    }

    makeTemplate(item) {
        return(`<div class="item-wrap">
                    <div class="item-image">
                        <a href="/catalog/${item.id}" target="_blank">
                            <img src="/static/choco/choco_pics/${item.choco_dir}/${item.choco_pic}"/>
                        </a>
                    </div>
                    <div class="item-info">
                        <a href="/catalog/${item.id}" target="_blank"><strong>${item.choco_name}</strong></a>
                        <span class="price">${item.choco_price} RUB</span>
                    </div>
                    <form action="/add/${item.id}/" method="post" class="cart-add-form">
                        <input name="csrfmiddlewaretoken" type="hidden" value="${document.querySelector("[name=csrfmiddlewaretoken]").value}">
                        <div class="placeholder"></div>
                        <label class="quantity">
                            <input type="number" name="quantity" value="1" required="" id="id_quantity" min="1">
                            <a href="#" class="quantity-up"></a>
                            <a href="#" class="quantity-down"></a>
                        </label>
                        <input type="hidden" class="choco-pk" value="${item.id}">
                        <input type="submit" value="Добавить в набор">
                        <div class="placeholder"></div>
                    </form>
                </div>`);
    }

    clear() {
        this.modalContent.empty();
    }
}

window.addEventListener("load", () => {
    let choco_catalog = document.getElementById("open-choco-catalog");
    let beresta_catalog = document.getElementById("open-beresta-catalog");
    let wood_catalog = document.getElementById("open-wood-catalog");
    let catalog_modal = new CatalogModal();

    choco_catalog.addEventListener("click", openCatalog(1, catalog_modal));
    beresta_catalog.addEventListener("click", openCatalog(2, catalog_modal));
    wood_catalog.addEventListener("click", openCatalog(3, catalog_modal));
});

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

function openCatalog(categoryId, modal){
    return function(e) {
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        //let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        $.ajax({
            url: "get_items/" + categoryId + "/",
            type: "POST",
            dataType: "json",
            
            headers: {
                "X-CSRFToken": csrftoken
            },

            success: function(json) {
                console.log(json);
                modal.fill(json);
                modal.show();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}
