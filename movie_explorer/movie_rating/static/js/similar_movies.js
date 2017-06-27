function next() {
    var container = document.querySelector("#similar-movies-container");
    var value = document.querySelector("#translate-value");//225
    var divs = container.querySelectorAll("#movie-post");
    if(value.value > -225 * divs.length + container.offsetWidth) {
        value.value = value.value - 225;
        container.style.transform = "translateX(" + value.value + "px)";
    }
}

function prev() {
    var container = document.querySelector("#similar-movies-container");
    var value = document.querySelector("#translate-value");
    if(value.value < 0) {
        value.value = value.value - (-225);
        container.style.transform = "translateX(" + value.value + "px)";
    }
}