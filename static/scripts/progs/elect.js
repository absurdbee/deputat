on('body', 'click', '.u_suggested_elect_new_create', function() {
  loader = document.body.querySelector("#window_loader");
  if (this.getAttribute("data-name")) {
    create_elect_fullscreen("/blog/progs/suggest_elect_new/", this.getAttribute("data-name"))
  } else {
    create_fullscreen("/blog/progs/suggest_elect_new/", "window_fullscreen");
  }
});

on('body', 'click', '.elect_new_window', function() {
  document.body.querySelector(".notify_dropdown") ? document.body.querySelector(".notify_dropdown").classList.remove("show") : null;
  create_fullscreen("/elect/new_window/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "window_fullscreen");
});
on('body', 'click', '.elect_new_window_comment', function() {
  loader = document.body.querySelector("#window_loader");
  document.body.querySelector(".notify_dropdown") ? document.body.querySelector(".notify_dropdown").classList.remove("show") : null;
  create_fullscreen("/elect/new_window/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk") + "/", "window_fullscreen")
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
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  };
  try{
  if (!form.querySelector("#id_elect").value){
    form.querySelector("#id_elect").style.border = "1px #FF0000 solid"
    toast_error("Выберите чиновника!");
    return
  }}catch {
    toast_error("Нужно выбрать чиновника!");
    form.querySelector(".search_elect_field").style.border = "1px #FF0000 solid"
    return}
  _this.disabled = true;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/suggest_elect_new/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость предложена!")

    form.parentElement.innerHTML = '<div class="card card-congratulations mt-4"><div class="card-body text-center"><img src="/static/images/left.png" class="congratulations-img-left" alt="card-img-left"><img src="/static/images/right.png" class="congratulations-img-right" alt="card-img-right"><div class="avatar avatar-xl bg-primary shadow"><div class="avatar-content"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-award font-large-1"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg></div></div><div class="text-center"><h2 class="mb-1 text-white">Благодарим, новость создана!</h2><p class="card-text m-auto w-75">Новость будет опубликована после проверки модераторами.</p><h4 class="card-text m-auto w-75 this_mob_fullscreen_hide underline text-white pt-2 pointer">Понятно</h4></div></div></div>';
  }};

  link_.send(form_data);
});

on('body', 'click', '#load_senat', function() {
  _this = this
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/elect/load_senat_elects/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    _this.parentElement.parentElement.parentElement.nextElementSibling.innerHTML = response.innerHTML;
    _this.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling.innerHTML = "";
    _this.parentElement.parentElement.parentElement.style.border = "none"
  }}
  link_.send();
});
on('body', 'click', '.load_regions_for_load_elects', function() {
  _this = this;
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/region/load_region_for_select_regional_elects/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;

    parent = _this.parentElement.parentElement.parentElement;

    parent.setAttribute("data-slug", "");

    if (_this.classList.contains("state_duma")) {
      parent.setAttribute("data-slug", "state_duma")
    } else if (_this.classList.contains("candidate_duma")) {
      parent.setAttribute("data-slug", "candidate_duma")
    } else if (_this.classList.contains("candidate_municipal")) {
      parent.setAttribute("data-slug", "candidate_municipal")
    };
    parent.nextElementSibling.innerHTML = response.innerHTML;
    parent.style.border = "none"
  }}
  link_.send();
});

on('body', 'change', '.select_region_for_load_elects', function() {
  _this = this;
  block = _this.parentElement.nextElementSibling;
  if (_this.value == '') {block.innerHTML = ""}
  else {
    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/elect/load_regional_elects/" + _this.value + "/" + _this.parentElement.previousElementSibling.getAttribute("data-slug") + "/", true );
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function () {
      if ( link.readyState == 4 ) {
          if ( link.status == 200 ) {
              block.innerHTML = link.responseText;
          }
      }
  };
  link.send( null );
  };
});


on('body', 'change', '.elect_rating_select', function() {
  this.parentElement.parentElement.parentElement.parentElement.nextElementSibling.style.display = "block"
});

on('body', 'click', '.get_elect_rating_voted', function() {
  _this = this;
  form = _this.parentElement;
  form_data = new FormData(form);
  pk = _this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/elect/votes/send_rating/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    toast_info("Голос учтён!");
    ajax_get_reload("/elect/" + pk + "/")
  }};

  link_.send(form_data);
});

on('body', 'click', '.remove_elect_rating_voted', function() {
  _this = this;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/elect/votes/delete_rating/" + _this.getAttribute("data-pk") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    toast_info("Голос сброшен!");
    ajax_get_reload("/elect/" + _this.getAttribute("data-pk") + "/")
  }};

  link_.send();
});

on('body', 'click', '.accept_elect_for_add_elect_new', function() {
  block = this.parentElement.parentElement;
  elect = this.parentElement;
  this.classList.remove("accept_elect_for_add_elect_new", "pointer");
  block.innerHTML = "<label>Чиновник</label>" + this.parentElement.innerHTML;
  field = block.previousElementSibling.querySelector(".search_elect_field");
  field.value = "";
  $input = document.createElement("input");
  $input.setAttribute("value", this.getAttribute("data-pk"));
  $input.setAttribute("type", "hidden");
  $input.setAttribute("name", "elect");
  $input.setAttribute("id", "id_elect");
  block.append($input)
});
