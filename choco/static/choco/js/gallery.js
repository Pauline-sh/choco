window.addEventListener("load", () => {
    
    /* workaround for django <select> bug */
    if (document.querySelector('select[name="configuration"]')) {
        document.querySelector('select[name="configuration"]').firstElementChild.innerHTML = "Выберите характеристики";
    }

    if (!document.getElementById("gallery-selection")) return;

    let pictures = document.getElementsByClassName("gallery-small");
    for (let pic of pictures) {
        pic.addEventListener("click", replaceMainPic);
    }
})

function replaceMainPic(e) {
    let imglink = e.target.src;
    document.getElementById("gallery-main").firstElementChild.src = imglink;
}