
on('body', 'click', '#register_ajax', function() {
  form = document.querySelector("#signup");
  if (!form.querySelector("#id_first_name").value){
    form.querySelector("#id_first_name").style.border = "1px #FF0000 solid";
    toast_error("Имя - обязательное поле!");
  } else if (!form.querySelector("#id_last_name").value){
    form.querySelector("#id_last_name").style.border = "1px #FF0000 solid";
    toast_error("Фамилия - обязательное поле!")
  } else if (!form.querySelector("#password1").value){
    form.querySelector("#password1").style.border = "1px #FF0000 solid";
    toast_error("Пароль - обязательное поле!")
  }else if (!form.querySelector("#password2").value){
    form.querySelector("#password2").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль еще раз!")
  }
  form_data = new FormData(form);
  reg_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  reg_link.open( 'POST', "/rest-auth/registration/", true );
  reg_link.onreadystatechange = function () {
  if ( reg_link.readyState == 4 && reg_link.status == 201 ) {
    window.location.href = "/users/phone_verify/"
    }};
  reg_link.send(form_data);
})
on('body', 'click', '#logg', function() {
  form = document.querySelector("#login_form");
  user_pk = form.getAttribute("data-pk");
  if (!form.querySelector("#id_username").value){
    form.querySelector("#id_username").style.border = "1px #FF0000 solid";
    toast_error("Введите телефон!")}
  else if (!form.querySelector("#id_password").value){
    form.querySelector("#id_password").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль!")}
  else {this.disabled = true}
  if (form.querySelector("#id_username").value){form.querySelector("#id_username").style.border = "rgba(0, 0, 0, 0.2)";}
  if (form.querySelector("#id_password").value){form.querySelector("#id_password").style.border = "rgba(0, 0, 0, 0.2)";}

  form_data = new FormData(form);
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/rest-auth/login/", true );

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    window.location.href = "/"
    }};
  link.send(form_data);
});

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url)
  } else {toast_info("Вы уже на этой странице")}
})

function phone_check() {
 if (document.getElementById('phone').value.length > 10)
   document.getElementById("phone_send").removeAttribute('disabled');
 else
   document.getElementById("phone_send").setAttribute("disabled", "true");
 }
 function code_check() {
  if (document.getElementById('code').value.length === 4)
    document.getElementById("code_send").removeAttribute('disabled');
  else
    document.getElementById("code_send").setAttribute("disabled", "true");
  }

  on('#ajax', 'click', '#code_send', function() {
      form = document.querySelector('.verify_form');
      user_pk = form.getAttribute("data-pk");
      var phone = form.querySelector('#phone').value;
      var code = document.body.querySelector('.block_verify').querySelector('#code').value;
      var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
      request.open('GET', "/users/progs/phone_verify/" + phone + "/" + code + "/", true);
      request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      request.onreadystatechange = function() {
          if (request.readyState == 4 && request.status == 200) {
              var div = document.getElementById('jsondata2');
              div.innerHTML = request.responseText;
              console.log(request.responseText);
              if (request.responseText.indexOf("ok") != -1) {
                 window.location.href = "/users/" + user_pk + "/"
              }
          }
      };
      request.send(null)
  });
