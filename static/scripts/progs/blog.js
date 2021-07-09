function send_like(item, url){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  inert = item.querySelector(".inert");

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    inerts_count = item.querySelector(".inerts_count");

    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    inerts_count.innerHTML = jsonResponse.inert_count;

    like.classList.toggle("btn_success");
    dislike.classList.remove("btn_danger");
    inert.classList.remove("btn_inert");
  }};
  link.send( null );
}
function send_comment_like(item, url){
  like = item.querySelector(".like");

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    like.classList.toggle("btn_success");
    console.log(jsonResponse.like_count)
  }};
  link.send( null );
}

function send_dislike(item, url){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  inert = item.querySelector(".inert");

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    inerts_count = item.querySelector(".inerts_count");

    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    inerts_count.innerHTML = jsonResponse.inert_count;

    dislike.classList.toggle("btn_danger");
    like.classList.remove("btn_success");
    inert.classList.remove("btn_inert");
  }};
  link.send( null );
}
function send_inert(item, url){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  inert = item.querySelector(".inert");

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    inerts_count = item.querySelector(".inerts_count");

    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    inerts_count.innerHTML = jsonResponse.inert_count;

    dislike.classList.remove("btn_danger");
    like.classList.remove("btn_success");
    inert.classList.toggle("btn_inert");
  }};
  link.send( null );
}

on('body', 'click', '.elect_new_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/elect_new_like/" + pk + "/");
});
on('body', 'click', '.elect_new_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/elect_new_dislike/" + pk + "/");
});
on('body', 'click', '.elect_new_inert', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_inert(item, "/blog/votes/elect_new_inert/" + pk + "/");
});

on('body', 'click', '.blog_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/blog_like/" + pk + "/");
});
on('body', 'click', '.blog_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/blog_dislike/" + pk + "/");
});
on('body', 'click', '.blog_inert', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_inert(item, "/blog/votes/blog_inert/" + pk + "/");
});

on('body', 'click', '.remove_blog_comment', function() {
  comment_delete(this, "/blog/delete_blog_comment/", "restore_blog_comment")
});
on('body', 'click', '.restore_blog_comment', function() {
  comment_abort_delete(this, "/blog/restore_blog_comment/")
})

on('body', 'click', '.remove_elect_new_comment', function() {
  comment_delete(this, "/blog/delete_new_comment/", "restore_elect_new_comment")
});
on('body', 'click', '.restore_elect_new_comment', function() {
  comment_abort_delete(this, "/blog/restore_new_comment/")
})

on('body', 'click', '.delete_elect_new', function() {
  item_delete(this, "/blog/progs/delete_elect_new/", "delete_elect_new", "restore_elect_new")
});
on('body', 'click', '.restore_elect_new', function() {
  item_restore(this, "/blog/progs/restore_elect_new/", "restore_elect_new", "delete_elect_new")
});

on('body', 'click', '.blog_comment_like', function() {
  item = this.parentElement.parentElement;
  send_comment_like(item, "/blog/votes/blog_comment_like/" + item.getAttribute("data-pk") + "/");
});
on('body', 'click', '.elect_new_comment_like', function() {
  item = this.parentElement.parentElement;
  send_comment_like(item, "/blog/votes/elect_new_comment_like/" + item.getAttribute("data-pk") + "/");
}); 

on('body', 'click', '.edit_blog_comment', function() {
  _this = this;
  clear_comment_dropdown();
  _this.parentElement.style.display = "none";
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/blog/edit_blog_comment/" + _this.parentElement.parentElement.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    elem = link.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    _this.parentElement.parentElement.append(response);
  }};
  link.send( null );
});

on('body', 'click', '.edit_elect_new_comment', function() {
  _this = this;
  clear_comment_dropdown();
  _this.parentElement.style.display = "none";
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/blog/edit_new_comment/" + _this.parentElement.parentElement.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    elem = link.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    _this.parentElement.parentElement.append(response);
  }};
  link.send( null );
});

on('body', 'click', '.edit_elect_new', function() {
  clear_comment_dropdown();
  loader = document.getElementById("window_loader");
  open_fullscreen("/blog/progs/edit_elect_new/" + this.parentElement.getAttribute("data-pk") + "/", loader)
});
on('body', 'click', '#u_edit_elect_new_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/blog/progs/edit_elect_new/" + _this.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    elem = link.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector("#ajax").innerHTML = response.querySelector("#ajax").innerHTML;
  }};
  link.send(form_data);
});

on('body', 'click', '.blogEditComment', function() {
  form = this.parentElement.parentElement
  span_form = form.parentElement;
  block = span_form.parentElement.parentElement.parentElement;
  form_comment = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('POST', "/blog/edit_blog_comment/" + this.getAttribute("data-pk") + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  if (!form.querySelector(".text-comment").value && !form.querySelector(".comment_attach_block").firstChild){
    toast_error("Напишите или прикрепите что-нибудь");
    form.querySelector(".text-comment").style.border = "1px #FF0000 solid";
    form.querySelector(".dropdown").style.border = "1px #FF0000 solid";
    return
  };
  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          crd = document.createElement("div");
          span = document.createElement("span");
          crd.classList.add("card-body");
          crd.style.paddingTop = "0.5rem";
          crd.style.paddingBottom = "0.5rem";
          crd.style.paddingLeft = "7px";
          span.append(crd);
          crd.innerHTML = new_post.querySelector(".card-body").innerHTML;
          block.innerHTML = span.innerHTML;
          toast_success(" Комментарий изменен");
      }
  };
  link_.send(form_comment)
});

function edit_comment_post(form, url) {
  span_form = form.parentElement;
  block = span_form.parentElement.parentElement.parentElement;
  form_comment = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('POST', url, true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  if (!form.querySelector(".text-comment").value && !form.querySelector(".comment_attach_block").firstChild){
    toast_error("Напишите или прикрепите что-нибудь");
    form.querySelector(".text-comment").style.border = "1px #FF0000 solid";
    form.querySelector(".dropdown").style.border = "1px #FF0000 solid";
    return
  };
  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          crd = document.createElement("div");
          span = document.createElement("span");
          crd.classList.add("card-body");
          crd.style.paddingTop = "0.5rem";
          crd.style.paddingBottom = "0.5rem";
          crd.style.paddingLeft = "7px";
          span.append(crd);
          crd.innerHTML = new_post.querySelector(".card-body").innerHTML;
          block.innerHTML = span.innerHTML;
          toast_success(" Комментарий изменен");
      }
  };
  link_.send(form_comment)
}

on('body', 'click', '.electnewEditComment', function() {
  edit_comment_post(this.parentElement.parentElement, "/blog/edit_new_comment/" + this.getAttribute("data-pk") + "/")
});

on('body', 'click', '.blogComment', function() {
  form = this.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.nextElementSibling, '/blog/blog_comment/', "prepend");
});

on('body', 'click', '.blogReplyComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling;
  send_comment(form, block, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("show");
});

on('body', 'click', '.blogReplyParentComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
});


on('body', 'click', '.electnewComment', function() {
  form = this.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.nextElementSibling, '/blog/add_new_comment/', "prepend");
});

on('body', 'click', '.electnewReplyComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling;
  send_comment(form, block, '/blog/reply_new_comment/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("show");
});

on('body', 'click', '.electnewReplyParentComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/blog/reply_new_comment/', "append")
  form.parentElement.style.display = "none";
});

on('body', 'click', '.u_load_comment_photo', function() {
  check_attach_block_message_post();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_photo_comment_load/', loader)
});
on('body', 'click', '.u_load_doc', function() {
  check_attach_block_message_post();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_doc_load/', loader)
});
on('body', 'click', '.u_load_video', function() {
  check_attach_block_message_post();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_video_load/', loader)
});
on('body', 'click', '.u_load_music', function() {
  check_attach_block_message_post();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_music_load/', loader)
});

on('body', 'change', '#u_photo_attach', function() {
  if (this.files.length > 10) {
      toast_error("Не больше 10 фотографий");return
  }
  form = this.parentElement;
  form_data = new FormData(form);

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_post_upload_attach(photo_list, document.body.querySelector(".attach_block")
    );
    }
    close_create_window();
  }
  link_.send(form_data);
});

on('body', 'change', '#u_photo_comment_attach', function() {
  if (this.files.length > 2) {
      toast_error("Не больше 2 фотографий");return
  }
  form = this.parentElement;
  form_data = new FormData(form);

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_comment_upload_attach(photo_list, document.body.querySelector(".current_file_dropdown").parentElement.parentElement
    );
    }
    close_create_window();
  }
  link_.send(form_data);
});


on('body', 'change', '#u_photo_attach', function() {
  if (this.files.length > 10) {
      toast_error("Не больше 10 фотографий");return
  }
  form = this.parentElement;
  form_data = new FormData(form);

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".pag");
    photo_post_upload_attach(photo_list, document.body.querySelector(".attach_block").parentElement.parentElement
    );
    }
    close_create_window();
  }
  link_.send(form_data);
});

on('body', 'click', '.u_select_photo', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_photo_load/', loader)
});
on('body', 'click', '.u_select_survey', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_survey_load/', loader)
});

on('body', 'click', '.u_select_video', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_video_load/', loader)
});
on('body', 'click', '.u_select_music', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_music_load/', loader)
});
on('body', 'click', '.u_select_doc', function() {
  this.parentElement.parentElement.previousElementSibling.classList.add("attach_block");
  clear_comment_dropdown();
  loader = document.getElementById("create_loader");
  open_load_fullscreen('/users/load/u_doc_load/', loader)
});
