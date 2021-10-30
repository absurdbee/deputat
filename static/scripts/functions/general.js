on('body', 'click', '.body_overlay', function() {
  container = document.body.querySelector("#fullscreens_container");
  if (container.innerHTML) {
    container.querySelector(".card_fullscreen").remove();
  };
  if (!container.innerHTML) {get_document_opacity_1(document.body);}
});

function create_fullscreen(url, type_class) {
  container = document.body.querySelector("#fullscreens_container");
  try {count_items = container.querySelectorAll(".card").length} catch {count_items = 0};

  $parent_div = document.createElement("div");
  $parent_div.classList.add("card_fullscreen", "mb-3", "border", type_class);
  $parent_div.style.zIndex = 100 + count_items;
  $parent_div.style.opacity = "0";

  if (document.body.querySelector(".desctop_nav")) {
    hide_svg = '<svg class="svg_default" style="position:fixed;" width="30" height="30" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  } else { hide_svg = "" };
  $hide_span = document.createElement("span");
  $hide_span.classList.add("this_fullscreen_hide");
  $loader = document.createElement("div");

  $loader.setAttribute("id", "fullscreen_loader");
  $hide_span.innerHTML = hide_svg;
  $parent_div.append($hide_span);
  $parent_div.append($loader);
  $parent_div.append(create_gif_loading ());
  container.prepend($parent_div);

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link.open('GET', url, true);
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          $load_div.remove();
          elem = link.responseText;

          $loader.innerHTML = elem;
          height = $loader.scrollHeight*1 + 30;
          if (height < 500 && !$loader.querySelector(".data_display")) {
            $parent_div.style.height = height + "px";
            $loader.style.overflowY = "unset";

            _height = (window.innerHeight - height - 50) / 2;
            $parent_div.style.top = _height + "px";
            prev_next_height = _height*1 + 50 + "px";
            try {$loader.querySelector(".prev_item").style.top = "-" + prev_next_height}catch {null};
            try {$loader.querySelector(".next_item").style.top = "-" + prev_next_height}catch {null}
          } else {
            $parent_div.style.height = "100%";
            $parent_div.style.top = "15px";
            $loader.style.overflowY = "auto";
          };
          $parent_div.style.opacity = "1";

          get_document_opacity_0();
          init_music($loader);

          if ($loader.querySelector(".next_page_list")) {
            $loader.onscroll = function() {
              box = $loader.querySelector('.next_page_list');
              if (box && box.classList.contains("next_page_list")) {
                  inViewport = elementInViewport(box);
                  if (inViewport) {
                      box.remove();
                      var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
                      link_3.open('GET', location.protocol + "//" + location.host + box.getAttribute("data-link"), true);
                      link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                      link_3.onreadystatechange = function() {
                          if (this.readyState == 4 && this.status == 200) {
                              var elem = document.createElement('span');
                              elem.innerHTML = link_3.responseText;
                              $loader.querySelector(".is_load_paginate").insertAdjacentHTML('beforeend', elem.querySelector(".is_load_paginate").innerHTML);
                            }
                      }
                      link_3.send();
                  }
              };
            }
          }
      }
  };
  link.send();
};

function create_elect_fullscreen(url, name) {
  container = document.body.querySelector("#fullscreens_container");
  try {count_items = container.querySelectorAll(".card").length} catch {count_items = 0};

  $parent_div = document.createElement("div");
  $parent_div.classList.add("card_fullscreen", "mb-3", "border", "worker_fullscreen");
  $parent_div.style.zIndex = 100 + count_items;
  $parent_div.style.opacity = "0";

  if (document.body.querySelector(".desctop_nav")) {
    hide_svg = '<svg class="svg_default" style="position:fixed;" width="30" height="30" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  } else { hide_svg = "" };
  $hide_span = document.createElement("span");
  $hide_span.classList.add("this_fullscreen_hide");
  $loader = document.createElement("div");

  $loader.setAttribute("id", "fullscreen_loader");
  $hide_span.innerHTML = hide_svg;
  $parent_div.append($hide_span);
  $parent_div.append($loader);
  $parent_div.append(create_gif_loading ());
  container.prepend($parent_div);

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link.open('GET', url, true);
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          $load_div.remove();
          elem = link.responseText;

          $loader.innerHTML = elem;
          height = $loader.scrollHeight*1 + 30;
          if (height < 500 && !$loader.querySelector(".data_display")) {
            $parent_div.style.height = height + "px";
            $loader.style.overflowY = "unset";

            _height = (window.innerHeight - height - 50) / 2;
            $parent_div.style.top = _height + "px";
            prev_next_height = _height*1 + 50 + "px";
            try {$loader.querySelector(".prev_item").style.top = "-" + prev_next_height}catch {null};
            try {$loader.querySelector(".next_item").style.top = "-" + prev_next_height}catch {null}
          } else {
            $parent_div.style.height = "100%";
            $parent_div.style.top = "15px";
            $loader.style.overflowY = "auto";
          };
          $parent_div.style.opacity = "1";
          get_document_opacity_0();

          if (name) {
            elect_box = $loader.querySelector(".elect_block");
            content = document.body.querySelector(".content-body");
            elect_name = content.querySelector("h1").innerHTML;
            elect_src = content.querySelector(".img_elect_page").getAttribute("src");
            elect_pk = content.getAttribute("data-pk");
            elect_box.innerHTML = '<label>Чиновник</label><input value="' + elect_pk + '" type="hidden" name="elect" id="id_elect"><div class="media border" style="margin-bottom:5px"><img src="' + elect_src + '" style="width:35px;" alt="image"><div class="media-body pl-1"><h6 class="my-0">' + elect_name + '</h6></div></div>'
          };
      }
  };
  link.send();
};

function change_this_fullscreen(_this, type_class) {
  _this.parentElement.classList.contains("col") ? $loader = _this.parentElement.parentElement.parentElement.parentElement : $loader = _this.parentElement.parentElement;
  $loader.innerHTML = "";
  $parent_div.style.opacity = "0";
  $parent_div.style.height = "35px";

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link.open('GET', _this.getAttribute("href"), true);
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem = link.responseText;
          $loader.innerHTML = elem;
          height = $loader.scrollHeight*1 + 30;
          $parent_div = $loader.parentElement
          if (height < 500 && !$loader.querySelector(".data_display")){
            $parent_div.style.height = height + "px";
            _height = (window.innerHeight - height - 50) / 2;
            $parent_div.style.top = _height + "px";
            prev_next_height = _height*1 + 50 + "px";
            $loader.style.overflowY = "unset";
            try {$loader.querySelector(".prev_item").style.top = "-" + prev_next_height}catch {null};
            try {$loader.querySelector(".next_item").style.top = "-" + prev_next_height}catch {null}
          } else {
            $parent_div.style.height = "100%";
            $parent_div.style.top = "15px";
            $loader.style.overflowY = "auto";
          };
          $parent_div.style.opacity = "1";
          init_music($loader);
      }
  };
  link.send();
};
function close_fullscreen() {
  container = document.body.querySelector("#fullscreens_container");
  container.querySelector(".card_fullscreen").remove();
  if (!container.innerHTML) {
    get_document_opacity_1(document.body.querySelector(".main-container"));
  }
};

on('body', 'click', '.this_fullscreen_hide', function() {
  close_fullscreen()
});
on('body', 'click', '.this_mob_fullscreen_hide', function() {
  close_fullscreen()
});

function validateEmail(email){var re = /\S+@\S+\.\S+/;return re.test(email)};
function scrollToBottom(id) {document.querySelector(id).scrollIntoView(false);}
function findSize(input) {
    try{
        return input.files[0].size;
    }catch(e){
        var objFSO = new ActiveXObject("Scripting.FileSystemObject");
        var e = objFSO.getFile( input.value);
        var fileSize = e.size;
        return fileSize;
    }
};
function post_send_change(span, _link, new_class, html) {
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    pk = item.getAttribute("data-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            span.innerHTML = "";
            span.append(new_span)
        }
    };
    link.send(null)
};
function send_form_and_toast_and_close_window(url, form) {
    form_data = new FormData(form);
    ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            close_fullscreen();
            toast_info("Жалоба отправлена!");
        }
    }
    ajax_link.send(form_data);
}

function get_profile_sanction_window(_this, url) {
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
    pk = _this.parentElement.getAttribute("data-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }
  else if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk")
  }
  create_fullscreen(url + pk + "/", "worker_fullscreen");
}
function get_item_sanction_window(_this, block, url) {
    _this.parentElement.parentElement.getAttribute("data-uuid")
     ?  uuid = _this.parentElement.parentElement.getAttribute("data-uuid")
     : (uuid = _this.getAttribute("data-uuid"), block.classList.add("changed"));
  create_fullscreen(url + uuid + "/", "worker_fullscreen");
}
function get_music_doc_sanction_window(_this, block, url) {
    _this.parentElement.parentElement.parentElement.getAttribute("data-pk")
     ?  (block = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement, pk = _this.parentElement.parentElement.parentElement.getAttribute("data-pk"), block.classList.add("changed"))
     : (pk = _this.getAttribute("data-pk"), block.classList.add("changed"));
  create_fullscreen(url + pk + "/", "worker_fullscreen");
}

function send_user_sanction(_this, form, url, old_class, new_class, toast) {
  form_data = new FormData(form);
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk")
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("user-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info(toast);
    close_fullscreen();
    if (document.body.querySelector(".pk_saver")) {
      _this.innerHTML = "Отменить";
      _this.classList.replace(old_class, new_class)
    }else if (li.classList.contains("changed")){
      li.remove();
    }
  }};

  link_.send(form_data);
}

function send_item_sanction(_this, form, url, old_class, new_class, toast) {
  form_data = new FormData(form);

  if (document.body.querySelector(".load_block")){
    uuid = _this.getAttribute("data-uuid")
  }
  else if (document.body.querySelector(".changed")){
    div = document.body.querySelector(".changed");
    uuid = div.getAttribute("data-uuid");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info(toast);
    close_fullscreen();

    if (document.body.querySelector(".load_block")){
      document.body.querySelector(".load_block").innerHTML = '<div class="card mt-3 centered"><div class="card-body" style="margin-top: 10%;">  <svg class="thumb_big svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg></div><h6>Сущность блокирована.</h6></div>'
    }
    else if (div && div.classList.contains("changed")){
      div.remove();
    }
  }};

  link_.send(form_data);
}

function open_manager_window(_this, url) {
  if (document.body.querySelector(".changed")) {
    div = document.body.querySelector(".changed");
    uuid = div.querySelector(".uuid_keeper").getAttribute("data-uuid")
  } else if (_this.parentElement.getAttribute("data-pk")) {
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.getAttribute("data-pk");
    div.classList.add("changed");
    console.log("ok")
  }  else{
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    uuid = div.getAttribute("data-pk"), div.classList.add("changed");
  }
  div = document.body.querySelector(".changed");
  create_fullscreen(url + uuid + "/", "worker_fullscreen");
}
function send_window_sanction_post(form, url, toast) {
  // отправляем данные формы применеия санкций на странице списка или в модерском отделе модерации
  form_data = new FormData(form);
  div = document.body.querySelector(".changed") ? div = document.body.querySelector(".changed") : div = null;
  uuid = form.getAttribute("data-uuid");
  form.getAttribute("data-uuid") ? uuid = form.getAttribute("data-uuid") : uuid = form.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info(toast);
    close_fullscreen();

    if (document.body.querySelector(".changed")){
      div.remove();
    }
    else if (document.body.querySelector(".load_block")){
      document.body.querySelector(".load_block").innerHTML = '<div class="card mt-3 centered"><div class="card-body" style="margin-top: 10%;">  <svg class="thumb_big svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg></div><h6>Сущность блокирована.</h6></div>'
    }
  }};

  link_.send(form_data);
}
function clean_body_changed_class() {
  document.body.querySelector(".changed") ? (changed = document.body.querySelector(".changed"), changed.classList.remove("changed")) : null
}
function send_window_sanction_get(_this, url, toast) {
  // работа санкций при открытом окне списков и элементов - посылка сигнала без формы
  if (document.body.querySelector(".changed")) {
    div = document.body.querySelector(".changed");
    uuid = div.querySelector(".uuid_keeper").getAttribute("data-uuid")
  } else if (_this.parentElement.getAttribute("data-pk")) {
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.getAttribute("data-pk");
  }  else{
    div = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    uuid = div.getAttribute("data-pk"), div.classList.add("changed");
  }
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info(toast);
    close_fullscreen();

    if (document.body.querySelector(".load_block")){
      document.body.querySelector(".load_block").innerHTML = '<div class="card mt-3 centered"><div class="card-body" style="margin-top: 10%;">  <svg class="thumb_big svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg></div><h6>Сущность блокирована.</h6></div>'
    }
    else {div.remove();}
  }};

  link_.send();
}

function list_load(block, link) {
  // грузим что-то по ссылке link в блок block
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ) {
      block.innerHTML = request.responseText;
      block.querySelector(".left_menu_select").click();
      block.querySelector(".left_menu_select").focus();
    }
  };
  request.send( null );
}

function cities_list_load(block, link) {
  // грузим что-то по ссылке link в блок block
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ) {
      block.innerHTML = request.responseText;

        parent = block.parentElement.parentElement.parentElement;
        console.log(parent)
        if (parent.classList.contains("municipal_authorities")) {
  				district_id = "district_elects_1"
  			}
  			else if (parent.classList.contains("organizations")) {
  				district_id = "district_organizations_2"
  			}
  			else if (parent.classList.contains("communities")) {
  				district_id = "district_communities_3"
  			};

        input_1 = block.querySelector(".left_menu_select_districts");
        input_1.setAttribute("list", district_id);
  			input_1.nextElementSibling.setAttribute("id", district_id);
    }
  };
  request.send( null );
}

function media_list_edit(_this, url) {
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { _this.disabled = true }
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    close_fullscreen();
    name = form.querySelector('#id_name').value;
    list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
    list.querySelector('.list_name') ? list.querySelector('.list_name').innerHTML = name : null;
    document.body.querySelector('.second_list_name').innerHTML = name;
    toast_success("Список изменен")
  }}
  link_.send(form_data);
}
function media_list_delete(_this, url, old_class, new_class) {
  uuid = _this.parentElement.parentElement.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.previousElementSibling.style.display = "none";
    _this.previousElementSibling.previousElementSibling.style.display = "none";
    _this.parentElement.querySelector(".second_list_name").innerHTML = "Список удален";
    list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
    list.querySelector('.list_name') ? list.querySelector('.list_name').innerHTML = "Список удален" : null;
    _this.classList.replace(old_class, new_class);
    _this.innerHTML = "Восстановить список";
  }}
  link_.send();
}
function media_list_recover(_this, url, old_class, new_class) {
  uuid = _this.parentElement.parentElement.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.previousElementSibling.style.display = "unset";
    _this.previousElementSibling.previousElementSibling.style.display = "unset";
    second_list = document.body.querySelector('.second_list_name');
    name = second_list.getAttribute("data-name");
    second_list.innerHTML = name;
    document.body.querySelector('.file-manager-item') ?
      (list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
       list.querySelector('.list_name').innerHTML = name) : null;
    _this.classList.replace(old_class, new_class);
    _this.innerHTML = "Удалить список";
  }}
  link_.send();
}

function profile_list_block_load(_this, block, link, actions_class) {
  // подгрузка списков в профиле пользователя
  if (_this.getAttribute("href")) {
    return
  }
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ){
        elem_ = document.createElement('span');
        elem_.innerHTML = request.responseText;
       document.body.querySelector(block).innerHTML = elem_.querySelector(block).innerHTML;
       init_music(document.body.querySelector(block));
       class_to_add = _this.parentElement.parentElement.querySelectorAll(".list_toggle")
       for (var i = 0; i < class_to_add.length; i++) {
         class_to_add[i].classList.add(actions_class, "pointer");
         class_to_add[i].classList.replace("active_border", "border");
       };
       _this.classList.remove(actions_class, "pointer");
       _this.classList.replace("border", "active_border");
       create_pagination(document.body.querySelector(block))
    }};
    request.send( null );
}
function init_music(block) {
  audios = block.querySelectorAll("audio");
  for (var i = 0; i < audios.length; i++) {
    player = new Plyr(audios[i]);
  };
  block.querySelector("#player") ? video = new Plyr(block.querySelector("#player")) : null
}

function check_span1(span1, uuid, response) {
  if (span1.classList.contains(uuid)){
    document.body.querySelector(".is_paginate").insertAdjacentHTML('afterBegin', response)
  }
}
function get_preview(response, type) {
  if (document.body.querySelector(".current_file_dropdown")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_body, pk)
    } else if (type == "track") {
      response.querySelector(".span_btn").remove();
      track_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, response.querySelector(".music_media_body"))
    } else if (type == "video") {
      pk = response.querySelector(".u_video_detail").getAttribute("video-pk");
      uuid = response.querySelector(".u_video_detail").getAttribute("list-pk");
      src = response.querySelector("img").getAttribute("src");
      video_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, uuid, src)
    }
  } else if (document.body.querySelector(".attach_block")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_post_attach(document.body.querySelector(".attach_block"), response.querySelector(".media-body"), pk)
    } else if (type == "track") {
      response.querySelector(".span_btn").remove();
      track_post_attach(document.body.querySelector(".attach_block"), response.querySelector(".music_media_body"))
    } else if (type == "video") {
      pk = response.querySelector(".u_video_detail").getAttribute("video-pk");
      uuid = response.querySelector(".u_video_detail").getAttribute("list-pk");
      src = response.querySelector("img").getAttribute("src");
      video_post_attach(document.body.querySelector(".attach_block"), pk, uuid, src)
    }
  } else if (document.body.querySelector(".message_attach_block")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_message_attach(document.body.querySelector(".message_attach_block"), response.querySelector(".media-body"), pk)
  }
} else if (document.body.querySelector(".uuid_saver")){
  uuid = document.body.querySelector(".uuid_saver").getAttribute("data-uuid");
  check_span1(response.querySelector('.span1'), uuid, response.innerHTML);
  document.body.querySelector(".item_empty") ? document.body.querySelector(".item_empty").style.display = "none" : null
};
};

on('body', 'click', '.menu_drop', function() {
  block = this.nextElementSibling;
  if (block.classList.contains("show")) { block.classList.remove("show") }
  else {
    all_drop = document.body.querySelectorAll(".dropdown-menu");
    for(i=0; i<all_drop.length; i++) {all_drop[i].classList.remove("show")};
    block.classList.add("show");
  }
});

function on_off_list_in_collections(_this, url, new_class, old_class, text) {
  pk = _this.parentElement.parentElement.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add(new_class);
      _this.classList.remove(old_class)
      _this.innerHTML = text
}}
link.send( null );
};
function add_item_in_list(_this, url, old_class, new_class) {
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.style.paddingLeft = "14px";
    _this.classList.add(new_class);
    _this.classList.remove(old_class);
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    _this.prepend(span)
  }};
  link.send( null );
}
function remove_item_from_list(_this, url, old_class, new_class, check_class) {
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  parent = _this.parentElement.parentElement.parentElement
  if (parent.parentElement.querySelector(check_class)) {
    drops = parent.parentElement.querySelectorAll("." + old_class);
    if (drops.length == 1) {
      return
    }
  };
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + parent.getAttribute("data-pk") + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.style.paddingLeft = "30px";
    _this.classList.add(new_class);
    _this.classList.remove(old_class);
    _this.querySelector("svg").remove();
  }};
  link.send( null );
}

function mob_send_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement;
    item.getAttribute("data-uuid") ? uuid = item.getAttribute("data-uuid") : uuid = item.getAttribute("good-pk"); link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + uuid + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}

function mob_send_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement;
    item.getAttribute("data-uuid") ? uuid = item.getAttribute("data-uuid") : uuid = item.getAttribute("good-pk"); link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + uuid + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}

function post_and_load_object_page(form, url_post, url_1) {
    form_data = new FormData(form);
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url_post, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0, 0);
            close_fullscreen();
            document.title = elem_.querySelector('title').innerHTML;
            uuid = rtr.querySelector(".uuid_saver").getAttribute("data-uuid");
            window.history.pushState(null, "vfgffgfgf", url_1 + uuid + '/')
        }
    }
    ajax_link.send(form_data)
}

on('body', 'click', '.photo_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  if (block.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  parent.remove();
});
on('body', 'click', '.doc_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  if (block.classList.contains("attach_block")){
    remove_file_attach(); is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  parent.remove();
});
on('body', 'click', '.video_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  if (block.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  parent.remove();
});
on('body', 'click', '.music_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  if (block.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  parent.remove();
});
on('body', 'click', '.photo_attach_list_remove', function() {
  block = this.parentElement.parentElement;
  if (block.parentElement.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  block.remove();
});
on('body', 'click', '.doc_attach_list_remove', function() {
  block = this.parentElement.parentElement;
  if (block.parentElement.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.parentElement.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  block.remove();
});
on('body', 'click', '.video_attach_list_remove', function() {
  block = this.parentElement.parentElement;
  if (block.parentElement.classList.contains("attach_block")){
    remove_file_attach(), is_full_attach()
  } else if (block.parentElement.classList.contains("comment_attach_block")){
    remove_file_dropdown(); is_full_dropdown()
  } else if (block.classList.contains("message_attach_block")){
    remove_file_message_attach(); is_full_message_attach()
  }
  block.remove();
});

function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};
function elementInViewport(el){var bounds = el.getBoundingClientRect();return ((bounds.top + bounds.height > 0) && (window.innerHeight - bounds.top > 0));}

function create_pagination(block) {
  if (block.querySelector('.is_paginate')) {
    scrolled(block.querySelector('.is_paginate'));
    console.log("Работает пагинация для списка не постов")
  }
  else if (block.querySelector('.is_load_paginate')) {
    scrolled(block.querySelector('.is_load_paginate'));
    console.log("Работает пагинация для списка в блоке")
  }
}
_ajax = document.getElementById('ajax');

create_pagination(_ajax);
init_music(_ajax);

function scrolled(_block) {
    onscroll = function() {
        try {
            box = _block.querySelector('.next_page_list');
            if (box && box.classList.contains("next_page_list")) {
                inViewport = elementInViewport(box);
                if (inViewport) {
                    box.classList.remove("next_page_list");
                    paginate(box);
                }
            };
        } catch {return}
    }
};

on('body', 'click', '.toggle_fixed_block', function() {
  try{
    document.body.querySelector(".notify_dropdown").style.display = "none";
    document.body.querySelector(".get_user_notify_box").classList.remove("show")
  } catch { null }
});
on('body', 'click', '.main-menu', function() {
  try{
    document.body.querySelector(".notify_dropdown").style.display = "none";
    document.body.querySelector(".get_user_notify_box").classList.remove("show");
  } catch { null }
});
function paginate(block) {
        var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        link_3.open('GET', location.protocol + "//" + location.host + block.getAttribute("data-link"), true);
        link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        link_3.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var elem = document.createElement('span');
                elem.innerHTML = link_3.responseText;
                if (elem.querySelector(".is_paginate")){
                  block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_paginate").innerHTML)
                } else if (document.body.querySelector(".is_load_paginate")){
                  block_paginate = document.body.querySelector(".is_load_paginate");
                  if (elem.querySelector(".is_load_paginate")){
                      block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_load_paginate").innerHTML)
                  } else {
                    block.parentElement.insertAdjacentHTML('beforeend', elem.innerHTML)
                  }};
                block.remove()
            }
        }
        link_3.send();
}

function get_select() {
  on('body', 'hover', '#russia_map path', function() {
    svg_list = this.parentElement.querySelectorAll("path");
    for (var i = 0; i < svg_list.length; i++) {
      if (svg_list[i].style.fill != "#897FF1"){
      svg_list[i].style.fill = "rgba(0,0,0,0.2)";
    }
    }
    if (this.style.fill != "#897FF1"){
    this.style.fill = "#FFFFFF";
  }

  },

  function(){
    svg_list = this.parentElement.querySelectorAll("path");
    for (var i = 0; i < svg_list.length; i++) {
      if (svg_list[i].style.fill != "#897FF1"){
      svg_list[i].style.fill = "rgba(0,0,0,0.15)";
    }
    }
  });
}; get_select();

function send_form_and_toast(url, form, toast) {
    form_data = new FormData(form);
    ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            toast_info(toast);
        }
    }
    ajax_link.send(form_data);
}

function get_image_priview(ggg, img) {
    entrou = false;
    img.click();
    img.onchange = function() {
        if (!entrou) {
            imgPath = img.value;
            extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
            if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg"|| extn == "webp") {
                if (typeof FileReader != "undefined") {
                    if (ggg) {}
                    ggg.innerHTML = "";
                    reader = new FileReader();
                    reader.onload = function(e) {
                        $img = document.createElement("img");
                        $img.src = e.target.result;
                        $img.class = "thumb-image";
                        $img.style.height = "100px";
                        //ggg.innerHTML = '<a href="#" style="right:15px;top: 0;" class="delete_thumb">Удалить</a>'
                        ggg.append($img)
                    };
                    reader.readAsDataURL(img.files[0])
                }
            } else {
                this.value = null
            }
        }
        entrou = true;
        setTimeout(function() {
            entrou = false
        }, 1000)
    }
};

function toast_success(text){
  var toasts = new ToastManager();
  toasts.showSuccess(text);
}
function toast_error(text){
  var toasts = new ToastManager();
  toasts.showError(text);
}
function toast_info(text){
  var toasts = new ToastManager();
  toasts.showInfo(text);
}
function toast_warning(text){
  var toasts = new ToastManager();
  toasts.showWarning(text);
}

function comment_delete(_this, _link, _class){
  data = _this.parentElement.parentElement;
  comment_pk = data.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + comment_pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    comment = data.parentElement.parentElement;
    comment.style.display = "none";
    div = document.createElement("div");
    div.classList.add("card");

    div.innerHTML = "<p class='" + _class + "'style='cursor:pointer;text-decoration:underline;padding:15px' data-pk='" + comment_pk + "'>Комментарий удален. Восстановить</p>";
    comment.parentElement.insertBefore(div, comment);
    comment.style.display = "none";
  }};
  link.send( );
}

function item_delete(_this, _link, old_class, new_class){
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + _this.parentElement.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.classList.replace(old_class, new_class)
    _this.innerHTML = "Отменить";
  }};
  link.send( );
}
function item_restore(_this, _link, old_class, new_class){
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + _this.parentElement.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.classList.replace(old_class, new_class)
    _this.innerHTML = "Удалить";
  }};
  link.send( );
}

function comment_abort_delete(_this, _link){
  comment = _this.parentElement.nextElementSibling;
  comment.style.display = "flex";
  pk = _this.getAttribute("data-pk");
  block = _this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
}

function load_chart() {
    try {
        var ctx = document.querySelector('#canvas');
        var dates = ctx.getAttribute('dates').split(",");
        var data_1 = ctx.getAttribute('data_views').split(",");
        var data_2 = ctx.getAttribute('data_member_views').split(",");
        var data_3 = ctx.getAttribute('data_likes').split(",");
        var data_4 = ctx.getAttribute('data_dislikes').split(",");
        var label_1 = ctx.getAttribute('label_views');
        var label_2 = ctx.getAttribute('label_member_views');
        var label_3 = ctx.getAttribute('label_likes');
        var label_4 = ctx.getAttribute('label_dislikes');
        var config = {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: label_1,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_1,
                    fill: false,
                }, {
                    label: label_2,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_2,
                }, {
                    label: label_3,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_3,
                }, {
                    label: label_4,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: ''
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }]
                }
            }
        };
        ctx.getContext('2d');
        window.myLine = new Chart(ctx, config)
    } catch {return}
}; load_chart();

function get_document_opacity_0() {
  document.body.style.overflow = "hidden";
  document.body.style.marginRight = "4px";
  overlay = document.body.querySelector(".body_overlay");
  overlay.style.visibility = "unset";
  overlay.style.opacity = "1";
  document.body.querySelector(".main-menu").style.zIndex = "10";
}
function get_document_opacity_1(block) {
  document.body.style.overflow = "scroll";
  document.body.style.marginRight = "0";
  overlay = document.body.querySelector(".body_overlay");
  overlay.style.visibility = "hidden";
  overlay.style.opacity = "0";
  document.body.querySelector(".main-menu").style.zIndex = "1031";
};

function ajax_get_reload(url) {
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        window.history.pushState("", document.title, url);
        document.title = elem_.querySelector('title').innerHTML;
        create_pagination(rtr);
        init_music(rtr);
        mobile_menu_close();
        try{document.body.querySelector(".notify_dropdown").style.display = "none"}catch{null};
        get_document_opacity_1(rtr)
      }
    }
    ajax_link.send();
}

function send_comment(form, block, link, prepend) {
    form_comment = new FormData(form);
    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link_.open('POST', link, true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    if (!form.querySelector(".text-comment").value && !form.querySelector(".comment_attach_block").firstChild){
      toast_error("Напишите или прикрепите что-нибудь");
      form.querySelector(".text-comment").style.border = "1px #FF0000 solid";
      form.querySelector(".dropdown").style.border = "1px #FF0000 solid";
      return
    };
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            form.querySelector(".text-comment").value = "";
            elem = link_.responseText;
            new_post = document.createElement("span");
            new_post.innerHTML = elem;
            prepend == "prepend" ? block.insertAdjacentHTML('afterBegin', new_post.innerHTML) : block.append(new_post);
            toast_success(" Комментарий опубликован");
            form.querySelector(".comment_attach_block").innerHTML = "";
            try {
                form_dropdown = form.querySelector(".current_file_dropdown");
                form_dropdown.classList.remove("current_file_dropdown");
                form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");
                form_dropdown.parentElement.parentElement.classList.add("files_null")
            } catch {
                null
            }
        }
    };
    link_.send(form_comment)
}
