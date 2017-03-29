 $('.your-class').slick({
  dots: false,
  infinite: false,
  speed: 300,
  slidesToShow: 3,
  slidesToScroll: 1,
  initialSlide: 3,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        arrows: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        initialSlide: 5
      }
    },
    {
      breakpoint: 960,
      settings: {
        arrows: true,
        slidesToShow: 1,
        slidesToScroll: 2,
        initialSlide: 6
      }
    }
    
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ]
});