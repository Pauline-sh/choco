window.addEventListener("load", () => {
    
    /* workaround for django <select> bug */
    if (document.querySelector('select[name="configuration"]')) {
        document.querySelector('select[name="configuration"]').firstElementChild.innerHTML = "Выберите характеристики";
    }

    //document.getElementById("gallery-main").addEventListener("click",openImgModal);

    $(".img-zoomable").each(function() {
        this.addEventListener("click",openImgModal);
    })
    
    document.getElementById("img-modal").addEventListener("click", closeModal);
    $(".close-modal").each(function() {
        this.addEventListener("click", closeModal);
    })

    let pictures = document.getElementsByClassName("gallery-small");
    for (let pic of pictures) {
        pic.addEventListener("click", replaceMainPic);
    }
})

function replaceMainPic(e) {
    let imglink = e.target.src;
    document.getElementById("gallery-main").firstElementChild.src = imglink;
}

function openImgModal(e) {
    let imglink = e.target.src;
    document.querySelector("#img-modal img").src = imglink;
    document.querySelector("#img-modal").style.display = "block";
}

function closeModal(e) {
    /* clicking outside the modal */
    if (e.target.parentNode == document.body) {
        e.target.style.display = "none";
        return;
    }

    /* clicking the close button */
    if (e.target.classList.contains("close-modal")) {
        e.target.parentNode.parentNode.style.display = "none";
    }
}