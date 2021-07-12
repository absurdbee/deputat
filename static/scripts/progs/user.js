on('body', 'click', '#holder_image', function() {
  img = this.previousElementSibling.querySelector("input")
  get_image_priview(this, img);
});

on('body', 'click', '.copy_link', function() {
  url = this.getAttribute("data-link");
  aux = document.createElement("input");
  aux.setAttribute("value", window.location.host + url);
  document.body.appendChild(aux);
  aux.select();
  document.execCommand("copy");
  document.body.removeChild(aux);
  toast_info("Ссылка скопирована")
});

on('body', 'click', '.u_edit_password', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/users/settings/edit_password/", loader)
});
on('body', 'click', '.edit_user_phone', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/users/settings/edit_phone/", loader)
});
on('body', 'click', '.deputat_verified_send', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/users/settings/deputat_send/", loader)
});
on('body', 'click', '.create_secret_user_key', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen("/users/settings/create_secret_key/", loader)
});

on('body', 'click', '#edit_user_profile_btn', function() {
  form = this.parentElement.parentElement;
  if (!form.querySelector("#id_first_name").value){
    form.querySelector("#id_first_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Ваше имя!"); return
  } else if (!form.querySelector("#id_last_name").value){
    form.querySelector("#id_last_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Вашу фамилию!"); return
  } else if (form.querySelector("#id_email").value && !validateEmail(form.querySelector("#id_email").value)){
    form.querySelector("#id_email").style.border = "1px #FF0000 solid";
    toast_error("Введите правильный email!"); return
  };
  send_form_and_toast('/users/settings/', form, "Изменения приняты!");
  form.querySelector("#id_first_name").style.border = "1px #D8D6DE solid";
  form.querySelector("#id_last_name").style.border = "1px #D8D6DE solid";
  form.querySelector("#id_email").style.border = "1px #D8D6DE solid";
});

on('#ajax', 'click', '#u_edit_password_btn', function() {
  form = this.parentElement.parentElement.parentElement;
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
  send_form_and_toast('/rest-auth/password/change/', form, "Пароль изменён!")
  close_create_window();
});

on('#ajax', 'click', '#u_edit_password_btn', function() {
  form = this.parentElement.parentElement.parentElement;
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
  send_form_and_toast('/rest-auth/password/change/', form, "Пароль изменён!")
  close_create_window();
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

on('body', 'click', '.remove_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk"); name = _this.getAttribute("data-name")

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.classList.add("add_elect_subscribe"); _this.classList.remove("remove_elect_subscribe");
          _this.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart align-middle mr-25"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg><span class="text-truncate">Подписаться</span>'
          toast_info(name + " удален из подписок");
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
          toast_info("Подписка оформлена");
        }
    }
};
link.send( null );
})

on('body', 'click', '.claim_blog', function() {
  open_fullscreen("/managers/progs_blog/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.claim_blog_comment', function() {
  open_fullscreen("/managers/progs_blog/comment_create_claim/" + this.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.claim_elect_new', function() {
  open_fullscreen("/managers/elect_new/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.claim_elect_new_comment', function() {
  open_fullscreen("/managers/elect_new/comment_create_claim/" + this.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.photo_claim', function() {
  open_fullscreen("/managers/progs_photo/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_photo_list_claim', function() {
  open_fullscreen("/managers/progs_photo/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_video_claim', function() {
  open_fullscreen("/managers/progs_video/create_claim/" + this.parentElement.parentElement.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_video_list_claim', function() {
  open_fullscreen("/managers/progs_video/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_doc_list_claim', function() {
  open_fullscreen("/managers/progs_doc/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.doc_claim', function() {
  open_fullscreen("/managers/progs_doc/create_claim/" + this.parentElement.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_playlist_claim', function() {
  open_fullscreen("/managers/progs_audio/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.track_claim', function() {
  open_fullscreen("/managers/progs_audio/create_claim/" + this.parentElement.parentElement.parentElement.getAttribute('data-pk') + "/", document.getElementById("create_loader"))
});
on('body', 'click', '.u_survey_list_claim', function() {
  open_fullscreen("/managers/progs_survey/list_create_claim/" + this.parentElement.parentElement.getAttribute('data-uuid') + "/", document.getElementById("create_loader"))
});

on('body', 'click', '.create_blog_comment_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_blog/comment_create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_elect_new_comment_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/elect_new/comment_create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_blog_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_blog/create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_elect_new_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/elect_new/create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_audio_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_audio/create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_playlist_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_audio/list_create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_doc_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_doc/create_claim/" + this.getAttribute('data-pk') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_doc_list_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_doc/list_create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_video_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_video/create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_video_list_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_video/list_create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_photo_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_photo/create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_photo_list_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_photo/list_create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_survey_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_survey/create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});
on('body', 'click', '.create_survey_list_claim_btn', function() {
  send_form_and_toast_and_close_window("/managers/progs_survey/list_create_claim/" + this.getAttribute('data-uuid') + "/", this.parentElement.parentElement.parentElement)
});


on('body', 'click', '#change_code_send', function() {
    form = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    form_data = new FormData(form);
    user_pk = form.getAttribute("data-pk");
    var phone = form.querySelector('#phone').value;
    var code = document.body.querySelector('.block_verify').querySelector('#code').value;
    var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    request.open('POST', "/users/progs/change_phone_verify/" + phone + "/" + code + "/", true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {
          close_create_window();
          toast_info("Телефон изменён")
        }
    };
    request.send(form_data)
});

on('body', 'click', '.change_phone_send', function() {
  form = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
var phone = document.querySelector('#phone').value;
 var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
 request.open( 'POST', "/users/progs/change_phone_send/" + phone + "/", true );
 request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
 request.onreadystatechange = function () {
   if ( request.readyState == 4 && request.status == 200) {
     var div = document.getElementById('jsondata');
     div.innerHTML = request.responseText;
     if (request.responseText.indexOf("уже зарегистрирован") !== -1) {
       div.innerHTML = 'Пользователь с таким номером уже зарегистрирован. Используйте другой номер или напишите в <a class="pointer underline send_support_message">Службу поддержки</a>, если этот номер Вы не использовали ранее.'
       document.querySelector(".change_phone_send").setAttribute("disabled", "true");
     } else if (request.responseText.indexOf("Мы Вам звоним") !== -1){
       div.innerHTML = request.responseText;
     document.querySelector("#phone").setAttribute("disabled", "true");
     document.querySelector(".change_phone_send").setAttribute("disabled", "true");
   }}}
 request.send(form_data);
})
