on('body', 'click', '.u_video_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user_progs/add_list/", loader)
});
on('body', 'click', '.u_video_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user_progs/create_video/", loader)
});
on('body', 'click', '.u_video_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_video")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_video")
  loader = document.getElementById("create_loader");
  open_fullscreen("/video/user_progs/edit_video/" + parent.getAttribute("data-pk") +"/", loader)
});

on('body', 'click', '.next_video', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('window_loader'));
})
on('body', 'click', '.prev_video', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('window_loader'));
})

on('body', 'click', '.u_video_detail', function() {
  video_pk = this.getAttribute('video-pk');
  loader = document.getElementById("window_loader");
  open_fullscreen("/video/user_detail/" + video_pk + "/", loader)
});

on('body', 'click', '#u_edit_video_list_btn', function() {
  media_list_edit(this, "/video/user_progs/edit_list/")
});

on('body', 'click', '.u_video_list_remove', function() {
  media_list_delete(this, "/video/user_progs/delete_list/", "u_video_list_remove", "u_video_list_abort_remove")
});
on('body', 'click', '.u_video_list_abort_remove', function() {
  media_list_recover(this, "/video/user_progs/abort_delete_list/", "u_video_list_abort_remove", "u_video_list_remove")
});

on('body', 'click', '#u_create_video_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/video/user_progs/add_list/", "/video/user_list/", "/");
});

on('body', 'click', '#u_edit_playlist_btn', function() {
  media_list_edit(this, "/video/user_progs/edit_list/")
});

on('body', 'click', '.u_add_video_in_list', function() {
  add_item_in_list(this, '/video/user_progs/add_track_in_list/', 'u_add_video_in_list', 'u_remove_video_in_list')
})
on('body', 'click', '.u_remove_video_in_list', function() {
  remove_item_from_list(this, '/video/user_progs/remove_track_from_list/', 'u_remove_video_in_list', 'u_add_video_in_list')
})

on('body', 'click', '#u_create_video_btn', function() {
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
  else if (!form.querySelector("#id_file").value && !form.querySelector("#id_uri").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    form.querySelector("#id_uri").style.border = "1px #FF0000 solid";
    toast_error("Загрузите файл или вставьте ссылку!")
  }
  else if (!form.querySelector("#id_file").value && form.querySelector("#id_uri").value && !form.querySelector("#id_image")){
    form.querySelector("#id_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку к видео!")
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/user_progs/create_video/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".pk_saver").getAttribute("data-uuid") ? (
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid"),
      check_span1(response.querySelector('.span1'), uuid, response.innerHTML),
      document.body.querySelector(".item_empty") ? document.body.querySelector(".item_empty").style.display = "none" : null) : get_preview(response, "video");
    toast_info("Видеозапись создана!")
    close_create_window();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_video_btn', function() {
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
    toast_error("Загрузите видеозапись!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/user_progs/edit_video/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Видеозапись изменена!")
    close_create_window();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    video = document.body.querySelector(".edited_video");
    video.innerHTML = response.querySelector(".pag").innerHTML;
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
  loader = document.getElementById("window_loader");
  open_fullscreen("/video/user_load/" + pk + "/", loader)
});

on('body', 'click', '.u_load_profile_video_list', function() {
  profile_list_block_load(this, ".load_block", "/video/user_list/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_profile_video_list");
});

on('body', 'click', '.u_load_attach_video_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_video_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_attach_video_list");
});
