
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

on('body', 'click', '.remove_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk"); name = _this.getAttribute("data-name")

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.classList.add("add_elect_subscribe", "btn-primary"); _this.classList.remove("remove_elect_subscribe");
          _this.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart align-middle mr-25"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg><span class="text-truncate">Подписаться</span>'
          toast_info(name + " удален из подписок!");
        }
    }
};
link.send( null );
})

on('body', 'click', '.add_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk"); name = _this.getAttribute("data-name")

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/subscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.classList.add("remove_elect_subscribe"); _this.classList.remove("add_elect_subscribe", "btn-primary");
          _this.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x align-middle mr-25"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg><span class="text-truncate">Вы подписаны</span>'
          toast_info(name + " возвращен в подписки!");
        }
    }
};
link.send( null );
})

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

on('body', 'click', '.elect_new_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/progs/elect_like/" + pk + "/");
});
on('body', 'click', '.elect_new_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/progs/elect_dislike/" + pk + "/");
});

on('body', 'click', '.blog_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/progs/blog_like/" + pk + "/");
});
on('body', 'click', '.blog_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/progs/blog_dislike/" + pk + "/");
});

on('body', 'click', '.load_elect_stat_year', function() {
  this.getAttribute('data-pk') ? pk = this.getAttribute('data-pk') : pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("window_loader");
  open_fullscreen("/stat/elect_year/" + pk + "/", loader);
});

load_chart(); get_select()


on('#ajax', 'click', '.sel', function() {
  this.classList.toggle('active')
})

on('#ajax', 'click', '.sel__box__options', function() {
  var txt = $(this).text();
  var index = $(this).index();
  var slug = $(this).attr("slug");

  console.log(slug)

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

$(window).on('load', function() {
    if (feather) {
        feather.replace({
            width: 14,
            height: 14
        });
    }
})

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url)
  } else {toast_info("Вы уже на этой странице")}
})
