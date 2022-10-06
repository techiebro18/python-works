jQuery(document).ready(function($) {

	$('.mainmenu ul li.parent > a').after('<span class="childlink"><i class="fa fa-angle-down"></i></a>');
	$('.menulinks').click(function() {
		$(this).next('ul').slideToggle(250);
		$('body').toggleClass('mobile-open');
		$('span.childlink').removeClass('child-open');
		return false;
	});

	$('span.childlink').click(function() {
		$(this).parent().siblings('ul').find('span.childlink').removeClass('child-open');
		$(this).parent().siblings('ul').slideUp(250);
		$(this).next('ul').slideToggle(250);
		$(this).toggleClass('child-open');

		return false;
	});


	$(".backtotop").click(function(){
		$('html, body').animate({scrollTop:0},800,'linear');
	});


	$('.bg-img').each(function() {
		var imgSrc = $(this).find('img').attr('src');
		$(this).css('background-image', 'url(' + imgSrc + ')');
	});

	$('.homeheader-slider').slick({
		arrows: false,
		dots: true
	});

/*	$('.homeheader-slider').slick({
		arrows: false,
		asNavFor: '.homeheader-slider-tab',
		responsive: [
		{
		  breakpoint: 767,
		  settings: {
			dots: true
		  }
		}]
	});

	$('.homeheader-slider-tab').slick({
		slidesToShow: 5,
		slidesToScroll: 1,
		asNavFor: '.homeheader-slider',
		focusOnSelect: true,
		responsive: [
		{
		  breakpoint: 1224,
		  settings: {
			slidesToShow: 4,
			slidesToScroll: 1
		  }
		}]
	});*/


	$('.productlist-slider').slick({
	  speed: 300,
	  slidesToShow: 5,
	  slidesToScroll: 1,
	  responsive: [
		{
		  breakpoint: 1224,
		  settings: {
			slidesToShow: 4,
			slidesToScroll: 1
		  }
		},
		{
		  breakpoint: 1024,
		  settings: {
			slidesToShow: 3,
			slidesToScroll: 1
		  }
		},
		{
		  breakpoint: 767,
		  settings: {
			slidesToShow: 2,
			slidesToScroll: 1
		  }
		},
		{
		  breakpoint: 520,
		  settings: {
			slidesToShow: 1,
			slidesToScroll: 1
		  }
		}
	  ]
	});
    $('.productlist-sliders').slick({
        speed: 300,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1224,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 520,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
    $('.productlists-slider').slick({
        speed: 300,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1224,
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 520,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            }
        ]
    });



	$(".search-link").click(function(){
		$('.locationoffers-section').addClass('search-open');
	});

	$('.product-tab-link a').click(function() {
			$('.productab-content').removeClass('active');
			$('.product-tab-link a').removeClass('active');
			$(this).addClass('active');
			var content = $(this).attr('rel');
			$('#' + content).addClass('active');
  });


});


jQuery(window).bind('scroll resize load', function() {

	if (jQuery(this).scrollTop() > 35) {
		jQuery('.top').addClass('fixed');
		jQuery('.mainmenu').addClass('fixed');
	} else {
		jQuery('.top').removeClass('fixed');
		jQuery('.mainmenu').removeClass('fixed');
	}

});

jQuery(window).load(function() {

	jQuery('.matchheight').matchHeight();

});

jQuery(window).resize(function() {

	jQuery('.matchheight').matchHeight();


});


