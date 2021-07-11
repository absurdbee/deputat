on('body', 'click', '.u_photo_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/add_list/", loader)
});
on('body', 'click', '.u_photo_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user_progs/edit_list/" + uuid + "/", loader)
});

on('body', 'click', '.u_photo_list_remove', function() {
  media_list_delete(this, "/gallery/user_progs/delete_list/", "u_photo_list_remove", "u_photo_list_abort_remove")
});
on('body', 'click', '.u_photo_list_abort_remove', function() {
  media_list_recover(this, "/gallery/user_progs/abort_delete_list/", "u_photo_list_abort_remove", "u_photo_list_remove")
});

on('body', 'click', '#u_create_photo_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/gallery/user_progs/add_list/", "/gallery/user_list/", "/");
});

on('body', 'click', '#u_edit_photo_list_btn', function() {
  media_list_edit(this, "/gallery/user_progs/edit_list/")
});

on('body', 'change', '#u_photo_add', function() {
  uuid = this.parentElement.parentElement.getAttribute("data-uuid");
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
    document.body.querySelector(".item_empty") ? document.body.querySelector(".item_empty").style.display = "none" : null
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

on('body', 'click', '.u_add_photo_in_list', function() {
  add_item_in_list(this, '/gallery/user_progs/add_photo_in_list/', 'u_add_photo_in_list', 'u_remove_photo_from_list')
})
on('body', 'click', '.u_remove_photo_from_list', function() {
  remove_item_from_list(this, '/gallery/user_progs/remove_photo_from_list/', 'u_remove_photo_from_list', 'u_add_photo_in_list', ".u_photo_remove")
})

on('body', 'click', '.u_photo_detail', function() {
  pk = this.getAttribute('photo-pk');
  this.parentElement.getAttribute('data-uuid') ? uuid = this.parentElement.getAttribute('data-uuid') : uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid')
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
on('body', 'click', '.u_blog_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  comment_pk = this.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/blog_photo/" + comment_pk + "/" + photo_pk + "/", loader)
});
on('body', 'click', '.u_elect_new_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  comment_pk = this.parentElement.parentElement.parentElement.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/elect_new_photo/" + comment_pk + "/" + photo_pk + "/", loader)
});

on('body', 'click', '.u_load_photo_list', function() {
  parent = this.parentElement.parentElement;
  pk = parent.getAttribute("photolist-pk");
  loader = document.getElementById("window_loader");
  open_fullscreen("/gallery/user_load/" + pk + "/", loader)
});

on('body', 'click', '.u_copy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/add_list_in_collections/", "u_uncopy_photo_list", "u_copy_photo_list", "Удалить")
});
on('body', 'click', '.u_uncopy_photo_list', function() {
  on_off_list_in_collections(this, "/gallery/user_progs/remove_list_from_collections/", "u_copy_photo_list", "u_uncopy_photo_list", "Добавить")
});

on('body', 'click', '.u_load_profile_photo_list', function() {
  profile_list_block_load(this, ".load_block", "/gallery/user_list/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_profile_photo_list");
});

on('body', 'click', '.u_load_attach_photo_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_photo_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_attach_photo_list");
});
