on('body', 'click', '.show_logs_elect_new', function() {
  create_fullscreen("/managers/logs/elect_new/" + this.getAttribute("data-pk") + "/", "worker_fullscreen");
});

on('body', 'click', '.select_manager_logs', function() {
  _this = this;
  lists_block = _this.parentElement.parentElement;
  slug = lists_block.getAttribute("data-link");
  if (slug == _this.getAttribute("data-link")) {
    return
  };
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', "/managers/logs" + _this.getAttribute("data-link") + lists_block.getAttribute("data-pk") + "/", true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ){
      lists_block.setAttribute("data-link", slug);
      elem_ = document.createElement('span');
      elem_.innerHTML = request.responseText;
      block = _this.parentElement.parentElement.parentElement.parentElement.parentElement;
      block.innerHTML = elem_.querySelector(".load_block").innerHTML;
      class_to_add = document.body.querySelectorAll(".list_toggle")
      for (var i = 0; i < class_to_add.length; i++) {
         class_to_add[i].classList.add("select_manager_logs", "pointer");
         _this.classList.remove("underline");
      };
     _this.classList.remove("select_manager_logs", "pointer");
     _this.classList.add("underline");
     create_pagination(document.body.querySelector(block))
    }};
    request.send( null );
});

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
       class_to_add = document.body.querySelectorAll(".list_toggle")
       for (var i = 0; i < class_to_add.length; i++) {
         class_to_add[i].classList.add(actions_class, "pointer");
         class_to_add[i].classList.replace("active_border", "border");
       };
       _this.classList.remove(actions_class, "pointer");
       _this.classList.replace("border", "active_border");
       create_pagination(document.body.querySelector(block))
    }};
    request.send( null );
};


on('body', 'click', '.manager_elect_delete', function() {
  string_send_change(this, "/managers/elect_new/delete_elect/", "manager_elect_restore", "manager_elect_delete", "ОТМЕНА")
});
on('body', 'click', '.manager_elect_restore', function() {
  string_send_change(this, "/managers/elect_new/restore_elect/", "manager_elect_delete", "manager_elect_restore", "УДАЛИТЬ")
});


function post_elect_new(_this, url, toast) {
  elect_id = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  try {
    if (form.querySelector("#id_elect").value){
      elect_id = true;
      form.querySelector("#id_elect").style.border = "1px #FF0000 solid"
    }} catch { null };
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  } else if (!elect_id){
    form.querySelector(".search_elect_field").style.border = "1px #FF0000 solid";
    toast_error("Выберите чиновника!"); return
  } else { _this.disabled = true };


  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    close_fullscreen();
    toast_info(toast);
    try {document.body.querySelector(".changed").remove()} catch { null }
  }};
  link.send(form_data);
};

on('body', 'click', '.add_media_list', function() {
  create_fullscreen("/managers/create_media_list/", "worker_fullscreen");
});

on('body', 'click', '.show_elect_rating_voters', function() {
  create_fullscreen("/elect/votes/show_elect_rating_voters/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "window_fullscreen");
});

on('body', 'click', '.edit_media_list', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  create_fullscreen("/managers/edit_media_list/" + uuid + "/", "worker_fullscreen");
});
on('body', 'click', '#add_media_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  _name = form.querySelector("#id_name");
  if (!_name.value){
    _name.style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true };

  form_data = new FormData(form);
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  ajax_link.open('POST', "/managers/create_media_list/", true);
  ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  ajax_link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          ajax_get_reload(window.location.href);
      }
  }
  ajax_link.send(form_data);
});
on('body', 'click', '#edit_media_list_btn', function() {
  media_list_edit(this, "/managers/edit_media_list/")
});
on('body', 'click', '.media_list_remove', function() {
  media_list_delete(this, "/managers/delete_list/", "media_list_remove", "media_list_recover")
});
on('body', 'click', '.media_list_recover', function() {
  media_list_recover(this, "/managers/abort_delete_list/", "media_list_recover", "media_list_remove")
});

on('body', 'click', '.u_elect_new_remove', function() {
  post_send_change(this.parentElement, "/blog/progs/delete_elect_new/", "u_elect_new_restore", "Отмена");
});
on('body', 'click', '.u_elect_new_restore', function() {
  post_send_change(this.parentElement, "/blog/progs/restore_elect_new/", "u_elect_new_remove", "Удалить");
});
on('body', 'click', '.u_blog_remove', function() {
  post_send_change(this.parentElement, "/blog/progs/delete_blog/", "u_blog_restore", "Отмена");
});
on('body', 'click', '.u_blog_restore', function() {
  post_send_change(this.parentElement, "/blog/progs/restore_blog/", "u_blog_restore", "Удалить");
});


on('body', 'click', '#_create_media_doc_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!"); return
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    input_file.style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "pdf" && format != "doc" && format != "docx" && format != "txt") {
    toast_error("Допустим формат файла pdf, doc, docx, txt!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_doc/create_doc/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    get_preview(response, "doc");
    toast_info("Документ создан!")
    close_fullscreen();
  }};

  link_.send(form_data);
});
on('body', 'click', '#edit_media_doc_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!"); return
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "pdf" && format != "doc" && format != "docx" && format != "txt") {
    toast_error("Допустим формат файла pdf, doc, docx, txt!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_doc/edit_doc/" + form.getAttribute("data-pk") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Документ изменен!")
    close_fullscreen();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    doc = document.body.querySelector(".edited_doc");
    doc.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.media_doc_add', function() {
  create_fullscreen("/managers/progs_doc/create_doc/", "worker_fullscreen");
});
on('body', 'click', '.media_doc_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_doc")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  create_fullscreen("/managers/progs_doc/edit_doc/" + parent.getAttribute("data-pk") +"/", "worker_fullscreen");
});

on('body', 'click', '.media_track_add', function() {
  create_fullscreen("/managers/progs_audio/create_track/", "worker_fullscreen");
});
on('body', 'click', '.media_track_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_track")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_track")
  create_fullscreen("/managers/progs_audio/edit_track/" + parent.getAttribute("data-pk") +"/", "worker_fullscreen");
});

on('body', 'click', '.media_video_add', function() {
  create_fullscreen("/managers/progs_video/create_video/", "worker_fullscreen");
});
on('body', 'click', '.media_video_edit', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_video")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  create_fullscreen("/managers/progs_video/edit_video/" + parent.getAttribute("data-pk") +"/", "worker_fullscreen");
});

on('body', 'change', '#media_photo_add', function() {
  form = this.parentElement;
  form_data = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_photo/create_photo/" + form.getAttribute("data-uuid") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".is_paginate").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".item_empty") ? document.body.querySelector(".item_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('body', 'click', '.u_edit_blog', function() {
  create_fullscreen("/blog/progs/edit_blog/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_edit_elect_new', function() {
  create_fullscreen("/blog/progs/edit_manager_elect_new/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "window_fullscreen");
});

on('body', 'click', '.manager_elect_create', function(e) {
  e.preventDefault();
  create_fullscreen("/managers/elect_new/create_elect/", "worker_fullscreen");
});
on('body', 'click', '.manager_elect_edit', function() {
  create_fullscreen("/managers/elect_new/edit_elect/" + this.getAttribute("data-pk") + "/", "worker_fullscreen");
});

on('body', 'click', '.manager_blog_create', function(e) {
  e.preventDefault();
  create_fullscreen("/blog/progs/add_blog/", "worker_fullscreen");
});

on('body', 'click', '.manager_elect_new_create', function() {
  loader = document.body.querySelector("#window_loader");
  if (this.getAttribute("data-name")) {
    create_elect_fullscreen("/managers/elect_new/create_elect_new/", this.getAttribute("data-name"))
  } else {
    create_fullscreen("/managers/elect_new/create_elect_new/", "window_fullscreen");
  }
});

on('body', 'click', '.penalty_photo', function() {
  this.parentElement.parentElement.classList.add("changed");
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/penalty_photo/" + pk + "/", "photo_fullscreen");
});
on('body', 'click', '.u_photo_moderated_detail', function() {
  this.parentElement.parentElement.classList.add("changed");
  pk = this.getAttribute('photo-pk');
  create_fullscreen("/gallery/moderated_photo/" + pk + "/", "photo_fullscreen");
});

on('body', 'click', '.u_publish_elect_new', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.classList.add("changed");
  create_fullscreen("/managers/elect_new/create_publish/" + this.parentElement.getAttribute("data-pk") + "/", "window_fullscreen");
});

on('body', 'click', '#create_blog_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  }
  else if (!form.querySelector("#id_image").value){
    form.querySelector("#holder_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку!"); return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/add_blog/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость создана!")
    close_fullscreen()
  } else { _this.disabled = false }};

  link_.send(form_data);
});

on('body', 'click', '#create_elect_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("ФИО - обязательное поле!"); return
  } else if (!form.querySelector("#id_list").value){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите орган власти!"); return
  } else if (!form.querySelector("#id_region").value){
    form.querySelector("#id_region").style.border = "1px #FF0000 solid";
    toast_error("Выберите регион!"); return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/elect_new/create_elect/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Чиновник создан!")
    close_fullscreen()
  } else { _this.disabled = false }};

  link_.send(form_data);
});

on('body', 'click', '#edit_elect_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("ФИО - обязательное поле!"); return
  } else if (!form.querySelector("#id_list").value){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите орган власти!"); return
  } else if (!form.querySelector("#id_region").value){
    form.querySelector("#id_region").style.border = "1px #FF0000 solid";
    toast_error("Выберите регион!"); return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/elect_new/edit_elect/" + _this.getAttribute("data-pk") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Чиновник изменён!")
    close_fullscreen()
  } else { _this.disabled = false }};

  link_.send(form_data);
});

on('body', 'click', '#edit_blog_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  }
  else if (!form.querySelector("#id_image").value){
    form.querySelector("#holder_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку!"); return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/edit_blog/" + this.getAttribute("data-pk") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость изменена!");
    close_fullscreen()
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_publish_elect_new_btn', function() {
  post_elect_new(this, "/managers/elect_new/create_publish/" + this.getAttribute("data-pk") + "/", "Активность опубликована!")

});
on('body', 'click', '#manager_create_elect_new_btn', function() {
  post_elect_new(this, "/managers/elect_new/create_elect_new/", "Активность создана и опубликована!")
});
on('body', 'click', '#u_edit_manage_elect_new_btn', function() {
  post_elect_new(this, "/blog/progs/edit_manager_elect_new/" + this.getAttribute("data-pk") + "/", "Активность изменена!")
});

on('body', 'click', '.show_object_reports', function() {
  if (this.getAttribute("obj-pk")) {
    pk = this.getAttribute("obj-pk")
  } else {
    pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("obj-pk")
  }
  create_fullscreen("/managers/load_claims/" + pk + "/", "window_fullscreen");
});

on('body', 'click', '.u_load_penalty_playlist', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/music/penalty_load/" + parent.getAttribute("playlist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_penalty_video_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/video/penalty_load/" + parent.getAttribute("videolist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_penalty_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/docs/penalty_load/" + parent.getAttribute("doclist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_penalty_survey_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/survey/penalty_load/" + parent.getAttribute("surveylist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_penalty_photo_list', function() {
  parent = this.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/gallery/penalty_load/" + parent.getAttribute("photolist-pk") + "/", "window_fullscreen");
});


on('body', 'click', '.u_load_moderated_photo_list', function() {
  parent = this.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/gallery/moderated_load/" + parent.getAttribute("photolist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_moderated_playlist', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/music/moderated_load/" + parent.getAttribute("playlist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_moderated_video_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/video/moderated_load/" + parent.getAttribute("videolist-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.u_load_moderated_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  create_fullscreen("/docs/moderated_load/" + parent.getAttribute("doclist-pk") + "/", "window_fullscreen");
});

on('body', 'click', '.create_user_close', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_close/")
})
on('body', 'click', '.create_user_warning_banner', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_warning_banner/")
})
on('body', 'click', '.create_user_suspend', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_suspension/")
})

on('body', 'click', '.create_user_blocker_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_close/", "create_user_close", "remove_user_close", "Аккаунт блокирован")
});
on('body', 'click', '.create_user_warning_banner_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_warning_banner/", "create_user_warning_banner", "remove_user_warning_banner", "Баннер применен")
});
on('body', 'click', '.create_user_suspend_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_suspension/", "create_user_suspend", "remove_user_suspend", "Аккаунт заморожен")
});

on('body', 'click', '.user_unverify', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("user-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/unverify/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});

on('body', 'click', '.remove_user_close', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("user-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/delete_close/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});

on('body', 'click', '.create_user_rejected', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = this.parentElement.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/create_rejected/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});


//////////////////////////// CLOSE ////////////////////
on('body', 'click', '.close_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_close/")
})
on('body', 'click', '.suspend_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_suspension/")
})
on('body', 'click', '.banner_create_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_warning_banner/")
})
on('body', 'click', '.u_close_photo_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_photo/list_create_close/")
})
on('body', 'click', '.u_close_photo', function() {
  get_item_sanction_window(this, "", "/managers/progs_photo/create_close/")
})
on('body', 'click', '.u_close_playlist', function() {
  get_item_sanction_window(this, "", "/managers/progs_audio/list_create_close/")
})
on('body', 'click', '.u_close_track', function() {
  get_music_doc_sanction_window(this, "", "/managers/progs_audio/create_close/")
})
on('body', 'click', '.u_close_video_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_video/list_create_close/")
})
on('body', 'click', '.u_close_video', function() {
  get_item_sanction_window(this, "", "/managers/progs_video/create_close/")
})
on('body', 'click', '.u_close_survey_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_survey/list_create_close/")
})
on('body', 'click', '.u_close_doc_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_doc/list_create_close/")
});
on('body', 'click', '.u_close_doc', function() {
  get_music_doc_sanction_window(this, "", "/managers/progs_doc/create_close/")
});

on('body', 'click', '.close_elect_new_comment', function() {
  get_comment_sanction_window(this, "/managers/elect_new/comment_create_close/")
});
on('body', 'click', '.close_blog_comment', function() {
  get_comment_sanction_window(this, "/managers/progs_blog/comment_create_close/")
});

on('body', 'click', '#create_blog_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_blog/create_close/", "Новость закрыта")
});
on('body', 'click', '#create_elect_new_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/elect_new/create_close/", "Активность закрыта")
});
on('body', 'click', '#create_photo_List_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_photo/list_create_close/", "Фотоальбом закрыт")
});
on('body', 'click', '#create_photo_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_photo/create_close/", "Фото закрыто")
});
on('body', 'click', '#create_playlist_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_audio/list_create_close/", "Плейлист закрыт")
});
on('body', 'click', '#create_track_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_audio/create_close/", "Аудиозапись закрыта")
});
on('body', 'click', '#create_doc_list_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_doc/list_create_close/", "Список документов закрыт")
});
on('body', 'click', '#create_doc_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_doc/create_close/", "Документ закрыт")
});
on('body', 'click', '#create_video_List_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_video/list_create_close/", "Список видеозаписей закрыт")
});
on('body', 'click', '#create_video_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_video/create_close/", "Видеозапись закрыта")
});
on('body', 'click', '#create_survey_list_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_survey/list_create_close/", "Список опросов закрыт")
});
on('body', 'click', '#create_blog_comment_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_blog/comment_create_close/", "Комментарий закрыт")
});
on('body', 'click', '#create_elect_new_comment_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/elect_new/comment_create_close/", "Комментарий закрыт")
});

on('body', 'click', '.remove_photo_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_delete_close/", "Фотоальбом восстановлен")
});
on('body', 'click', '.photo_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_photo_close', function() {
  send_window_sanction_get(this, "/managers/progs_photo/delete_close/", "Фото восстановлено")
});
on('body', 'click', '.photo_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_photo/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_elect_new_comment_close', function() {
  send_sanction_comments_get(this, "/managers/elect_new/comment_delete_close/", "Комментарий восстановлен")
});
on('body', 'click', '.elect_new_comment_unverify', function() {
  send_sanction_comments_get(this, "/managers/elect_new/comment_unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_blog_comment_close', function() {
  send_sanction_comments_get(this, "/managers/progs_blog/comment_delete_close/", "Комментарий восстановлен")
});
on('body', 'click', '.blog_comment_unverify', function() {
  send_sanction_comments_get(this, "/managers/progs_blog/comment_unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_playlist_close', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_delete_close/", "Плейлист восстановлен")
});
on('body', 'click', '.playlist_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_track_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_audio/delete_close/", "Аудиозапись восстановлена")
});
on('body', 'click', '.track_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_audio/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_video_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_delete_close/", "Видеоальбом восстановлен")
});
on('body', 'click', '.video_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_video_close', function() {
  send_window_sanction_get(this, "/managers/progs_video/delete_close/", "Видеоальбом восстановлен")
});
on('body', 'click', '.video_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_video/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_doc_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_delete_close/", "Список документов восстановлен")
});
on('body', 'click', '.doc_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_doc_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_doc/delete_close/", "Документ восстановлен")
});
on('body', 'click', '.doc_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_doc/unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_elect_new_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/elect_new/delete_close/", "Активность восстановлена")
});
on('body', 'click', '.elect_new_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/elect_new/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_survey_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_delete_close/", "Список опросов восстановлен")
});
on('body', 'click', '.survey_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_unverify/", "Верификация отменена")
});


on('body', 'click', '.create_photo_list_close', function() {
  open_manager_window(this, "/managers/progs_photo/list_create_close/")
});
on('body', 'click', '.create_photo_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_photo_close', function() {
  open_manager_window(this, "/managers/progs_photo/create_close/")
});
on('body', 'click', '.create_photo_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_photo/create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_playlist_close', function() {
  open_manager_window(this, "/managers/progs_audio/list_create_close/")
});
on('body', 'click', '.create_playlist_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_track_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_audio/create_close/")
});
on('body', 'click', '.create_track_rejected', function() {
  _this = this;
  send_window_sanction_get(_this, "/managers/progs_audio/create_rejected/", "Жалобы отклонены");
  _this.parentElement.parentElement.parentElement.parentElement.parentElement.remove()
});
on('body', 'click', '.reject_suggested_elect_new', function() {
  send_window_sanction_get(this, "/managers/elect_new/suggest_rejected/", "Активность отклонена")
});

on('body', 'click', '.create_video_list_close', function() {
  open_manager_window(this, "/managers/progs_video/list_create_close/")
});
on('body', 'click', '.create_video_list_rejected', function() {
  send_window_sanction_get(this, this.parentElement.parentElement.parentElement.parentElement.parentElement, "/managers/progs_video/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_video_close', function() {
  open_manager_window(this, "/managers/progs_video/create_close/")
});
on('body', 'click', '.create_video_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_doc_list_close', function() {
  open_manager_window(this, "/managers/progs_doc/list_create_close/")
});
on('body', 'click', '.create_doc_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_doc_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_doc/create_close/")
});
on('body', 'click', '.create_doc_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_doc/create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_elect_new_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/elect_new/create_close/")
});
on('body', 'click', '.create_elect_new_rejected', function() {
  send_window_sanction_get(this, "/managers/elect_new/create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_elect_new_comment_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/elect_new/comment_create_close/")
});
on('body', 'click', '.create_elect_new_comment_rejected', function() {
  send_window_sanction_get(this, "/managers/elect_new/comment_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_survey_list_close', function() {
  open_manager_window(this, "/managers/progs_survey/list_create_close/")
});
on('body', 'click', '.create_survey_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_blog_comment_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_blog/comment_create_close/")
});
on('body', 'click', '.create_blog_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_blog/create_close/")
});
on('body', 'click', '.create_blog_comment_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_blog/comment_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_blog_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_blog/create_rejected/", "Жалобы отклонены")
});


on('body', 'click', '#create_media_video_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");
  if (form.querySelector("#id_uri").value){
    input_file.value = "";
  }

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  }
  else if (!form.querySelector("#id_uri").value){
    if (!format) {
      input_file.style.border = "1px #FF0000 solid";
      form.querySelector("#id_uri").style.border = "1px #FF0000 solid";
      toast_error("Загрузите файл или вставьте ссылку!"); return
    }
    else if (findSize(input_file)> 5242880) {
      toast_error("Файл не должен превышать 5 Мб!"),
      form.querySelector(".form_file").style.color = "red";
      _this.disabled = false; return
    }
    else if (format != "mp4" && format != "mpeg4" && format != "avi") {
      toast_error("Допустим формат файла mp4, mpeg4, avi!"),
      form.querySelector(".form_file").style.color = "red";
      _this.disabled = false; return
    }
  }
  else if (!form.querySelector("#id_image")){
    form.querySelector("#id_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку к видео!"); return
  }
  else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_video/create_video/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    get_preview(response, "video");
    toast_info("Видеозапись создана!")
    close_fullscreen();
  }};

  link_.send(form_data);
});

on('body', 'click', '#media_create_doc_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");
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
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!")
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    input_file.style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "pdf" && format != "doc" && format != "docx" && format != "txt") {
    toast_error("Допустим формат файла pdf, doc, docx, txt!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_doc/create_doc/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    get_preview(response, "doc");
    toast_info("Документ создан!")
    close_fullscreen()
  }};

  link_.send(form_data);
});

on('body', 'click', '#create_media_track_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите аудиозапись!"); return
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "ogg" && format != "mp3" && format != "wav") {
    toast_error("Допустим формат файла ogg, mp3, wav!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_audio/create_track/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    get_preview(response, "track");
    toast_info("Аудиозапись создана!");
    init_music(document.body);
    close_fullscreen()
  } else { _this.disabled = true }};
  link_.send(form_data);
});


on('body', 'click', '.add_video_in_media_list', function() {
  add_item_in_list(this, '/managers/progs_video/add_video_in_list/', 'add_video_in_media_list', 'remove_video_from_media_list')
});
on('body', 'click', '.remove_video_from_media_list', function() {
  remove_item_from_list(this, '/managers/progs_video/remove_video_from_list/', 'remove_video_from_media_list', 'add_video_in_media_list', ".mob_media_video_remove")
});

on('body', 'click', '.add_photo_in_media_list', function() {
  add_item_in_list(this, '/managers/progs_photo/add_photo_in_list/', 'add_photo_in_media_list', 'remove_photo_from_media_list')
});
on('body', 'click', '.remove_photo_from_media_list', function() {
  remove_item_from_list(this, '/managers/progs_photo/remove_photo_from_list/', 'remove_photo_from_media_list', 'add_photo_in_media_list', ".mob_media_photo_remove")
});

on('body', 'click', '.mob_media_photo_remove', function() {
  mob_send_change(this, "/managers/progs_photo/delete/", "mob_media_photo_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
});
on('body', 'click', '.mob_media_photo_abort_remove', function() {
  mob_send_change(this, "/managers/progs_photo/abort_delete/", "mob_media_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
});

on('body', 'click', '.mob_media_video_remove', function() {
  mob_send_change(this, "/managers/progs_video/delete_video/", "mob_media_video_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
});
on('body', 'click', '.mob_media_video_abort_remove', function() {
  mob_send_change(this, "/managers/progs_video/abort_delete_video/", "mob_media_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
});


on('body', 'click', '.media_doc_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/managers/progs_doc/remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Документ удален. <span class='media_doc_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.media_doc_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/managers/progs_doc/abort_remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});


on('body', 'click', '.media_track_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/managers/progs_audio/delete_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Аудиозапись удалена. <span class='media_track_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.media_track_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/managers/progs_audio/abort_delete_track/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});
