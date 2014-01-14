window.onload = function() {

  // create and initialize a 3D renderer
  var r = new X.renderer3D();
  r.container = 'render'
  r.init();
   
  // create a cube
  cube = new X.cube();
  
  // setting the edge length can also be skipped since 20 is the default
  cube.lengthX = cube.lengthY = cube.lengthZ = 20;
  
  // can also be skipped since [0,0,0] is the default center
  cube.center = [0, 0, 0];
  
  // [1,1,1] (== white) is also the default so this can be skipped aswell
  cube.color = [1, 1, 1];
  r.add(cube)
  r.render();
  
};

jQuery(function() {

  var smallHeight = '40px'
  var bigHeight = '150px'

  jQuery('.menu').stop().animate({
    'marginLeft': '-195px',
    'height': smallHeight
  }, 200);
  

  $(document.body).on ( 'mouseenter', '.menu', function(event) {

    console.log ( "mouseenter ", jQuery(this) )
    if (jQuery('.menu', jQuery(this)).hasClass('menuDisabled')) {
      // if this menu is disabled, don't slide
      return;
    }
    console.log ( "sliding out ", jQuery(this) )
    jQuery(this).stop().animate({
      'marginLeft': '-2px',
      'height': bigHeight
    }, 200);
    
  } )

$(document.body).on ( 'mouseleave', '.menu', function(event) {

    console.log ( "mouseenter ", jQuery(this) )
    if (jQuery('.menu', jQuery(this)).hasClass('menuDisabled')) {
      // if this menu is disabled, don't slide
      return;
    }
    console.log ( "sliding in ", jQuery(this) )
    jQuery(this).stop().animate({
      'marginLeft': '-195px',
      'height': smallHeight
    }, 200);
    
  } )



  jQuery('.navigationLi').hover(function() {

    if (jQuery('.menu', jQuery(this)).hasClass('menuDisabled')) {
      // if this menu is disabled, don't slide
      return;
    }
    
    if (jQuery('.miniColors-selector').length > 0) {
      
      // color dialog is active, don't slide
      return;
      
    }
    
    jQuery('.menu', jQuery(this)).stop().animate({
      'marginLeft': '-2px',
      'height': bigHeight
    }, 200);
    
  }, function() {

    if (jQuery('.pinicon', jQuery(this)).hasClass('ui-icon-pin-s')) {
      // if pinned, don't slide in
      return;
    }
    
    if (jQuery('.miniColors-selector').length > 0) {
      
      // color dialog is active, don't slide
      return;
      
    }
    
    jQuery('.menu', jQuery(this)).stop().animate({
      'marginLeft': '-195px',
      'height' : smallHeight
    }, 200);
    
  });
  
  jQuery('.pin').click(
      function() {

        jQuery('.pinicon', jQuery(this)).toggleClass('ui-icon-pin-w')
            .toggleClass('ui-icon-pin-s');
        
      });
  

  
});
