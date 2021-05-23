

on('body', 'click', '.u_suggested_elect_new_create', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/blog/progs/suggest_elect_new/", loader)
});

on('body', 'click', '#u_create_suggested_new_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!")
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/suggest_elect_new/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость предложена!")
    close_create_window();
  }};

  link_.send(form_data);
});
