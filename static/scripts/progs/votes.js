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
  item = this.parentElementюparentElement;
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
