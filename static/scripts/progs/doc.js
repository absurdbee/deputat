on('body', 'click', '.u_doc_list_add', function() {
  loader = document.body.querySelector("#create_loader");
  open_fullscreen("/docs/user_progs/add_list/", loader)
});
on('body', 'click', '.u_doc_add', function() {
  loader = document.body.querySelector("#create_loader");
  open_fullscreen("/docs/user_progs/create_doc/", loader)
});
on('body', 'click', '.u_doc_edit', function() {
  parent = this.parentElement.parentElement.parentElement;
  blocks = document.body.querySelectorAll('.col-sm-12');
  for (var i = 0; i < blocks.length; i++) {blocks[i].classList.remove("edited_doc")}

  parent.parentElement.parentElement.parentElement.classList.add("edited_doc")
  loader = document.body.querySelector("#create_loader");
  open_fullscreen("/docs/user_progs/edit_doc/" + parent.getAttribute("data-pk") +"/", loader)
});
on('body', 'click', '.u_doc_list_edit', function() {
  list = document.body.querySelectorAll('.cover_block');
  for (var i = 0; i < list.length; i++) {
    list[i].classList.remove("list_active")
  }
  block = this.parentElement.parentElement;
  block.classList.add("list_active");
  uuid = block.getAttribute('data-uuid');
  loader = document.body.querySelector("#create_loader");
  open_fullscreen("/docs/user_progs/edit_list/" + uuid + "/", loader)
});

on('body', 'click', '.u_doc_list_remove', function() {
  media_list_delete(this, "/docs/user_progs/delete_list/", "u_doc_list_remove", "u_doc_list_abort_remove")
});
on('body', 'click', '.u_doc_list_abort_remove', function() {
  media_list_recover(this, "/docs/user_progs/abort_delete_list/", "u_doc_list_abort_remove", "u_doc_list_remove")
});

on('body', 'click', '.u_copy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/user_progs/add_list_in_collections/", "u_uncopy_doc_list", "u_copy_doc_list", "Удалить")
});
on('body', 'click', '.u_uncopy_doc_list', function() {
  on_off_list_in_collections(this, "/docs/user_progs/remove_list_from_collections/", "u_copy_doc_list", "u_uncopy_doc_list", "Добавить")
});

on('body', 'click', '#u_create_doc_list_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { this.disabled = true }
  post_and_load_object_page(form, "/docs/user_progs/add_list/", "/docs/user_list/");
});

on('body', 'click', '#u_edit_doc_list_btn', function() {
  media_list_edit(this, "/docs/user_progs/edit_list/")
});
on('body', 'click', '.u_add_doc_in_list', function() {
  add_item_in_list(this, '/docs/user_progs/add_doc_in_list/', 'u_add_doc_in_list', 'u_remove_doc_from_list')
})
on('body', 'click', '.u_remove_doc_from_list', function() {
  remove_item_from_list(this, '/docs/user_progs/remove_doc_from_list/', 'u_remove_doc_from_list', 'u_add_doc_in_list', ".u_doc_remove")
})

on('body', 'click', '#u_create_doc_btn', function() {
  _this = this;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");
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
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!")
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    input_file.style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "pdf" && format != "doc" && format != "docx") {
    toast_error("Допустим формат файла pdf, doc, docx!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/create_doc/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    get_preview(response, "doc");
    toast_info("Документ создан!")
    close_create_window();
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_edit_doc_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  try {format = form.querySelector("#id_file").files[0].name.split(".").splice(-1,1)[0]} catch { format = null };
  input_file = form.querySelector("#id_file");

  lists = form.querySelector("#id_list");
  selectedOptions = lists.selectedOptions;
  val = false;
  for (var i = 0; i < selectedOptions.length; i++) {
    if(selectedOptions[i].value) {val = true}
  }

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!val){
    form.querySelector("#id_list").style.border = "1px #FF0000 solid";
    toast_error("Выберите список!"); return
  }
  else if (!format){
    input_file.style.border = "1px #FF0000 solid";
    toast_error("Загрузите документ!"); return
  }
  else if (findSize(input_file)> 5242880) {
    toast_error("Файл не должен превышать 5 Мб!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else if (format != "pdf" && format != "doc" && format != "docx") {
    toast_error("Допустим формат файла pdf, doc, docx!"),
    form.querySelector(".form_file").style.color = "red";
    _this.disabled = false;
    return
  }
  else { this.disabled = true }

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/docs/user_progs/edit_doc/" + form.getAttribute("data-pk") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Документ изменен!")
    close_create_window();
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    doc = document.body.querySelector(".edited_doc");
    doc.innerHTML = response.querySelector(".pag").innerHTML;
  }};

  link_.send(form_data);
});

on('body', 'click', '.u_doc_remove', function() {
  saver = this.parentElement.parentElement.parentElement;
  pk = saver.getAttribute("data-pk")
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    div = document.createElement("div");
    div.classList.add("col-md-6", "col-sm-12");
    div.style.padding = "20px";
    div.style.display =  "block";
    div.innerHTML = "Запись удалена. <span class='u_doc_abort_remove pointer underline' data-pk='" + pk + "'>Восстановить</span>";
    item = saver.parentElement.parentElement.parentElement;
    item.style.display = "none"; item.parentElement.insertBefore(div, item)
  }};
  link.send( );
});
on('body', 'click', '.u_doc_abort_remove', function() {
  pk = this.getAttribute("data-pk");
  block = this.parentElement; next = block.nextElementSibling;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/docs/user_progs/abort_remove_doc/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    next.style.display = "block";
  }};
  link.send();
});

on('body', 'click', '.u_load_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("doclist-pk");
  loader = document.body.querySelector("#window_loader_2");
  open_fullscreen("/docs/user_load/" + pk + "/", loader)
});

on('body', 'click', '.u_load_profile_doc_list', function() {
  profile_list_block_load(this, ".load_block", "/docs/user_list/" + this.getAttribute("data-uuid") + "/", "u_load_profile_doc_list");
});

on('body', 'click', '.u_load_attach_doc_list', function() {
  profile_list_block_load(this, ".load_block", "/users/load/u_doc_list_load/" + this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", "u_load_attach_doc_list");
});
