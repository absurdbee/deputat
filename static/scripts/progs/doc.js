on('body', 'click', '.u_doc_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/add_list/", loader)
});
on('body', 'click', '.u_doc_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/create_doc/", loader)
});
on('body', 'click', '.u_doc_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_doc")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/edit_doc/" + parent.getAttribute("data-pk") +"/", loader)
});
on('body', 'click', '.u_doc_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/docs/user_progs/edit_list/" + uuid + "/", loader)
});
on('body', 'click', '.u_doc_list_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement;
  this.parentElement.parentElement.style.display = "none";

  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/docs/user_progs/delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    a = block.querySelector(".content-wrapper");
    e = a.querySelector(".file-name");
    e.classList.add("u_doc_list_abort_remove", "pointer");
    e.innerHTML = "Восстановить";
    a.nextElementSibling.innerHTML = "Удалённый"
  }}
  link_.send();
});
on('body', 'click', '.u_doc_list_abort_remove', function() {
  _this = this;
  block = this.parentElement.parentElement.parentElement.parentElement;
  block.querySelector(".dropdown").style.display = "block";
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/docs/user_progs/abort_delete_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.classList.remove("u_doc_list_abort_remove", "pointer");
    _this.innerHTML = _this.getAttribute("data-name");
    _this.parentElement.nextElementSibling.innerHTML = "Приватный"
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
  link_.open( 'POST', "/docs/user_progs/edit_list/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    close_create_window();
    title = form.querySelector('#id_name').value;

    album = document.body.querySelector(".list_active");
    album.querySelector(".doc_name").innerHTML = title;
    album.classList.remove("album_active");
    toast_success("Список изменен")
  }}
  link_.send(form_data);
});

on('body', 'click', '.u_add_doc_in_list', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.parentElement.parentElement.parentElement.getAttribute("data-pk");
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
  pk = parent.parentElement.parentElement.parentElement.getAttribute("data-pk");
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

on('body', 'click', '#u_create_doc_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
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
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/create_doc/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;

      if (document.body.querySelector(".current_file_dropdown")){
        pk = response.querySelector(".span_btn").getAttribute("data-pk");
        media_body = response.querySelector(".media-body");
        media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
        check_doc_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (doc_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_body, pk))
      } else if (document.body.querySelector(".attach_block")){
        pk = response.querySelector(".span_btn").getAttribute("data-pk");
        check_doc_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (doc_post_attach(document.body.querySelector(".attach_block"), response.querySelector(".media-body"), pk))
      } else if (document.body.querySector(".message_attach_block")){
        pk = response.querySelector(".span_btn").getAttribute("data-pk");
        check_doc_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (doc_message_attach(document.body.querySelector(".message_attach_block"), response.querySelector(".media-body"), pk))
      }
      else {
        uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
        span1 = response.querySelector('.span1')
        if (span1.classList.contains(uuid)){
          container = document.body.querySelector(".is_paginate");
      container.insertAdjacentHTML('afterBegin', response.innerHTML);
      container.querySelector(".doc_empty") ? container.querySelector(".doc_empty").style.display = "none" : null
    } else{ toast_info("Документ создан!")}
      toast_info("Документ создан!")
    }
    close_create_window();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_doc_btn', function() {
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
    toast_error("Загрузите документ!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/edit_doc/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Документ изменен!")
    close_create_window();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    doc = document.body.querySelector(".edited_doc");
    doc.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_doc_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Запись удалена. <span class='u_doc_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.parentElement.insertBefore(div, item), item.style.display = "none"
  }};
  link.send( );
});
on('body', 'click', '.u_doc_abort_remove', function() {
  item = this.parentElement.nextElementSibling;
  item.style.display = "block";
  pk = this.getAttribute("data-pk");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/abort_remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
});

on('body', 'click', '.u_load_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("doclist-pk");
  loader = document.getElementById("window_loader");
  open_fullscreen("/docs/load/" + pk + "/", loader)
});
