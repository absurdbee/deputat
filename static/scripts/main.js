on('body', 'click', '.show_parent_next_element', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('body', 'click', '.map_selector', function() {
  slug = this.getAttribute("data-slug");
  text = this.querySelector("title").innerHTML;
  console.log(slug + " detected!");
  map = this.parentElement;
  svg_list = map.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    svg_list[i].style.fill = "rgba(0,0,0,0.15)";
  };
  this.style.fill = "#897FF1";
  col_md_3 = this.parentElement.parentElement.nextElementSibling;
  block = col_md_3.querySelector("#elect_for_regions_loader");
  col_md_3.querySelector("#select_regions").value = text;

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/list/region/" + slug + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
            block.innerHTML = link.responseText;

        }
    }
};
link.send( null );
})

on('body', 'click', '.select_elect_news_category', function() {
  _this = this;
  if (_this.classList.contains("active")){
    return
  }
  elect_news_container = document.body.querySelector(".elect_news_container");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _this.getAttribute("data-href"), true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          links = _this.parentElement.parentElement.querySelectorAll(".select_elect_news_category");
          for (var i = 0; i < links.length; i++){
            links[i].classList.remove("active");
          }
          elem = link.responseText;
          response = document.createElement("span");
          response.innerHTML = elem;
          _this.classList.add("active");
          elect_news_container.innerHTML = "";
          elect_news_container.insertAdjacentHTML('afterBegin', response.innerHTML);
        }
    }
};
link.send( null );
})

on('body', 'click', '.main_nav', function() {
  _this = this;
  if (_this.classList.contains("active")){
    return
  }
  container = _this.parentElement.parentElement.parentElement.nextElementSibling;
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _this.getAttribute("data-href"), true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          links = _this.parentElement.querySelectorAll(".main_nav");
          for (var i = 0; i < links.length; i++){
            links[i].classList.remove("active");
          }
          elem = link.responseText;
          response = document.createElement("span");
          response.innerHTML = elem;
          _this.classList.add("active");
          container.innerHTML = "";
          container.insertAdjacentHTML('afterBegin', response.querySelector(".main_news_container").innerHTML);
        }
    }
};
link.send( null );
})

on('body', 'click', '.window_fullscreen_hide', function() {
  parent = this.parentElement
  parent.querySelector(".window_fullscreen").style.display = "none";
  parent.getElementById("window_loader").innerHTML=""}
);
on('body', 'click', '.photo_fullscreen_hide', function() {
  parent = this.parentElement
  parent.querySelector(".photo_fullscreen").style.display = "none";
  parent.getElementById("photo_loader").innerHTML=""}
);
on('body', 'click', '.create_fullscreen_hide', function() {
  parent = this.parentElement
  parent.querySelector(".create_fullscreen").style.display = "none";
  parent.getElementById("create_loader").innerHTML=""}
);


on('#ajax', 'click', '.sel__box__options', function() {

  block = this.parentElement.parentElement.nextElementSibling;
  map = this.parentElement.parentElement.parentElement.previousElementSibling;

    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/list/region/" + slug + "/", true );
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function () {
      if ( link.readyState == 4 ) {
          if ( link.status == 200 ) {
              block.innerHTML = link.responseText;
              svg_list = map.querySelectorAll("path");
              for (var i = 0; i < svg_list.length; i++) {
                svg_list[i].style.fill = "rgba(0,0,0,0.15)";
              }
              svg = map.querySelector('[data-slug=' + '"' + slug + '"' + ']');
              svg.style.fill = "#897FF1";
          }
      }
  };
  link.send( null );
});

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url)
  } else {toast_info("Вы уже на этой странице")}
})


/////////////////////////////////////////////////////

var $body = document.querySelector("body");

on('body', 'click', '.nav-link-style', function() {
  var $this = this,
    mainMenu = $body.querySelector('.main-menu'),
    navbar = $body.querySelector('.header-navbar');

  if (!$body.classList.contains('dark-layout')) {
    $body.classList.add('dark-layout');
    mainMenu.classList.remove('menu-light'); mainMenu.classList.add('menu-dark');
    navbar.classList.remove('navbar-light'); navbar.classList.add('navbar-dark');
    $this.innerHTML = '<svg class="ficon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
  } else if ($body.classList.contains('dark-layout')){
    $body.classList.remove("dark-layout");
    mainMenu.classList.remove('menu-dark'); mainMenu.classList.add('menu-light');
    navbar.classList.remove('navbar-dark'); navbar.classList.add('navbar-light');
    $this.innerHTML = '<svg class="ficon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon ficon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
  }
  navbar.style.background = "inherit";
  navbar.style.boxShadow = "inherit";
});

on('body', 'click', '.nav-link-search', function() {
  this.nextElementSibling.classList.add("open");
});
on('body', 'click', '.a_has_sub', function() {
  this.parentElement.classList.contains("open") ? this.parentElement.classList.remove("open") : this.parentElement.classList.add("open")
});

on('body', 'click', '.search-input-close', function() {
  this.parentElement.classList.remove("open");
})

on('body', 'click', '.dropdown-user-link', function() {
  this.nextElementSibling.classList.contains("show") ? this.nextElementSibling.classList.remove("show") : this.nextElementSibling.classList.add("show")
});

on('body', 'click', '.menu-toggle', function() {
  _this = this;
  if (!_this.classList.contains("is-active")){
    _this.classList.add("is-active");
    $body.classList.add("menu-open");
    $body.querySelector(".sidenav-overlay").classList.add("show");
    $body.querySelector(".menu_close").style.display = "block";
    $body.querySelector(".main-menu").classList.add("left_18")
  }
})

on('body', 'click', '.sidenav-overlay', function() {
  if (this.classList.contains("show")){
    $body.querySelector(".menu-toggle").remove("is-active");
    $body.classList.remove("menu-open");
    $body.querySelector(".menu_close").style.display = "none";
    $body.querySelector(".sidenav-overlay").classList.remove("show");
    $body.querySelector(".nav_item_toggle").innerHTML = '<a class="nav-link menu-toggle pointer"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-menu ficon"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg></a>'
    $body.querySelector(".main-menu").classList.remove("left_18")
  }
})

on('body', 'click', '.menu_close', function() {
  this.style.display = "none";
  $body.querySelector(".menu-toggle").remove("is-active");
  $body.classList.remove("menu-open");
  $body.querySelector(".sidenav-overlay").classList.remove("show");
  $body.querySelector(".nav_item_toggle").innerHTML = '<a class="nav-link menu-toggle"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-menu ficon"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg></a>'
  $body.querySelector(".main-menu").classList.remove("left_18")
})

on('body', 'click', '.menu_nav_1', function() {
  _this = this;
  if (!_this.classList.contains("active")){
    _this.classList.add("active");
    _this.nextElementSibling.classList.remove("active");
    parent = _this.parentElement;
    parent.nextElementSibling.style.display = "block";
    parent.nextElementSibling.nextElementSibling.style.display = "none";
  }
})
on('body', 'click', '.menu_nav_2', function() {
  _this = this;
  if (!_this.classList.contains("active")){
    _this.classList.add("active");
    _this.previousElementSibling.classList.remove("active");
    parent = _this.parentElement;
    parent.nextElementSibling.style.display = "none";
    parent.nextElementSibling.nextElementSibling.style.display = "block";
  }
})

on('body', 'click', '.reply_comment', function() {
  first_name = this.parentElement.parentElement.parentElement.querySelector(".first_name").innerHTML;
  console.log(first_name)
  div = this.parentElement.nextElementSibling;
  input = div.querySelector(".text-comment");
  input.value = first_name + ', ';
  div.style.display = "block";
  input.focus();
})
on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle("show")
})
on('#ajax', 'click', '.hide_comment_form', function() {
  this.parentElement.parentElement.parentElement.style.display = "none";
})
