function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

function ajax_get_reload(url) {
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        window.history.pushState({route: url}, "network", url);
        get_select()
      }
    }
    ajax_link.send();
}

on('body', 'click', '#register_ajax', function() {
  if (!document.body.querySelector(".first_name").value){
    document.body.querySelector(".first_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Ваше имя!");
  } else if (!document.body.querySelector(".last_name").value){
    document.body.querySelector(".last_name").style.border = "1px #FF0000 solid";
    toast_error("Введите Вашу фамилию!");
  } else if (!document.body.querySelector(".password1").value){
    document.body.querySelector(".password1").style.border = "1px #FF0000 solid";
    toast_error("Придумайте пароль!")
  } else if (!document.body.querySelector(".password2").value){
    document.body.querySelector(".password2").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль еще раз!")
  }
  form_data = new FormData(document.querySelector("#signup"));
  reg_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  reg_link.open( 'POST', "/rest-auth/registration/", true );
  reg_link.onreadystatechange = function () {
  if ( reg_link.readyState == 4 && reg_link.status == 201 ) {
    if (window.location.href == "89072373637.рус/auth/"){window.location.href = "/profile/user_news/";}
    else {window.location.href=window.location.href}
    }else {document.body.querySelector(".signup_response").innerHTML = link.responseText}};
  reg_link.send(form_data);
})

on('body', 'click', '#logg', function() {
  if (!document.body.querySelector(".l_username").value){
    document.body.querySelector(".l_username").style.border = "1px #FF0000 solid";
    toast_error("Введите телефон!")}
  else if (!document.body.querySelector(".l_password").value){
    document.body.querySelector(".l_password").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль!")}
  if (document.body.querySelector(".l_username").value){document.body.querySelector(".l_username").style.border = "rgba(0, 0, 0, 0.2)";}
  if (document.body.querySelector(".l_password").value){document.body.querySelector(".l_password").style.border = "rgba(0, 0, 0, 0.2)";}

  form_data = new FormData(document.querySelector("#login_form"));
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/rest-auth/login/", true );
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    if (window.location.href == "89072373637.рус/auth/"){window.location.href = "/profile/user_news/";}
    else {window.location.href=window.location.href}
  } else {document.body.querySelector(".login_response").innerHTML = link.responseText} };
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
 if (document.getElementById('phone').value.length > 9)
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
      var phone = document.getElementById('phone').value;
      var code = document.getElementById('code').value;
      var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
      request.open('GET', "/users/progs/phone_verify/" + phone + "/" + code + "/", true);
      request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      request.onreadystatechange = function() {
          if (request.readyState == 4 && request.status == 200) {
              var div = document.getElementById('jsondata2');
              div.innerHTML = request.responseText;
              console.log(request.responseText);
              if (request.responseText.indexOf("ok") != -1) {
                  window.location.href = "{% url 'user' pk=request.user.pk %}";
              }
          }
      };
      request.send(null)
  });
