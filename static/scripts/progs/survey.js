on('body', 'click', '.u_survey_list_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/survey/user_progs/add_list/", loader)
});
on('body', 'click', '.u_survey_add', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/survey/user_progs/create_survey/", loader)
});
on('body', 'click', '.u_survey_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_survey")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_survey")
  loader = document.getElementById("create_loader");
  open_fullscreen("/survey/user_progs/edit_survey/" + parent.getAttribute("data-pk") +"/", loader)
});
on('body', 'click', '.u_survey_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.getElementById("create_loader");
  open_fullscreen("/survey/user_progs/edit_list/" + uuid + "/", loader)
});

on('body', 'click', '.u_survey_list_remove', function() {
  media_list_delete(this, "/survey/user_progs/delete_list/", "u_survey_list_remove", "u_survey_list_abort_remove")
});
on('body', 'click', '.u_survey_list_abort_remove', function() {
  media_list_recover(this, "/survey/user_progs/abort_delete_list/", "u_survey_list_abort_remove", "u_survey_list_remove")
});

on('body', 'click', '.u_copy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/user_progs/add_list_in_collections/", "u_uncopy_survey_list", "u_copy_survey_list", "Удалить")
});
on('body', 'click', '.u_uncopy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/user_progs/remove_list_from_collections/", "u_copy_survey_list", "u_uncopy_survey_list", "Добавить")
});

on('body', 'click', '#u_create_survey_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/survey/user_progs/add_list/", "/survey/user_list/", "/");
});


on('body', 'click', '#u_edit_survey_list_btn', function() {
  media_list_edit(this, "/survey/user_progs/edit_list/")
});

on('body', 'click', '.u_add_survey_in_list', function() {
  add_item_in_list(this, '/survey/user_progs/add_survey_in_list/', 'u_add_survey_in_list', 'u_remove_survey_from_list')
})
on('body', 'click', '.u_remove_survey_from_list', function() {
  remove_item_from_list(this, '/survey/user_progs/remove_survey_from_list/', 'u_remove_survey_from_list', 'u_add_survey_in_list', ".u_survey_remove")
})

on('body', 'click', '#u_create_survey_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!")
  } else { _this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/survey/user_progs/create_survey/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    document.body.querySelector(".pk_saver").getAttribute("data-uuid") ? (
      uuid = document.body.querySelector(".pk_saver").getAttribute("data-uuid"),
      check_span1(response.querySelector('.span1'), uuid, response.innerHTML),
      document.body.querySelector(".item_empty") ? document.body.querySelector(".item_empty").style.display = "none" : null) : get_preview(response, "survey");
    toast_info("Опрос создан!")
    close_create_window();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_survey_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
  form_data = new FormData(form);

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!")
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!")
  }
  else if (!form.querySelector("#id_file").value){
    form.querySelector("#id_file").style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!")
  } else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/survey/user_progs/edit_survey/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Документ изменен!")
    close_create_window();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    doc = document.body.querySelector(".edited_survey");
    doc.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_survey_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/survey/user_progs/remove_survey/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Опрос удален. <span class='u_survey_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_survey_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/survey/user_progs/abort_remove_survey/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('body', 'click', '.u_load_survey_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("surveylist-pk");
  loader = document.getElementById("window_loader");
  open_fullscreen("/survey/user_load/" + pk + "/", loader)
});

on('body', 'click', '.u_load_profile_survey_list', function() {
  profile_list_block_load(this, ".load_block", "/survey/user_list/" + this.getAttribute("data-uuid") + "/", "u_load_profile_survey_list");
});

on('body', 'click', '.u_load_attach_survey_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_survey_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_attach_survey_list");
});
