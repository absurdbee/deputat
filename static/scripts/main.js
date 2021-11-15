
function show_hide_password(target){
	var input = target.previousElementSibling;
	if (input.getAttribute('type') == 'password') {
		target.classList.add('view');
		input.setAttribute('type', 'text');
	} else {
		target.classList.remove('view');
		input.setAttribute('type', 'password');
	}
	return false;
};

on('body', 'click', '.why_publish', function() {
	create_fullscreen("/terms/window_about/", "window_fullscreen");
});
on('body', 'click', '.how_to_publish', function() {
	create_fullscreen("/terms/window_about/", "window_fullscreen");
});
on('body', 'click', '.create_support_message', function(e) {
	e.preventDefault();
	create_fullscreen("/quan/create_support/", "window_fullscreen");
});

on('body', 'click', '.load_media_list', function(el) {
	_this = this;
	path = el.path[0] + "";
	if (path[8] == "S") {
		if (_this.parentElement.classList.contains("open")) {
			_this.parentElement.classList.remove("open");
			svg = _this.querySelector("svg");
			svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 17l5-5-5-5v10z"/>'
		} else {
			_this.parentElement.classList.add("open");
			if (_this.querySelector("svg")) {
				svg = _this.querySelector("svg");
				svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M7 10l5 5 5-5H7z"/>'
			}
		}
	} else {
  		profile_list_block_load(_this, ".load_block", "/main_media/?uuid=" + _this.getAttribute("data-uuid"), "load_media_list");
			l = document.body.querySelectorAll(".list_toggle")
			for (var i = 0; i < l.length; i++) {
				l[i].querySelector(".text-truncate").style.borderBottom = "none"
			};
			_this.querySelector(".text-truncate").style.borderBottom = "1px #3176c1 dotted"
		}
});

on('body', 'keydown', '.form-control', function(e) {
  if (e.keyCode == 13) {
		if (this.classList.contains("custom_supported")){
			this.setAttribute("rows", this.getAttribute("rows")*1 + 1);
		}
		else if (this.classList.contains("elect_search_input")){
			// нажатие на enter формы поиска на левой панели
			if (this.value.length < 3) {
				toast_info("Поиск работает от 3х букв"); return
			} else { ajax_get_reload("/search/?all_name=" + this.value)}
		} else if (this.classList.contains("elect_search_input_2")){
			// нажатие на enter формы поиска на странице поиска
			if (this.value.length < 3) {
				toast_info("Поиск работает от 3х букв"); return
			};
			var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
			btn_box = document.body.querySelector(".nav-pills");
			active = btn_box.querySelector(".active");
			if (active.classList.contains("all_btn")) {
				q = "all_name="
			}
			else if (active.classList.contains("elect_btn")) {
				q = "elect_name="
			}
			else if (active.classList.contains("tags_btn")){
				q = "all_name="
			};

		  link.open( 'GET', "/search/?" + q + this.value, true );
		  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		  link.onreadystatechange = function () {
		    if ( link.readyState == 4 ) {
		        if ( link.status == 200 ) {
							block = document.body.querySelector(".search_container");
							elem_ = document.createElement('span');
							elem_.innerHTML = link.responseText;
							block.innerHTML = "";
							block.innerHTML = elem_.querySelector(".search_container").innerHTML;
		        }
		    }
		};
		link.send( null );
		}
		else {e.preventDefault()}
  }
})
on('body', 'click', '.nav_search_btn', function() {
	if (this.classList.contains("active")) {
		return
	};
	var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
	btns = document.body.querySelectorAll(".nav-link");
	for (var i = 0; i < btns.length; i++){
		btns[i].classList.remove("active")
	};
	this.classList.add("active");
	value = document.body.querySelector(".elect_search_input_2");
	link.open( 'GET', this.getAttribute("data-href") + value.value, true );
	link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	link.onreadystatechange = function () {
		if ( link.readyState == 4 ) {
				if ( link.status == 200 ) {
					block = document.body.querySelector(".search_container");
					elem_ = document.createElement('span');
					elem_.innerHTML = link.responseText;
					block.innerHTML = "";
					block.innerHTML = elem_.querySelector(".search_container").innerHTML;
				}
		}
};
link.send( null );
	block = document.body.querySelector(".search_container");

})

on('body', 'click', '.show_parent_next_element', function() {
  this.parentElement.nextElementSibling.style.display = "block"
})

on('body', 'click', '.load_left_menu_regions', function(e) {
	e.preventDefault();
  list_load(this.parentElement.parentElement, "/region/load_left_menu_regions/");
})
on('body', 'click', '.load_left_menu_dropdown_regions', function(e) {
	e.preventDefault();
  list_load(this.parentElement.parentElement, "/region/load_left_menu_regions_select/");
});

on('body', 'change', '.left_menu_regions', function() {
	_this = this;
	val = _this.value;
	option = _this.nextElementSibling.querySelector('[value=' + '"' + val + '"' + ']')
	slug = option.getAttribute("data-slug");

	if (val == '') {
		return
	} else {cities_list_load(this.nextElementSibling.nextElementSibling, "/region/load_left_menu_region_get_districts/" + slug + "/")}
});

on('body', 'click', '.base_row_container', function() {
	drops = document.body.querySelectorAll(".dropdown-menu");
  for (var i = 0; i < drops.length; i++){
		try{drops[i].classList.remove("show")} catch { null }
	}
})
on('body', 'click', '.stop_propagation_block', function(e) {
	e.stopPropagation()
});
on('body', 'click', '.window_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
	get_document_opacity_1()
});
on('body', 'click', '.previous_click', function(event) {
  this.previousElementSibling.click();
});
on('body', 'click', '.map_selector', function() {
  slug = this.getAttribute("data-slug");
  text = this.getAttribute("data-name");
  svg_list = this.parentElement.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    svg_list[i].style.fill = "#DAD8D6";
		svg_list[i].classList.remove("selected");
  };
  this.style.fill = "#3176C1";
	this.classList.add("selected");
  col_md_4 = this.parentElement.parentElement.nextElementSibling;
  block = col_md_4.querySelector("#elect_for_regions_loader");
  col_md_4.querySelector("#select_regions").value = slug;

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/region/region/" + slug + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
            block = link.responseText;
        }
    }
};
link.send( null );
});

on('body', 'change', '#select_regions', function() {
  slug = this.value;
	map = this.parentElement.parentElement.querySelector("#russia_map")
  svg_list = map.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    svg_list[i].style.fill = "#DAD8D6";
		svg_list[i].classList.remove("selected");
  };
	svg = map.querySelector('[data-slug=' + '"' + slug + '"' + ']')
  svg.style.fill = "#3176C1";
	svg.classList.add("selected");
  block = this.nextElementSibling;

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/region/region/" + slug + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
            block.innerHTML = link.responseText;
        }
    }
};
link.send( null );
});

on('body', 'mouseover', '.map_selector', function(e) {
	_this = this;
	popup = _this.parentElement.nextElementSibling;
	iconPos = _this.getBoundingClientRect();
  popup.style.left = (e.clientX - 200) + "px";
  popup.style.top = (e.clientY - 250) + "px";
	popup.querySelector("h6").innerHTML = _this.getAttribute("data-name");
	popup.style.display = "block";
	this.style.fill = "#3176C1";
});
on('body', 'mouseout', '.map_selector', function() {
	this.parentElement.nextElementSibling.style.display = "none";
	if (!this.classList.contains("selected")){
  	this.style.fill = "#DAD8D6"
	} else {
		this.style.fill = "#3176C1";
	}
});

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
});

on('body', 'click', '.window_fullscreen_hide', function() {
  parent = this.parentElement
  parent.style.display = "none";
  parent.getElementById("window_loader").innerHTML="";
	get_document_opacity_1();
});
on('body', 'click', '.photo_fullscreen_hide', function() {
  parent = this.parentElement
  parent.style.display = "none";
  parent.getElementById("photo_loader").innerHTML="";
	get_document_opacity_1();
});
on('body', 'click', '.create_fullscreen_hide', function() {
  parent = this.parentElement
  parent.style.display = "none";
  parent.getElementById("create_loader").innerHTML="";
	get_document_opacity_1();
});

on('body', 'click', '.sel__box__options', function() {
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
  } else {
		toast_info("Вы уже на этой странице")
	};
});


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
		theme = 2;
		if ($body.querySelector('.elect_detail_banner')) {
			img = $body.querySelector('.elect_detail_banner');
			img.setAttribute("src", "/static/images/test_1.jpg")
		}
  } else if ($body.classList.contains('dark-layout')){
    $body.classList.remove("dark-layout");
    mainMenu.classList.remove('menu-dark'); mainMenu.classList.add('menu-light');
    navbar.classList.remove('navbar-dark'); navbar.classList.add('navbar-light');
    $this.innerHTML = '<svg class="ficon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon ficon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
		theme = 1;
		if ($body.querySelector('.elect_detail_banner')) {
			console.log("elect_detail_banner!")
			img = $body.querySelector('.elect_detail_banner');
			img.setAttribute("src", "/static/images/test_2.jpg")
		}
  }
  navbar.style.background = "inherit";
  navbar.style.boxShadow = "inherit";

	var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', "/users/load/change_theme/?theme=" + theme, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.send( null );
});

on('body', 'click', '.nav-link-search', function() {
  this.nextElementSibling.classList.add("open");
});
on('body', 'click', '.a_has_sub', function() {
	if (this.parentElement.classList.contains("open")) {
		this.parentElement.classList.remove("open");
		if (this.querySelector("svg")) {
			svg = this.querySelector("svg");
			svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 17l5-5-5-5v10z"/>'
		}
	} else {
		this.parentElement.classList.add("open");
		if (this.querySelector("svg")) {
			svg = this.querySelector("svg");
			svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M7 10l5 5 5-5H7z"/>'
		}
	}
});

on('body', 'click', '.a_has_sub_alt', function() {
	if (_this.parentElement.classList.contains("open")) {
		_this.parentElement.classList.remove("open");
		svg = _this.querySelector("svg");
		svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 17l5-5-5-5v10z"/>'
	} else {
		_this.parentElement.classList.add("open");
		if (_this.querySelector("svg")) {
			svg = _this.querySelector("svg");
			svg.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M7 10l5 5 5-5H7z"/>'
		}
	}
});

on('body', 'click', '.search-input-close', function() {
  this.parentElement.classList.remove("open");
})

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
    mobile_menu_close()
    $body.querySelector(".menu_close").style.display = "none";
  }
})

function mobile_menu_close() {
	$body.querySelector(".menu-toggle").remove("is-active");
  $body.classList.remove("menu-open");
  $body.querySelector(".sidenav-overlay").classList.remove("show");
  $body.querySelector(".nav_item_toggle").innerHTML = '<a class="nav-link menu-toggle"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-menu ficon"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg></a>'
  $body.querySelector(".main-menu").classList.remove("left_18")
}

on('body', 'click', '.menu_close', function() {
  this.style.display = "none";
  mobile_menu_close();
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
on('body', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle("show")
})
on('body', 'click', '.hide_comment_form', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.style.display = "none";
  parent.parentElement.querySelector(".align-items-center").style.display = "block";
})

on('body', 'click', '.create_ajax', function() {
  link = this.getAttribute("data-href");
    create_fullscreen(link, "window_fullscreen");
});

on('body', 'click', '.get_user_notify_box', function() {
	count_box = this.querySelector(".resent_notify");
	_dropdown = this.parentElement.nextElementSibling;

	if (this.classList.contains("show")) {
		_dropdown.style.display = "none";
		this.classList.remove("show")
	} else {
		_dropdown.style.display = "block";
		this.classList.add("show")
	};

	container = _dropdown.querySelector(".notify_box");

	link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
	 link_.open( 'GET', "/notify/recent/", true );
	 link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	 link_.onreadystatechange = function () {
	 if ( this.readyState == 4 && this.status == 200 ) {
		elem_ = document.createElement('span');
		elem_.innerHTML = link_.responseText;
		container.innerHTML = "";
		container.innerHTML = elem_.innerHTML;
		count_box.classList.add("showed");
		create_pagination(container);

		if (count_box.innerHTML) {
			count_box.innerHTML = "";
			link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
			link.open( 'GET', "/notify/all_read/", true );
			link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
			link.onreadystatechange = function () {
			 if ( this.readyState == 4 && this.status == 200 ) {
				 console.log("Уведы прочитаны!")
			 }};
			 link.send();

		}
	 }};
	 link_.send();
})

on('body', 'change', '#id_region', function() {
	_this = this;
	var val = _this.value;
	parent = _this.parentElement;
	 if (!parent.classList.contains("is_region_multiple")) {
		 return
	 }
	city_container = parent.nextElementSibling;
	selectedOptions = _this.selectedOptions;
	if (val == '' || selectedOptions.length > 1) {
		city_container.innerHTML = "";
	} else {
		var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
		link.open( 'GET', "/region/load_districts_for_multiple_form/" + val + "/", true );
		link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		link.onreadystatechange = function () {
			if ( link.readyState == 4 ) {
					if ( link.status == 200 ) {
							city_container.innerHTML = link.responseText;
					}
			}
	};
	link.send( null );
	};
});

on('body', 'click', '#create_support_message_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
	files = form.querySelector("#id_files")
	if (files.length) {
		for (var i = 0; i < files.length; i++) {
			if (findSize(files[i])> 5242880) {
		    toast_error("Файлы не должен превышать 5 Мб!"),
		    _this.disabled = false;
		    return
		  }
		};
		if (files.length > 10) {
	      toast_error("Не больше 10 файлов");
				return
	  }
	}

  else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Напишите сообщение!");
		return
	}
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/quan/create_support/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Сообщение отправлено!")
    close_fullscreen()
  }};

  link_.send(form_data);
});
