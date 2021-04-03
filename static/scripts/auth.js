function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};
class ToastManager {
  constructor(){
    this.id = 0;
    this.toasts = [];
    this.icons = {
      'SUCCESS': "",
      'ERROR': '',
      'INFO': '',
      'WARNING': '',
    };

    var body = document.querySelector('body');
    this.toastsContainer = document.createElement('div');
    this.toastsContainer.classList.add('toasts', 'border-0');
    body.appendChild(this.toastsContainer);
  }

  showSuccess(message) {
    return this._showToast(message, 'SUCCESS');
  }
  showError(message) {
    return this._showToast(message, 'ERROR');
  }
  showInfo(message) {
    return this._showToast(message, 'INFO');
  }
  showWarning(message) {
    return this._showToast(message, 'WARNING');
  }
  _showToast(message, toastType) {
    var newId = this.id + 1;

    var newToast = document.createElement('div');
    newToast.style.display = 'inline-block';
    newToast.classList.add(toastType.toLowerCase());
    newToast.classList.add('toast');
    newToast.innerHTML = `
      <progress max="100" value="0"></progress>
      <h3> ${message} </h3>`;
    var newToastObject = {
      id: newId,
      message,
      type: toastType,
      timeout: 4000,
      progressElement: newToast.querySelector('progress'),
      counter: 0,
      timer: setInterval(() => {
        newToastObject.counter += 1000 / newToastObject.timeout;
        newToastObject.progressElement.value = newToastObject.counter.toString();
        if(newToastObject.counter >= 100) {
          newToast.style.display = 'none';
          clearInterval(newToastObject.timer);
          this.toasts = this.toasts.filter((toast) => {
            return toast.id === newToastObject.id;
          });
        }
      }, 10)
    }

    newToast.addEventListener('click', () => {
      newToast.style.display = 'none';
      clearInterval(newToastObject.timer);
      this.toasts = this.toasts.filter((toast) => {
        return toast.id === newToastObject.id;
      });
    });

    this.toasts.push(newToastObject);
    this.toastsContainer.appendChild(newToast);
    return this.id++;
  }
}

function toast_error(text){
  var toasts = new ToastManager();
  toasts.showError(text);
}
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
      }
    }
    ajax_link.send();
}

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
  }else if (!form.querySelector("#select_region").value){
    form.querySelector("#select_region").style.border = "1px #FF0000 solid";
    toast_error("Выберите регион!")
  }else if (!form.querySelector("#id_city").value){
    form.querySelector("#id_city").style.border = "1px #FF0000 solid";
    toast_error("Выберите город!")
  }
  form_data = new FormData(form);

  if (form.querySelector("#id_first_name").value){form.querySelector("#id_first_name").style.border = "rgba(0, 0, 0, 0.2)";}
  if (form.querySelector("#id_last_name").value){form.querySelector("#id_last_name").style.border = "rgba(0, 0, 0, 0.2)";}
  if (form.querySelector("#id_password1").value){form.querySelector("#id_password1").style.border = "rgba(0, 0, 0, 0.2)";}
  if (form.querySelector("#id_password2").value){form.querySelector("#id_password2").style.border = "rgba(0, 0, 0, 0.2)";} 
  if (form.querySelector("#select_region").value){form.querySelector("#select_region").style.border = "rgba(0, 0, 0, 0.2)";}

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
  on('#ajax', 'change', '.select_region', function() {
    _this = this;
    var val = _this.value;
    if (val == '') {
      _this.nextElementSibling.innerHTML = "";
    } else {
      var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      link.open( 'GET', "/region/cities/" + val + "/", true );
      link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      link.onreadystatechange = function () {
        if ( link.readyState == 4 ) {
            if ( link.status == 200 ) {
                _this.nextElementSibling.innerHTML = link.responseText;
            }
        }
    };
    link.send( null );
    };
  });
