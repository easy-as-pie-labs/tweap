
$( document ).ready(function() {
        $("a, p, span, table, h1, h2, h3, input").hover(function() {
            if (Math.floor(Math.random() * (50)) < 10) {
                console.log("go wild!");
                var index = Math.floor(Math.random() * (classes.length));
                $(this).toggleClass(classes[index] + "  animated");
            }
            else{
                console.log("no animation this time!");
            }
        });

var classes = [
    "bounce",
    "flash",
    "pulse",
    "rubberBand",
    "shake",
    "swing",
    "tada",
    "wobble",
    "bounceIn",
    "bounceInDown",
    "bounceInLeft",
    "bounceInRight",
    "bounceInUp",
    "fadeIn",
    "fadeInDown",
    "fadeInDownBig",
    "fadeInLeft",
    "fadeInLeftBig",
    "fadeInRight",
    "fadeInRightBig",
    "fadeInUp",
    "fadeInUpBig",
    "flipInX",
    "flipInY",
    "flipOutX",
    "flipOutY",
    "lightSpeedIn",
    "lightSpeedOut",
    "rotateIn",
    "rotateInDownLeft",
    "rotateInDownRight",
    "rotateInUpLeft",
    "rotateInUpRight",
    "hinge",
    "rollIn",
    "zoomIn",
    "zoomInDown",
    "zoomInLeft",
    "zoomInRight",
    "zoomInUp",
    "zoomOut",
    "zoomOutDown",
    "zoomOutLeft",
    "zoomOutRight",
    "zoomOutUp",
    "slideInDown",
    "slideInLeft",
    "slideInRight",
    "slideInUp",
    "slideOutDown",
    "slideOutLeft",
    "slideOutRight",
    "slideOutUp"];

});

