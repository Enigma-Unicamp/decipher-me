// dropdown menu
document.addEventListener('DOMContentLoaded', function() {

  var elems = document.querySelectorAll('.dropdown-trigger');
  var options = {
    inDuration: 300,
    outDuration: 0,
    constrain_width: false,
    hover: false,
    gutter: 0,
    coverTrigger: false,
    alignment: 'left'
  }
  var instances = M.Dropdown.init(elems, options);
});


// dropdown menu close with outside click
document.addEventListener('click', function(e) {

  // if it's the dropdown menu being clicked
  // we shouldn't hide anything
  var icon = document.getElementById('dropdown-icon');
  if (e.target !== icon) {

    var dropdown = document.querySelectorAll('.dropdown-trigger');
    for (i=0; i<dropdown.length; i++) {

      // if none the icon or the menu is being clicked,
      // close all dropdown menus
      if (! dropdown[i].isEqualNode(e.target)) {
        var instance = M.Dropdown.getInstance(dropdown[i]);
        instance.close();
      }
    }
  }
});
