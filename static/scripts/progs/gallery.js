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
    $block.classList.add("card", "delete_card", "rounded-0", "border-0", "mb-3");
    $block.innerHTML = '<div class="card-header"><div class="media"><div class="media-body"><h6 class="mb-0 u_album_abort_remove pointer">Восстановить</h6></div></div></div><div class="card-body"><a><img class="image_fit_200" src="/static/images/no_img/album.jpg" /></a></div>'
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
