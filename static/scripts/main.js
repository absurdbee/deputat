
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
  col_md_3.querySelector(".sel__placeholder").innerHTML = text;

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

var authority_infinite = new Waypoint.Infinite({
element: $('.pag_container')[0],
onBeforePageLoad: function () {
  $('.load').show();
},
onAfterPageLoad: function ($items) {
$('.load').hide();
}
});

on('body', 'click', '.select_elect_news_category', function() {
  _this = this;
  url = _this.getAttribute("data-href");
  if (_this.classList.contains("active")){
    return
  }
  elect_news_container = document.body.querySelector(".elect_news_container");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          links = _this.parentElement.parentElement.querySelectorAll(".select_elect_news_category");
          console.log(links);
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

on('body', 'click', '.window_fullscreen_hide', function() {
  document.querySelector(".window_fullscreen").style.display = "none";
  document.getElementById("window_loader").innerHTML=""}
);

load_chart();
get_select();


on('#ajax', 'click', '.sel', function() {
  this.classList.toggle('active')
})

on('#ajax', 'click', '.sel__box__options', function() {
  var txt = $(this).text();
  var index = $(this).index();
  var slug = $(this).attr("slug");

  $(this).siblings('.sel__box__options').removeClass('selected');
  $(this).addClass('selected');

  var $currentSel = $(this).closest('.sel');
  $currentSel.children('.sel__placeholder').text(txt);
  $currentSel.children('select').prop('selectedIndex', index + 1);

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
function getCurrentLayout() {
  var currentLayout = '';
  if ($body.hasClass('dark-layout')) {
    currentLayout = 'dark-layout';
  } else if ($body.hasClass('bordered-layout')) {
    currentLayout = 'bordered-layout';
  } else {
    currentLayout = '';
  }
  return currentLayout;
}

$('.nav-link-style').on('click', function () {
  var $this = $(this),
    currentLayout = getCurrentLayout(),
    mainMenu = $('.main-menu'),
    navbar = $('.header-navbar'),
    switchToLayout = '',
    prevLayout = $this.attr('data-prev-layout');

  if (currentLayout === '' || currentLayout === 'bordered-layout') {
    switchToLayout = 'dark-layout';
    $this.attr('data-prev-layout', currentLayout);
  } else {
    switchToLayout = prevLayout;
  }
  $body.removeClass('dark-layout bordered-layout');
  if (switchToLayout === 'dark-layout') {
    $body.addClass('dark-layout');
    mainMenu.removeClass('menu-light').addClass('menu-dark');
    navbar.removeClass('navbar-light').addClass('navbar-dark');
    $this.find('.ficon').replaceWith(feather.icons['sun'].toSvg({ class: 'ficon' }));
  } else {
    $body.addClass(prevLayout);
    mainMenu.removeClass('menu-dark').addClass('menu-light');
    navbar.removeClass('navbar-dark').addClass('navbar-light');
    $this.find('.ficon').replaceWith(feather.icons['moon'].toSvg({ class: 'ficon' }));
  }

  $('.horizontal-menu .header-navbar.navbar-fixed').css({
    background: 'inherit',
    'box-shadow': 'inherit'
  });
  $('.horizontal-menu .horizontal-menu-wrapper.header-navbar').css('background', 'inherit');
});
