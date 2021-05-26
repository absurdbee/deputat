function get_sanction_window(_this, url) {
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    pk = _this.parentElement.getAttribute("data-pk");
    list = document.querySelectorAll('.pag');
    for (var i = 0; i < list.length; i++) {
      list[i].classList.remove("changed");
    }
    div.classList.add("changed")
  }
  else if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk")
  }
  loader = document.getElementById("window_loader");
  open_fullscreen(url + pk + "/", loader)
}
function send_sanction(_this, form, url, old_class, new_class, toast) {
  form_data = new FormData(form);
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk")
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("user-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аккаунт заблокирован!");
    document.querySelector(".window_fullscreen").style.display = "none";
    document.getElementById("window_loader").innerHTML="";
    if (document.body.querySelector(".pk_saver")) {
      _this.innerHTML = "Отменить";
      _this.classList.replace(old_class, new_class)
    }else if (li.classList.contains("changed")){
      li.remove();
    }
  }};

  link_.send(form_data);
}

on('body', 'click', '.create_user_close', function() {
  get_sanction_window(this, "/managers/progs_user/create_close/")
})
on('body', 'click', '.create_user_warning_banner', function() {
  get_sanction_window(this, "/managers/progs_user/create_warning_banner/")
})
on('body', 'click', '.create_user_suspend', function() {
  get_sanction_window(this, "/managers/progs_user/create_suspension/")
})

on('body', 'click', '.create_user_blocker_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_sanction(this, parent, "/managers/progs_user/create_close/", "create_user_close", "remove_user_close", "Аккаунт блокирован")
});
on('body', 'click', '.create_user_warning_banner_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_sanction(this, parent, "/managers/progs_user/create_warning_banner/", "create_user_warning_banner", "remove_user_warning_banner", "Баннер применен")
});
on('body', 'click', '.create_user_suspend_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_sanction(this, parent, "/managers/progs_user/create_suspension/", "create_user_suspend", "remove_user_suspend", "Аккаунт заморожен")
});

on('body', 'click', '.user_unverify', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("user-pk");
  obj_pk = item.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/unverify/" + user_pk + "/" + obj_pk + "/", true );
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
  user_pk = this.parentElement.getAttribute("user-pk");
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
