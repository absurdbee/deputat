on('body', 'click', '.u_album_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_album/", loader)
});
on('body', 'click', '.u_album_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("album_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("album_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/edit_album/" + uuid + "/", loader)
});
on('body', 'click', '.u_album_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/user_progs/delete_album/" + uuid + "/", true );
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
on('body', 'click', '.u_album_abort_remove', function() {
  block = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = block.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/gallery/user_progs/abort_delete_album/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    block.querySelector(".delete_card").remove();
    block.querySelector(".card").style.display = "block";
  }}
  link_.send();
});

on('body', 'click', '#u_create_album_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/gallery/user_progs/add_album/", "/gallery/album/", "/");
});

on('body', 'click', '#u_edit_album_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/edit_album/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    title = form.querySelector('#id_title').value;

    album = document.body.querySelector(".album_active");
    album.querySelector("h6").innerHTML = title;
    album.classList.remove("album_active");
    close_create_window();
    toast_success("Альбом изменен")
  }}
  link_.send(form_data);
});

on('body', 'change', '#u_photo_add', function() {
  uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_photo/" + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector("#photos_container").insertAdjacentHTML('afterBegin', response.innerHTML);
    document.body.querySelector(".photos_empty") ? document.body.querySelector(".photos_empty").style.display = "none" : null
  }}
  link_.send(form_data);
});

on('body', 'click', '.mob_user_photo_remove', function() {
  mob_send_change(this, "/gallery/user_progs/delete/", "mob_user_photo_abort_remove", "Отмена");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "none";
  post.querySelector(".image_card").style.opacity = "0.5";
})
on('body', 'click', '.mob_user_photo_abort_remove', function() {
  mob_send_change(this, "/gallery/user_progs/abort_delete/", "mob_user_photo_remove", "Удалить");
  post = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  post.querySelector(".content_block").style.display = "unset";
  post.querySelector(".image_card").style.opacity = "1";
})
on('body', 'click', '.mob_u_photo_off_private', function() {
  mob_send_change(this, "/gallery/user_progs/off_private/", "mob_u_photo_on_private", "Вкл. приватность")
})
on('body', 'click', '.mob_u_photo_on_private', function() {
  mob_send_change(this, "/gallery/user_progs/on_private/", "mob_u_photo_off_private", "Выкл. приватность")
})
on('body', 'click', '.u_add_photo_in_album', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/gallery/user_progs/add_photo_in_album/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_add_photo_in_album");
    list.style.paddingLeft = "14px";
    list.classList.add("u_remove_photo_in_album");
    list.classList.remove("u_add_photo_in_album");
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    list.prepend(span)
  }};
  link.send( null );
})
on('body', 'click', '.u_remove_photo_in_album', function() {
  _this = this;
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = parent.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', '/gallery/user_progs/remove_photo_in_album/' + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    list = parent.querySelector(".u_remove_photo_in_album");
    list.style.paddingLeft = "30px";
    list.classList.add("u_add_photo_in_album");
    list.classList.remove("u_remove_photo_in_album");
    list.querySelector("svg").remove();
  }};
  link.send( null );
})

on('body', 'click', '.u_photo_detail', function() {
  pk = this.getAttribute('photo-pk');
  this.parentElement.parentElement.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.parentElement.parentElement.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/photo/" + pk + "/" + uuid + "/", loader)
});

on('body', 'click', '.next_photo', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('photo_loader'));
})
on('body', 'click', '.prev_photo', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('photo_loader'));
})

on('body', 'click', '.photo_fullscreen_hide_2', function() {
  this.parentElement.parentElement.parentElement.parentElement.parentElement.style.display = "none";
  this.parentElement.parentElement.parentElement.parentElement.innerHTML = "";
});

on('body', 'click', '.u_blog_comment_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  comment_pk = this.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/blog_comment_photo/" + comment_pk + "/" + photo_pk + "/", loader)
});
on('body', 'click', '.u_elect_new_comment_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  comment_pk = this.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/elect_new_comment_photo/" + comment_pk + "/" + photo_pk + "/", loader)
});
on('body', 'click', '.u_load_photo_album', function() {
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute("photoalbum-pk");
  loader = document.getElementById("window_loader");
  open_fullscreen("/gallery/load_album/" + pk + "/", loader)
});

on('body', 'click', '.u_add_photo_album', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/add_list/", "u_remove_photo_album", "u_add_photo_album", "Удалить")
});
on('body', 'click', '.u_remove_photo_album', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/remove_list/", "u_add_photo_album", "u_remove_photo_album", "Добавить")
});
on('body', 'click', '.u_copy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/add_list/", "u_uncopy_playlist", "u_copy_playlist", "Удалить")
});
on('body', 'click', '.u_uncopy_playlist', function() {
  on_off_list_in_collections(this, "/music/user_progs/remove_list/", "u_copy_playlist", "u_uncopy_playlist", "Добавить")
});
