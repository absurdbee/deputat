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
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/elect_new_like/" + pk + "/");
});
on('body', 'click', '.elect_new_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/elect_new_dislike/" + pk + "/");
});
on('body', 'click', '.elect_new_comment_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/elect_new_comment_like/" + pk + "/");
});
on('body', 'click', '.elect_new_comment_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/elect_new_comment_dislike/" + pk + "/");
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

on('body', 'click', '.blog_comment_like', function() {
  item = this.parentElement.parentElement;
  like = item.querySelector(".like");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', "/blog/votes/blog_comment_like/" + item.getAttribute("data-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    like.classList.toggle("btn_success");
  }};
  link.send( null );
});


on('#ajax', 'click', '.blogComment', function() {
  form = this.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.nextElementSibling, '/blog/blog_comment/', "prepend");
});

on('#ajax', 'click', '.blogReplyComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling;
  send_comment(form, block, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("show");
});

on('#ajax', 'click', '.blogReplyParentComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.u_load_comment_photo', function() {
  check_attach_block_message_post();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_img_comment_load/', loader)
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
