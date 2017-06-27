//youtube function

function open_popup() {
    // If element DNE
    if ($('#youtube-pop-video').length == 0) {
        var div = document.createElement('div');
        div.setAttribute('id', 'youtube-pop-video');
        document.body.append(div);
    }

    $('body').css("overflow", "hidden");

    $('#youtube-pop-video').css({
        "background-color": "rgba(0, 0, 0, 0.5)",
        "position": "absolute",
        "top": $("body").scrollTop(),
        "text-align": "center",
        "width": "100%",
        "height": "100%",
        "z-index": "1100",
    });

    var div = document.createElement("div");
    div.setAttribute("style", "padding-right:200px;float:right;font-size:40px");

    var x = document.createElement("i");
    x.setAttribute("class", "fa fa-times");
    x.setAttribute("aria-hidden", "true");
    x.setAttribute("style", "color:rgba(250,250,250,0.8); cursor: pointer;");

    var iframe = document.createElement('iframe');
    iframe.setAttribute('src', $('.youtube-pop-up').attr('href').replace("watch?v=", "embed/"));
    iframe.setAttribute('width', "70%");
    iframe.setAttribute('height', "600");
    iframe.setAttribute('frameborder', "0");

    div.appendChild(x);
    $('#youtube-pop-video').append(div);
    $('#youtube-pop-video').append("<br>");
    $('#youtube-pop-video').append("<br>");
    $('#youtube-pop-video').append("<br>");
    $('#youtube-pop-video').append(iframe);

    $(".fa-times").click(function () {
        $("body").css("overflow", "initial");
        $('#youtube-pop-video').remove();
    });
}