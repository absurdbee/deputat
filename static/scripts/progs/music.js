on('body', 'click', '.u_track_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/add_list/", loader)
});
on('body', 'click', '.u_track_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/create_track/", loader)
});


on('body', 'click', '.u_track_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_track")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_track")
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/edit_track/" + parent.getAttribute("data-pk") +"/", loader)
});
on('body', 'click', '.u_playlist_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/create_list/", loader)
});
on('body', 'click', '.u_playlist_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/edit_list/" + uuid + "/", loader)
});
on('body', 'click', '.u_playlist_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.style.display = "none";

  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/music/user_progs/delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    a = block.querySelector(".content-wrapper");
    e = a.querySelector(".file-name");
    e.classList.add("u_playlist_abort_remove", "pointer");
    e.innerHTML = "Восстановить";
    a.nextElementSibling.innerHTML = "Удалённый"
  }}
  link_.send();
});
on('body', 'click', '.u_playlist_abort_remove', function() {
  _this = this;
  block = this.parentElement.parentElement.parentElement.parentElement;
  block.querySelector(".dropdown").style.display = "block";
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/music/user_progs/abort_delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.classList.remove("u_playlist_abort_remove", "pointer");
    _this.innerHTML = _this.getAttribute("data-name");
    _this.parentElement.nextElementSibling.innerHTML = "Приватный"
  }}
  link_.send();
});

on('body', 'click', '#u_create_playlist_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/user_progs/create_list/", "/music/list/", "/");
});

on('body', 'click', '#u_edit_playlist_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/user_progs/edit_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    close_create_window();
    title = form.querySelector('#id_name').value;

    list = document.body.querySelector(".list_active");
    list.querySelector(".playlist_name").innerHTML = title;
    list.classList.remove("list_active");
    toast_success("Список изменен")
  }}
  link_.send(form_data);
});

on('body', 'click', '.u_add_track_in_list', function() {
  add_item_in_list(this, '/music/user_progs/add_track_in_list/', '.u_add_track_in_list', '.u_remove_track_from_list')
})
on('body', 'click', '.u_remove_doc_from_list', function() {
  remove_item_from_list(this, '/music/user_progs/remove_track_from_list/', '.u_remove_track_from_list', '.u_add_track_in_list')
})

on('body', 'click', '#u_create_track_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите аудиозапись!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/user_progs/create_track/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".pk_saver").getAttribute("data-uuid") ? (
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid"),
      check_span1(response.querySelector('.span1'), uuid, response.innerHTML),
      document.body.querySelector(".track_empty") ? document.body.querySelector(".track_empty").style.display = "none" : null) : get_preview(response, "track");
    toast_info("Аудиозапись создана!")
    close_create_window();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_track_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
  form_data = new FormData(form);

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите аудиозапись!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/edit_doc/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аудиозапись изменена!")
    close_create_window();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    doc = document.body.querySelector(".edited_track");
    doc.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_track_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/user_progs/delete_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Аудиозапись удалена. <span class='u_track_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_track_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/music/user_progs/abort_delete_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('body', 'click', '.u_load_playlist', function() {
  parent = this.parentElement.parentElement.parentElement;
  console.log(parent.getAttribute("playlist-pk"))
  open_fullscreen("/music/load/" + parent.getAttribute("playlist-pk") + "/", document.getElementById("window_loader"))
});

on('body', 'click', '.u_load_profile_playlist', function() {
  list_block_load(".is_paginate", ".is_paginate", "/music/list/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/")
});
