on('body', 'click', '.add_track_in_media_list', function() {
  add_item_in_list(this, '/managers/progs_audio/add_track_in_list/', 'add_track_in_media_list', 'remove_track_from_media_list')
});
on('body', 'click', '.remove_track_from_media_list', function() {
  remove_item_from_list(this, '/managers/progs_audio/remove_track_from_list/', 'remove_track_from_media_list', 'add_track_in_media_list', ".media_track_remove")
});

on('body', 'click', '.add_track_in_media_list_collection', function() {
  item_send_change(this, "/music/user_progs/add_track_in_media_list/", "remove_track_from_media_list_collection", "Убрать из медиа-списка")
});
on('body', 'click', '.remove_track_from_media_list_collection', function() {
  item_send_change(this, "/music/user_progs/remove_track_from_media_list/", "add_track_in_media_list_collection", "Добавить в медиа-список")
});

on('body', 'click', '.u_track_list_add', function() {
  create_fullscreen("/music/user_progs/add_list/", "worker_fullscreen");
});
on('body', 'click', '.u_track_add', function() {
  create_fullscreen("/music/user_progs/create_track/", "worker_fullscreen");
});

on('body', 'click', '.u_copy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/add_list_in_collections/", "u_uncopy_playlist", "u_copy_playlist", "Удалить")
});
on('body', 'click', '.u_uncopy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/remove_list_from_collections/", "u_copy_playlist", "u_uncopy_playlist", "Добавить")
});

on('body', 'click', '.u_track_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_track")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_track")
  create_fullscreen("/music/user_progs/edit_track/" + parent.getAttribute("data-pk") +"/", "worker_fullscreen");
});
on('body', 'click', '.u_playlist_add', function() {
  create_fullscreen("/music/user_progs/create_list/", "worker_fullscreen");
});
on('body', 'click', '.u_playlist_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/music/user_progs/edit_list/" + uuid + "/", "worker_fullscreen");
});

on('body', 'click', '.u_playlist_remove', function() {
  media_list_delete(this, "/music/user_progs/delete_list/", "u_playlist_remove", "u_playlist_abort_remove")
});
on('body', 'click', '.u_playlist_abort_remove', function() {
  media_list_recover(this, "/music/user_progs/abort_delete_list/", "u_playlist_abort_remove", "u_playlist_remove")
});

on('body', 'click', '#u_create_playlist_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/music/user_progs/create_list/", "/music/user_list/");
});

on('body', 'click', '#u_edit_playlist_btn', function() {
  media_list_edit(this, "/music/user_progs/edit_list/")
});

on('body', 'click', '.u_add_track_in_list', function() {
  add_item_in_list(this, '/music/user_progs/add_track_in_list/', 'u_add_track_in_list', 'u_remove_track_from_list')
})
on('body', 'click', '.u_remove_track_from_list', function() {
  remove_item_from_list(this, '/music/user_progs/remove_track_from_list/', 'u_remove_track_from_list', 'u_add_track_in_list', ".u_track_remove")
})

on('body', 'click', '#u_create_track_btn', function() {
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
  link_.open( 'POST', "/music/user_progs/create_track/", true );
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

on('body', 'click', '#u_edit_track_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
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
  else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/music/user_progs/edit_track/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аудиозапись изменена!")
    close_fullscreen();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    track = document.body.querySelector(".edited_track");
    track.innerHTML = response.querySelector(".pag").innerHTML;
    init_music(track);
  } else { this.disabled = false }};

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
  create_fullscreen("/music/user_load/" + parent.getAttribute("playlist-pk") + "/", "window_fullscreen");
});

on('body', 'click', '.u_load_profile_playlist', function() {
  profile_list_block_load(this, ".load_block", "/music/user_list/" + this.getAttribute("data-uuid") + "/", "u_load_profile_playlist");
});
on('body', 'click', '.u_load_attach_playlist', function() {
  profile_list_block_load(this, ".is_load_paginate", "/users/load/u_playlist_load/" + this.getAttribute("data-uuid") + "/", "u_load_attach_playlist");
});
