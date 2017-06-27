/**
 * Created by arthur on 3/11/2017.
 */
//section.playing-movies > div

setTimeout(showDiv, 300);

function showDiv() {
    var divs = document.querySelectorAll("div.hidden-movie");
    if(divs.length > 0) {
        divs[0].classList.add("shown-movie");
        divs[0].classList.remove("hidden-movie");
        setTimeout(showDiv, 150);
    }
}