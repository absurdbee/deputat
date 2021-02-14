on('#ajax', 'click', '#holder_image', function() {
  img = this.previousElementSibling.querySelector("input")
  get_image_priview(this, img);
});

on('#ajax', 'click', '#edit_user_info_btn', function() {
  form = document.body.querySelector("#edit_user_info_form");
  field1 = form.querySelector("#id_first_name");
  field2 = form.querySelector("#id_last_name");
  field3 = form.querySelector("#id_email");
  if (!field1.value){
    field1.style.border = "1px #FF0000 solid";
    toast_error("Введите Ваше имя!"); return
  } else if (!field2.value){
    field2.style.border = "1px #FF0000 solid";
    toast_error("Введите Вашу фамилию!"); return
  };
  send_form_and_toast('/users/edit/', form, "Изменения приняты!");
  field1.value = ""; field2.value = ""; field1.style.border = "1px #D8D6DE solid";field2.style.border = "1px #D8D6DE solid";
});

on('#ajax', 'click', '#edit_user_password_btn', function() {
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
