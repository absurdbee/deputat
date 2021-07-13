on('body', 'click', '.u_suggested_elect_new_create', function() {
  loader = document.getElementById("window_loader");
  this.getAttribute("data-name") ? name = this.getAttribute("data-name") : name = "";
  open_elect_fullscreen("/blog/progs/suggest_elect_new/", loader, name)
});

on('body', 'click', '.elect_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/elect/votes/like/" + pk + "/");
});
on('body', 'click', '.elect_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/elect/votes/dislike/" + pk + "/");
});
on('body', 'click', '.elect_inert', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_inert(item, "/elect/votes/inert/" + pk + "/");
});

on('body', 'click', '#u_create_suggested_new_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  elect_value = form.querySelector("#id_elect").value;
  form_data = new FormData(form);

  xxx = form.querySelector("#data-list");
  elect_list = xxx.querySelectorAll("option");
  console.log(elect_list.length);
  for (var i = 0; i < elect_list.length; i++){
    console.log(elect_list[i]);
    console.log(elect_list[i].value);
    console.log(elect_list[i].getAttribute("value"));
    if (elect_value == elect_list[i].getAttribute("value")) {
      elect = true; console.log("Депутат корректный"); console.log(elect_list[i].getAttribute("value"))
    }
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  } else if (!elect_value){
    form.querySelector("#id_elect").style.border = "1px #FF0000 solid";
    toast_error("Выберите чиновника!"); return
  } else if (!elect){
    form.querySelector("#id_elect").style.border = "1px #FF0000 solid";
    toast_error("Выберите чиновника из списка!"); return
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/suggest_elect_new/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость предложена!")
    document.getElementById("window_loader").innerHTML = '<div class="card card-congratulations mt-4"><div class="card-body text-center"><img src="/static/images/left.png" class="congratulations-img-left" alt="card-img-left"><img src="/static/images/right.png" class="congratulations-img-right" alt="card-img-right"><div class="avatar avatar-xl bg-primary shadow"><div class="avatar-content"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-award font-large-1"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg></div></div><div class="text-center"><h2 class="mb-1 text-white">Благодарим, новость создана!</h2><p class="card-text m-auto w-75">Новость будет опубликована после проверки модераторами.</p><h4 class="card-text m-auto w-75 create_fullscreen_hide_2 underline text-white pt-2 pointer">Понятно</h4></div></div></div>';
  }};

  link_.send(form_data);
});
