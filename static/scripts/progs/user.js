on('body', 'click', '#holder_image', function() {
  img = this.previousElementSibling.querySelector("input")
  get_image_priview(this, img);
});

on('body', 'click', '#edit_user_profile_btn', function() {
  form = this.parentElement.parentElement;
  if (!form.querySelector("#id_first_name").value){
    form.querySelector("#id_first_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Ваше имя!"); return
  } else if (!form.querySelector("#id_last_name").value){
    form.querySelector("#id_last_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Вашу фамилию!"); return
  };
  send_form_and_toast('/users/settings/', form, "Изменения приняты!");
  form.querySelector("#id_first_name").style.border = "1px #D8D6DE solid";
  form.querySelector("#id_last_name").style.border = "1px #D8D6DE solid";
});

on('body', 'click', '#edit_user_about_btn', function() {
  send_form_and_toast('/users/settings/about/', this.parentElement.parentElement, "Изменения приняты!");
})
on('body', 'click', '#edit_user_notify_btn', function() {
  send_form_and_toast('/users/settings/notify/', this.parentElement.parentElement, "Изменения приняты!");
})
on('body', 'click', '#edit_user_private_btn', function() {
  send_form_and_toast('/users/settings/private/', this.parentElement.parentElement, "Изменения приняты!");
})

on('body', 'click', '#edit_user_password_btn', function() {
  form = document.body.querySelector("#edit_user_password_form")
  field1 = form.querySelector("#password1"); field2 = form.querySelector("#password2");
  if (!field1.value){
    field1.style.border = "1px #FF0000 solid";
    toast_error("Введите новый пароль!"); return
  } else if (!field2.value){
    field2.style.border = "1px #FF0000 solid";
    toast_error("Повторите новый пароль!"); return
  } else if (field1.value != field2.value){
    field2.value = '';
    toast_error("Пароли не совпадают!"); return
  };
  send_form_and_toast('/rest-auth/password/change/', form, "Изменения приняты!");
  field1.value = ""; field2.value = ""; field1.style.border = "1px #D8D6DE solid";field2.style.border = "1px #D8D6DE solid";
});

on('body', 'click', '.remove_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk"); name = _this.getAttribute("data-name")

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.classList.add("add_elect_subscribe", "btn-primary"); _this.classList.remove("remove_elect_subscribe");
          _this.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart align-middle mr-25"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg><span class="text-truncate">Подписаться</span>'
          toast_info(name + " удален из подписок!");
        }
    }
};
link.send( null );
})

on('body', 'click', '.add_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk"); name = _this.getAttribute("data-name")

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/subscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.classList.add("remove_elect_subscribe"); _this.classList.remove("add_elect_subscribe", "btn-primary");
          _this.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x align-middle mr-25"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg><span class="text-truncate">Вы подписаны</span>'
          toast_info(name + " возвращен в подписки!");
        }
    }
};
link.send( null );
})


on('body', 'click', '.photo_claim', function() {
  open_fullscreen("/managers/progs_photo/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_photo_list_claim', function() {
  open_fullscreen("/managers/progs_photo/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_video_claim', function() {
  open_fullscreen("/managers/progs_video/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_video_list_claim', function() {
  open_fullscreen("/managers/progs_video/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_doc_list_claim', function() {
  open_fullscreen("/managers/progs_doc/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.doc_claim', function() {
  open_fullscreen("/managers/progs_doc/create_claim/" + this.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_playlist_claim', function() {
  open_fullscreen("/managers/progs_audio/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.track_claim', function() {
  open_fullscreen("/managers/progs_audio/create_claim/" + this.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
on('body', 'click', '.u_survey_list_claim', function() {
  open_fullscreen("/managers/progs_survey/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("window_loader"))
});
