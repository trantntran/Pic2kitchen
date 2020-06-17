$( document ).ready(function() {
    $('.camera').click(function() {
    	$('.list-products').addClass('active');
    	$('.camera-container').css('display', 'none');
    });

    $('.carousel-inner').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    fade: true,
    prevArrow: '<a class="slick-prev carousel-control-prev"><span class="carousel-control-prev-icon"></span></a>',
    nextArrow: '<a class="slick-next carousel-control-next"><span class="carousel-control-next-icon"></span></a>'
});
});