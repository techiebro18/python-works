function menubar() {
    openmenu = 0, $(document).ready(function () {
        $(".topLink").mouseenter(function () {
            var t = $(this);
            0 == openmenu ? timer1 = setTimeout(function () {
                t.addClass("openMenu")
            }, 200) : t.addClass("openMenu")
        }), $(".topLink").mouseleave(function () {
            $(this).removeClass("openMenu"), "undefined" != typeof timer1 && clearTimeout(timer1), openmenu = 1, timer2 = setTimeout(function () {
                openmenu = 0
            }, 200)
        }), $(".levelSecond>div").mouseenter(function () {
            var t = $(this);
            timer = setTimeout(function () {
                $(".openMenu .subMenuOpen").removeClass("subMenuOpen"), t.addClass("subMenuOpen")
            }, 200)
        }), $(".levelSecond>div").mouseleave(function () {
            clearTimeout(timer)
        }), $(".loginMenu").mouseenter(function () {
            $(this).addClass("open")
        }), $(".loginMenu").mouseleave(function () {
            $(this).removeClass("open")
        })
    })
}


function headerfunction() {
    var t = $("#desktopheader");
    $clone = t.before(t.clone().addClass("clone")), $("header.clone>nav").remove(), $("header.clone").find("#cartbigbutton").attr("id", "cartbuttonclone"), $(window).scroll(function () {
        var t = $(window).scrollTop();
        $("body").toggleClass("down", t > 200)
    })
}

function imageloadfade() {
    var t = document.querySelectorAll(".productImg img");
    Array.prototype.map.call(t, function (t) {
        t.complete ? t.className = "loaded" : t.addEventListener("load", function () {
            t.className = "loaded"
        })
    })
}

function nanofunction() {
    nanobar = new Nanobar
}

function accountpage() {
    $(document).ready(function () {
        $(window).scroll(function () {
            var t = $(".boxLeftWrap"),
                e = $(".trustBar").offset().top - 17;
            t.offset().top, t.outerHeight();
            $(window).scrollTop() < $(".boxRightWrap").offset().top ? (t.css("position", ""), t.css("top", "")) : $(window).scrollTop() < $(".boxRightWrap").offset().top + 140 - 80 ? (t.css("position", "fixed"), t.css("top", 80 * ($(window).scrollTop() - $(".boxRightWrap").offset().top) / 60)) : $(window).scrollTop() > e - t.outerHeight() - 80 ? (t.css("top", e - t.outerHeight()), t.css("position", "absolute")) : (t.css("position", "fixed"), t.css("top", 80))
        })
    })
}

function productpage() {
    $(document).ready(function () {
        $(window).scroll(function () {
            var t = $(".combosWrapInner"),
                e = $(".reviewRatingWrap").offset().top + $(".reviewRatingWrap").height();
            t.offset().top, t.outerHeight();
            $(window).scrollTop() < $(".similarProductComboOption").offset().top + 60 - 80 ? (t.css("position", ""), t.css("top", "")) : $(window).scrollTop() > e - t.outerHeight() - 80 ? (t.css("top", e - t.outerHeight() - $("#ComboProductBlock").offset().top), t.css("position", "absolute")) : (t.css("position", "fixed"), t.css("top", 80))
        }), $(document).on("mouseenter", ".thumbImg", function () {
            $(".thumbImg").removeClass("selected"), $(this).addClass("selected"), currentId = $(this).attr("id"), currentImgID = "#m_" + currentId, $(".imgMainItem").removeClass("currentImg"), $(currentImgID).addClass("currentImg"), 0 == $(this).hasClass("thumbImgVideo") && zoomImg()
        }), $(window).scroll(function () {
            $(this).scrollTop() > 400 ? $(".scrollup").fadeIn() : $(".scrollup").fadeOut()
        }), $(".scrollup").click(function () {
            $("html, body").animate({
                scrollTop: 0
            }, 600)
        }), $(".smoothScroll").click(function () {
            var t = $(this).attr("data-target");
            $("html, body").animate({
                scrollTop: $(t).position().top - 65
            }, 600)
        })
    })
}

function cartSizing() {
    $(".shoppingCartRemodal").parents(".remodal-wrapper").addClass("shoppingCartWrap")
}

function topFixedDetailTab() {
    $(window).scroll(function () {
        var t = $(window).scrollTop();
        $(".tabHeadingWrap").toggleClass("showTabHeading", t > $(".similarProductComboOption").offset().top - 46)
    }), $(document).on("click", ".smoothScroll", function () {
        var t = $(this).attr("data-target");
        $("html, body").animate({
            scrollTop: $(t).offset().top - 65
        }, 600)
    })
}

function homepagemobile() {
    $(document).ready(function () {
        $(".healthmugMessageScreen").css("height", $(window).height()), $(".mobile").click(function () {
            $(".healthmugMessageScreen").fadeIn()
        }), $(".gotIt").click(function () {
            $(".healthmugMessageScreen").fadeOut()
        })
    })
}



function waveinitialize() {
    $(".wavelet,.waveletLight").click(function (t) {
        if ($(this)[0] == $(t.target).closest(".wavelet,.waveletLight")[0]) {
            var e = $(this)[0].getBoundingClientRect(),
                n = e.left,
                o = e.top,
                i = e.width,
                r = e.height;
            i >= r ? r = i : i = r, $(this).prepend("<div class='rippleBox' style='position:absolute;z-index:1;top:0px;left:0px;overflow:hidden;width:" + e.width + "px;height:" + e.height + "px'><span class='ripple'></span></div>");
            var s = t.clientX - n - i / 2,
                a = t.clientY - o - r / 2;
            $(".ripple").css({
                width: i,
                height: r,
                top: a + "px",
                left: s + "px"
            }).addClass("rippleEffect"), setTimeout(function () {
                $(".rippleBox").remove()
            }, 600)
        }
    })
}
