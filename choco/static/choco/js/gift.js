"use strict";

class CatalogModal {
    constructor() {
        this.modalNode = document.getElementById("catalog-modal");
        this.modalContent = document.getElementById("catalog-modal-main");
        this.pages = [];
        this.ITEMS_ON_PAGE = 15;

        this.modalNode.getElementsByClassName("close-modal-outside")[0].addEventListener("click", () => {
            this.hide();
        })
    }

    show() {
        this.modalNode.style.display = "block";
    }

    hide() {
        this.modalNode.style.display = "";
        this.clearAll();
    }

    fill(data) {
        const numPages = Math.ceil(data.length / this.ITEMS_ON_PAGE);
        this.pages = Array(numPages).fill(null);
        this.makePages(numPages,data);
        if (numPages > 1) {
            this.makePagination(numPages)
        };

        this.showPage(1);
    }

    makePagination(pages) {
        this.modalContent.insertAdjacentHTML("afterend", '<div class="pagination"></div>');
        document.querySelector(".pagination").insertAdjacentHTML(
            "beforeend",
            `<div class="button-container active">
                <a href="#" data-pagenum="1">1</a>
            </div>`)
        
        for (let i = 2; i <= pages; i++) {
            document.querySelector(".pagination").insertAdjacentHTML(
                "beforeend",
                `<div class="button-container">
                    <a href="#" data-pagenum="${i}">${i}</a>
                </div>`)
        }

        const pageBtns = document.querySelectorAll(".button-container > a");
        for (const btn of pageBtns) {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                document.querySelector(".button-container.active").classList.remove("active");
                e.target.parentNode.classList.add("active");
                $('#catalog-modal').animate({
                    scrollTop: "0px"
                }, 500);

                this.showPage(Number(e.target.dataset.pagenum));
            })
        }
    }

    makePages(pages,data) {
        for (let i = 0; i < pages; i++) {
            this.pages[i] = Array(this.ITEMS_ON_PAGE);

            for (let j = 0; j < this.ITEMS_ON_PAGE; j++) {
                this.pages[i][j] = data[j + i * this.ITEMS_ON_PAGE];
            }
        }
        //console.log(this.pages);
    }

    showPage(num) {
        this.clearPage();

        const pageArr = this.pages[num - 1];
        for (const item of pageArr) {
            if (!item) break;
            this.modalContent.insertAdjacentHTML("beforeend",this.makeTemplate(item));
        }
        
        this.addItemEvents();
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
                    <form action="" method="post" class="gift-add-form">
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

    addItemEvents() {
        const ups = this.modalContent.getElementsByClassName("quantity-up");
        const downs = this.modalContent.getElementsByClassName("quantity-down");
        const giftAddForms = this.modalContent.getElementsByClassName("gift-add-form");
        for (const btn of ups) {
            btn.addEventListener("click", quantityUp);
        }
        for (const btn of downs) {
            btn.addEventListener("click", quantityDown);
        }
        for (const form of giftAddForms) {
            form.addEventListener("submit", addToGift(this));
        }
    }

    clearPage() {
        while(this.modalContent.firstChild) {
            this.modalContent.removeChild(this.modalContent.firstChild);
        }
    }

    clearAll() {
        this.clearPage();
        this.pages = [];
        if (document.querySelector(".pagination")) {
            document.querySelector(".pagination").remove();
        }
    }
}

function addToGift(modal) {
    // TODO: когда добавляешь второй предмет, цена первого должна зачеркиваться и показываться со скидкой
    return function(e) {
        e.preventDefault();

        // if configuration is not chosen it is set to -1 and back-end sets it to the first found config in db
        let itemId = e.target.getElementsByClassName("choco-pk")[0].value,
            configId = -1;
        let configClassItems = e.target.getElementsByClassName("config-pk");
        if(configClassItems.length > 0){
            configId = configClassItems[0].firstElementChild.value
            if(!isInt(configId))
                configId = -1;
        }

        let csrftoken = getCookie('csrftoken');
        let newValue = e.target.getElementsByClassName("quantity")[0].firstElementChild.value;

        $.ajax({
            url: "add/" + itemId + "/",
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
                const item = json.new_item;

                if(!isDuplicate(item)) {
                    $("#gift-body").append(makeGiftItemTemplate(item, json.total_items));
                    $("#gift-body")[0].lastElementChild.querySelector(".gift-remove-item").addEventListener("click", removeFromGift);
                } else {
                    const giftElem = document.querySelector(`#product-${item.product.id}-${item.configuration}`);
                    giftElem.querySelector(".item-quantity").innerHTML = "Количество: " + item.quantity + ";";
                }
                $("#total-number").text(json.total_price);
                //console.log(json);
                modal.hide();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                modal.hide();
            }
        });
    }

    function isDuplicate(newItem) {
        return Boolean(document.querySelector(`#product-${newItem.product.id}-${newItem.configuration}`));
    }
}

function removeFromGift(e) {
    e.preventDefault();
    let itemId = e.target.parentNode.getElementsByClassName("choco-pk")[0].value;
    let configId = e.target.parentNode.getElementsByClassName("config-pk")[0].value;
    let csrftoken = getCookie('csrftoken');

    //console.log(itemId, configId);

    $.ajax({
        url: "remove/" + itemId + "/" + configId + "/",
        type: "POST",
        dataType: "json",

        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function(json) {
            if (json.result == 'OK') {
                //removing from the cart page
                let itemContainer = e.target.parentNode.parentNode.parentNode;
                itemContainer.style.opacity = 0;

                setTimeout(() => {
                    $('#product-' + itemId + '-' + configId).remove();
                }, 500);
                //console.log(json);
                $("#total-number").text(json.total_price);
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function makeGiftItemTemplate(item, total_items) {
    // TODO: если total_items меньше 2 то не зачеркивать и не делать скидку
    return (`<div class="gift-item" id="product-${item.product.id}-${item.configuration}">
    <div class="wrapper">
        <div class="img-container">
            <img src="/static/choco/choco_pics/${item.product.choco_dir}/${item.product.choco_pic}"/>
        </div>
        <div class="item-info">
            <div class="title">${item.product.choco_name}</div>
            <div class="price">
                Цена: 
                <strike>${item.product.choco_price} RUB</strike> 
                ${(Number(item.product.choco_price) * 0.90).toFixed(2)} RUB</div>
                <div class="additional-info">
                    <span class="item-quantity">Количество: ${item.quantity};</span>
                    ${stringifyConfig(item.conf_object)}
                </div>
        </div>
            <div class="delete-cross-wrap">
                <input class="gift-remove-item" type="submit" value="✕">
                <input type="hidden" class="choco-pk" value="${item.product.id}">
                <input type="hidden" class="config-pk" value="${item.configuration}">
            </div>
        </div>
    </div>`);
}

function orderGift(e) {
    e.preventDefault();

    let packageRadios = document.getElementsByName('package');
    let packageValue = -1
    for (let packageRadio of packageRadios) {
        if (packageRadio.checked) {
            packageValue = packageRadio.value;
        }
    }
    if(packageValue == -1) {
        alert("Нужно выбрать вид упаковки!");
        return;
    }

    $.ajax({
        url: "state/",
        type: "POST",
        dataType: "json",

        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        data: {
            packageValue: packageValue,
        },
        success: function(json) {
            if(json.result == 'OK') {
                window.location = "order";
            }
            else{
                alert(json.error);
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

window.addEventListener("load", () => {
    let choco_catalog = document.getElementById("open-choco-catalog");
    let beresta_catalog = document.getElementById("open-beresta-catalog");
    let wood_catalog = document.getElementById("open-wood-catalog");
    let catalog_modal = new CatalogModal();

    let packageRadios = document.getElementsByName('package');
    for (let packageRadio of packageRadios) {
        packageRadio.addEventListener("click", setPackage);
    }

    let orderGiftBtn = document.getElementById("gift-checkout-btn");

    let removeCrosses = document.getElementsByClassName("gift-remove-item");
    for (let cross of removeCrosses) {
        cross.addEventListener("click", removeFromGift);
    }

    choco_catalog.addEventListener("click", openCatalog(1, catalog_modal));
    beresta_catalog.addEventListener("click", openCatalog(2, catalog_modal));
    wood_catalog.addEventListener("click", openCatalog(3, catalog_modal));

    orderGiftBtn.addEventListener("submit", orderGift);
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
        $.ajax({
            url: "get_items/" + categoryId + "/",
            type: "POST",
            dataType: "json",
            
            headers: {
                "X-CSRFToken": csrftoken
            },

            success: function(json) {
                //console.log(json);
                modal.fill(json);
                modal.show();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}

function stringifyConfig(conf) {
    let confStr = "";
    if (conf.size) confStr += `Размер: ${conf.size}; `;
    if (conf.weight) confStr += `Вес: ${conf.weight} г; `;
    if (conf.diameter) confStr += `Диаметр: ${conf.diameter} см; `;
    if (conf.height) confStr += `Высота: ${conf.height} см; `;
    if (conf.width) confStr += `Ширина: ${conf.width} см; `;
    if (conf.length) confStr += `Длина: ${conf.length} см; `;
    return confStr;
}

function setPackage(e) {
    e.preventDefault();
    let packageId = e.target.value;
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        url: "get_total_price/" + packageId + "/",
        type: "POST",
        dataType: "json",

        headers: {
            "X-CSRFToken": csrftoken
        },

        success: function(json) {
            //console.log(json);
            e.target.checked = true;
            $("#total-number").text(json.total_price);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}
