function search_resize() {
    var search = document.getElementById("search_settings");
    var up = document.getElementById("up");
    var down = document.getElementById("down");
    search.classList.toggle("resize");
    up.classList.toggle("link_hidden");
    down.classList.toggle("link_hidden");
}