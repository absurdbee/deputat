on('body', 'click', '.create_user_close', function() {
  _this = this;
  if(_this.parentElement.classList.contains("btn_console")){
    div = _this.parentElement.parentElement.parentElement.parentElement;
    uuid = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid");
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
  open_fullscreen("/managers/progs_user/create_close/" + pk + "/", loader)
})

on('#ajax', 'click', '.create_user_blocker_btn', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement;
  form_data = new FormData(parent);
  if (document.body.querySelector(".pk_saver")){
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk")
  }else if (document.body.querySelector(".changed")){
    li = document.body.querySelector(".changed");
    pk = li.getAttribute("data-pk");
  }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_user/create_create/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Аккаунт заблокирован!");
    document.querySelector(".window_fullscreen").style.display = "none";
    document.getElementById("worker_loader").innerHTML="";
    if (document.body.querySelector(".pk_saver")) {
      a = document.body.querySelector(".create_user_close");
      a.innerHTML = "Отменить блокировку";
      a.classList.replace("create_user_close", "remove_user_close")
    }else if (li.querySelector(".btn_console")){
      li.remove();
    }
  }};

  link_.send(form_data);
});
