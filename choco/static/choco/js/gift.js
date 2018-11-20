"use strict";

window.addEventListener("load", () => {
    let choco_catalog = document.getElementById("open-choco-catalog");
    let beresta_catalog = document.getElementById("open-beresta-catalog");
    let wood_catalog = document.getElementById("open-wood-catalog");

    choco_catalog.addEventListener("click", openCatalog(1));
    beresta_catalog.addEventListener("click", openCatalog(2));
    wood_catalog.addEventListener("click", openCatalog(3));
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

function openCatalog(categoryId){
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
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
}
