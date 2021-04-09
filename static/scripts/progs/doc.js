on('body', 'click', '.u_doc_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/add_list/", loader)
});
on('body', 'click', '.u_doc_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/create_doc/", loader)
});
on('body', 'click', '.u_doc_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/edit_list/" + uuid + "/", loader)
});
on('body', 'click', '.u_doc_list_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/docs/user_progs/delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".card").style.display = "none";
    $block = document.createElement("div");
    $block.classList.add("card", "delete_card");
    $block.innerHTML = '<div class="card-header"><div class="media"><div class="media-body"><h6 class="mb-0 u_album_abort_remove pointer">Восстановить</h6></div></div></div><div class="card-body"><a><img style="object-fit: cover;height: 150px;width: 170px;" src="/static/images/album.jpg" /></a></div>'
    block.append($block);
  }}
  link_.send();
});
on('body', 'click', '.u_doc_list_abort_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/docs/user_progs/abort_delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".delete_card").remove();
    block.querySelector(".card").style.display = "block";
  }}
  link_.send();
});

on('body', 'click', '#u_create_doc_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/docs/user_progs/add_list/", "/docs/list/", "/");
});

on('body', 'click', '#u_edit_doc_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/edit_doc_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    title = form.querySelector('#id_name').value;

    album = document.body.querySelector(".album_active");
    album.querySelector("h6").innerHTML = title;
    album.classList.remove("album_active");
    close_create_window();
    toast_success("Список изменен")
  }}
  link_.send(form_data);
});

on('body', 'click', '.mob_user_doc_remove', function() {
  mob_send_change(this, "/docs/user_progs/delete/", "mob_user_photo_abort_remove", "Отмена");
  toast_success("Список изменен")
})
on('body', 'click', '.mob_user_doc_abort_remove', function() {
  mob_send_change(this, "/docs/user_progs/abort_delete/", "mob_user_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
})
on('body', 'click', '.mob_u_photo_off_private', function() {
  mob_send_change(this, "/docs/user_progs/off_private/", "mob_u_photo_on_private", "Вкл. приватность")
})
on('body', 'click', '.mob_u_photo_on_private', function() {
  mob_send_change(this, "/docs/user_progs/on_private/", "mob_u_photo_off_private", "Выкл. приватность")
})
on('body', 'click', '.u_add_doc_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/docs/user_progs/add_doc_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_add_doc_in_list");
    list.style.paddingLeft = "14px";
    list.classList.add("u_remove_doc_in_list");
    list.classList.remove("u_add_doc_in_list");
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    list.prepend(span)
  }};
  link.send( null );
})
on('body', 'click', '.u_remove_doc_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/docs/user_progs/remove_doc_in_list/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_remove_doc_in_list");
    list.style.paddingLeft = "30px";
    list.classList.add("u_add_doc_in_list");
    list.classList.remove("u_remove_doc_in_list");
    list.querySelector("svg").remove();
  }};
  link.send( null );
})

on('body', 'click', '.u_load_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  loader = document.getElementById("window_loader");
  open_fullscreen("/docs/load/" + pk + "/", loader)
});

on('#ajax', 'click', '#u_create_doc_btn', function() {
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
    toast_error("Загрузите документ!")
  } else { this.disabled = true }

  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/create_doc/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    span1 = response.querySelector('.span1')
    if (span1.classList.contains(uuid)){
      container = document.body.querySelector(".is_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".doc_empty") ? container.querySelector(".doc_empty").style.display = "none" : null;
      toast_info("Документ создан!")
    } else{
      toast_info("Документ создан!")
    }
    close_create_window();
  }};

  link_.send(form_data);
});
