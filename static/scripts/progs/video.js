on('body', 'click', '.add_video_in_media_list_collection', function() {
  mob_send_change(this, "/video/user_progs/add_video_in_media_list/", "remove_video_from_media_list_collection", "Убрать из медиа-списка")
});
on('body', 'click', '.remove_video_from_media_list_collection', function() {
  mob_send_change(this, "/video/user_progs/remove_video_from_media_list/", "add_video_in_media_list_collection", "Добавить в медиа-список")
});

on('body', 'click', '.add_video_in_media_list_collection_2', function() {
  item_send_change(this, "/video/user_progs/add_video_in_media_list/", "remove_video_from_media_list_collection_2", "Убрать из медиа-списка")
});
on('body', 'click', '.remove_video_from_media_list_collection_2', function() {
  item_send_change(this, "/video/user_progs/remove_video_from_media_list/", "add_video_in_media_list_collection_2", "Добавить в медиа-список")
});

on('body', 'click', '.u_video_list_add', function() {
  create_fullscreen("/video/user_progs/add_list/", "worker_fullscreen")
});
on('body', 'click', '.u_video_add', function() {
  create_fullscreen("/video/user_progs/create_video/", "worker_fullscreen")
});
on('body', 'click', '.u_video_edit', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("video-pk");
  blocks = document.body.querySelectorAll('.u_video_detail');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_video")}
  try{
    cur_video = document.body.querySelector('[video-pk=' + '"' + pk + '"' + ']')
    cur_video.classList.add("edited_video")
  } catch { null }
  create_fullscreen("/video/user_progs/edit_video/" + pk +"/", "worker_fullscreen")
});

on('body', 'click', '.u_video_detail', function() {
  video_pk = this.getAttribute('video-pk');
  uuid = this.parentElement.getAttribute("data-uuid");
  create_fullscreen("/video/user_detail/" + video_pk + "/" + uuid + "/", "window_fullscreen")
});
on('body', 'click', '.media_video_detail', function() {
  video_pk = this.getAttribute('video-pk');
  uuid = this.parentElement.parentElement.parentElement.parentElement.previousElementSibling.getAttribute('data-uuid');
  create_fullscreen("/video/media_video_detail/" + video_pk + "/" + uuid + "/", "window_fullscreen")
});

on('body', 'click', '#u_edit_video_list_btn', function() {
  media_list_edit(this, "/video/user_progs/edit_list/")
});

on('body', 'click', '.u_video_list_edit', function() {
  uuid = this.parentElement.parentElement.getAttribute('data-uuid');
  create_fullscreen("/video/user_progs/edit_list/" + uuid + "/", "worker_fullscreen")
});

on('body', 'click', '.u_video_list_remove', function() {
  media_list_delete(this, "/video/user_progs/delete_list/", "u_video_list_remove", "u_video_list_abort_remove")
});
on('body', 'click', '.u_video_list_abort_remove', function() {
  media_list_recover(this, "/video/user_progs/abort_delete_list/", "u_video_list_abort_remove", "u_video_list_remove")
});

on('body', 'click', '.u_copy_video_list', function() {
  on_off_list_in_collections(this, "/video/user_progs/add_list_in_collections/", "u_uncopy_video_list", "u_copy_video_list", "Удалить")
});
on('body', 'click', '.u_uncopy_video_list', function() {
  on_off_list_in_collections(this, "/video/user_progs/remove_list_from_collections/", "u_copy_video_list", "u_uncopy_video_list", "Добавить")
});

on('body', 'click', '#u_create_video_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/video/user_progs/add_list/", "/video/user_list/");
});

on('body', 'click', '#u_edit_playlist_btn', function() {
  media_list_edit(this, "/video/user_progs/edit_list/")
});

on('body', 'click', '.u_add_video_in_list', function() {
  add_item_in_list(this, '/video/user_progs/add_video_in_list/', 'u_add_video_in_list', 'u_remove_video_from_list')
})
on('body', 'click', '.u_remove_video_from_list', function() {
  remove_item_from_list(this, '/video/user_progs/remove_video_from_list/', 'u_remove_video_from_list', 'u_add_video_in_list', ".mob_user_video_remove")
})

on('body', 'click', '#u_create_video_btn', function() {
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
  if (!form.querySelector("#id_image")){
    form.querySelector("#id_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку к видео!"); return
  }
  else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/user_progs/create_video/", true );
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

on('body', 'click', '#u_edit_video_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
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
    toast_error("Название - обязательное поле!"); return
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
  link_.open( 'POST', "/video/user_progs/edit_video/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Видеозапись изменена!")
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    try{
      video = document.body.querySelector(".edited_video");
      video.innerHTML = response.querySelector(".pag").innerHTML
    } catch { null };
    close_fullscreen();
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_video_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/video/user_progs/remove_video/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Видеоапись удалена. <span class='u_videoabort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_video_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/video/user_progs/abort_remove_video/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('body', 'click', '.u_load_video_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("videolist-pk");
  create_fullscreen("/video/user_load/" + pk + "/", "window_fullscreen")
});

on('body', 'click', '.u_load_profile_video_list', function() {
  profile_list_block_load(this, ".load_block", "/video/user_list/" + this.getAttribute("data-uuid") + "/", "u_load_profile_video_list");
});

on('body', 'click', '.u_load_attach_video_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_video_list_load/" + this.getAttribute("data-uuid") + "/", "u_load_attach_video_list");
});

on('body', 'click', '.mob_user_video_remove', function() {
  mob_send_change(this, "/video/user_progs/delete_video/", "mob_user_video_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
})
on('body', 'click', '.mob_user_video_abort_remove', function() {
  mob_send_change(this, "/video/user_progs/abort_delete_video/", "mob_user_video_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
})
on('body', 'click', '.mob_u_video_off_private', function() {
  mob_send_change(this, "/video/user_progs/off_private/", "mob_u_video_on_private", "Вкл. приватность")
})
on('body', 'click', '.mob_u_video_on_private', function() {
  mob_send_change(this, "/video/user_progs/on_private/", "mob_u_video_off_private", "Выкл. приватность")
})
