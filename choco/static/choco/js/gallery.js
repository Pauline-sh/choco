window.addEventListener("load", () => {
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