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
function toast_success(text){
  var toasts = new ToastManager();
  toasts.showSuccess(text);
}
function toast_error(text){
  var toasts = new ToastManager();
  toasts.showError(text);
}
function toast_info(text){
  var toasts = new ToastManager();
  toasts.showInfo(text);
}
function toast_warning(text){
  var toasts = new ToastManager();
  toasts.showWarning(text);
}
function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

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



function send_comment(form, block, link){
  if (!form.querySelector(".text-comment").value){
    form.querySelector(".text-comment").style.border = "1px #FF0000 solid";
    toast_error("Напишите что-нибудь");
    return
  }

  form_comment = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', link, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form.querySelector(".text-comment").value="";
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    block.append(new_post);
  }};

  link_.send(form_comment);
}

function comment_delete(_this, _link, _class){
  data = _this.parentElement.parentElement;
  comment_pk = data.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + comment_pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    comment = data.parentElement.parentElement.parentElement.parentElement;
    comment.style.display = "none";
    div = document.createElement("div");
    div.classList.add("media", "comment");

    div.innerHTML = "<p class='" + _class + "'style='cursor:pointer;text-decoration:underline;padding:15px' data-pk='" + comment_pk + "'>Комментарий удален. Восстановить</p>";
    comment.parentElement.insertBefore(div, comment);
    comment.style.display = "none";
  }};
  link.send( );
}
function comment_abort_delete(_this, _link){
  comment = _this.parentElement.nextElementSibling;
  comment.style.display = "flex";
  pk = _this.getAttribute("data-pk");
  block = _this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', _link + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
  }};
  link.send();
}




$('#russia_map path').hover(function(e){
  svg_list = this.parentElement.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    if (svg_list[i].style.fill != "green"){
    svg_list[i].style.fill = "rgba(0,0,0,0.2)";
  }
  }
  if (this.style.fill != "green"){
  this.style.fill = "#FFFFFF";
}

},

function(){
  svg_list = this.parentElement.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    if (svg_list[i].style.fill != "green"){
    svg_list[i].style.fill = "rgba(0,0,0,0.15)";
  }
  }
});

on('body', 'click', '.map_selector', function() {
  slug = this.getAttribute("data-slug");
  text = this.querySelector("title").innerHTML;
  console.log(slug + " detected!");
  map = this.parentElement;
  svg_list = map.querySelectorAll("path");
  for (var i = 0; i < svg_list.length; i++) {
    svg_list[i].style.fill = "rgba(0,0,0,0.15)";
  };
  this.style.fill = "green";
  col_md_3 = this.parentElement.parentElement.nextElementSibling;
  block = col_md_3.querySelector("#elect_for_regions_loader");
  col_md_3.querySelector(".sel__placeholder").innerHTML = text;

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/list/region/" + slug + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
            block.innerHTML = link.responseText;

        }
    }
};
link.send( null );
})


var authority_infinite = new Waypoint.Infinite({
element: $('.pag_container')[0],
onBeforePageLoad: function () {
  $('.load').show();
},
onAfterPageLoad: function ($items) {
$('.load').hide();
}
});


on('body', 'click', '.create_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/subscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.innerHTML = "<i class='fe-icon-user'></i>&nbsp;Отписаться от чиновника";
          _this.classList.add("delete_elect_subscribe");
          _this.classList.remove("create_elect_subscribe");
          toast_info("Подписка оформлена! Все подписки - в профиле.")
        }
    }
};
link.send( null );
})

on('body', 'click', '.delete_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.innerHTML = "<i class='fe-icon-user-plus'></i>&nbsp;Подписаться от чиновника";
          toast_info("Подписка отменена!");
          _this.classList.remove("delete_elect_subscribe");
          _this.classList.add("create_elect_subscribe")
        }
    }
};
link.send( null );
})

on('body', 'click', '.remove_elect_subscribe_in_profile', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");
  parent = _this.parentElement;

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          parent.style.display = "none";
          div = document.createElement("div");
          div.setAttribute("data-pk", pk);
          div.classList.add("elect_subscribe_in_profile", "cart-item", "justify-content-between", "p-4", "border", "border-primary", "pointer")
          name = parent.querySelector(".cart-item-product-title").innerHTML;
          div.innerHTML = '<h6 class="elect_name card-title">' + name + "</h6> удален из подписок. Отменить";
          parent.parentElement.insertBefore(div, parent);
          toast_info(name + " удален из подписок!");
        }
    }
};
link.send( null );
})

on('body', 'click', '.elect_subscribe_in_profile', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/elect/progs/subscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          elect =  _this.nextElementSibling;
          elect.style.display = "flex";
          name = _this.querySelector(".elect_name").innerHTML;
          _this.remove();
          toast_info(name + " возвращен в подписки!");
        }
    }
};
link.send( null );
})

on('body', 'click', '.select_elect_news_category', function() {
  _this = this;
  url = _this.getAttribute("data-href");
  if (_this.classList.contains("active")){
    return
  }
  elect_news_container = document.body.querySelector(".elect_news_container");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          links = _this.parentElement.parentElement.querySelectorAll(".select_elect_news_category");
          console.log(links);
          for (var i = 0; i < links.length; i++){
            links[i].classList.remove("active");
          }
          elem = link.responseText;
          response = document.createElement("span");
          response.innerHTML = elem;
          _this.classList.add("active");
          elect_news_container.innerHTML = "";
          elect_news_container.insertAdjacentHTML('afterBegin', response.innerHTML);
        }
    }
};
link.send( null );
})

function open_fullscreen(link, block) {
  var link_, elem;
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', link, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    block.parentElement.style.display = "block";
    block.innerHTML = elem
  }};
  link_.send();
}

function load_chart() {
    try {
        var ctx = document.getElementById('canvas');
        var dates = ctx.getAttribute('dates').split(",");
        var data_1 = ctx.getAttribute('data_views').split(",");
        var data_2 = ctx.getAttribute('data_member_views').split(",");
        var data_3 = ctx.getAttribute('data_likes').split(",");
        var data_4 = ctx.getAttribute('data_dislikes').split(",");
        var label_1 = ctx.getAttribute('label_views');
        var label_2 = ctx.getAttribute('label_member_views');
        var label_3 = ctx.getAttribute('label_likes');
        var label_4 = ctx.getAttribute('label_dislikes');
        var config = {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: label_1,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_1,
                    fill: false,
                }, {
                    label: label_2,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_2,
                }, {
                    label: label_3,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_3,
                }, {
                    label: label_4,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: ''
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }]
                }
            }
        };
        ctx.getContext('2d');
        window.myLine = new Chart(ctx, config)
    } catch {
        return
    }
}
load_chart();

function send_like(item, url){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    like.classList.toggle("text-success");
    dislike.classList.remove("text-danger");
  }};
  link.send( null );
}

function send_dislike(item, url){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.overrideMimeType("application/json");
  link.open( 'GET', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    jsonResponse = JSON.parse(link.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    dislike.classList.toggle("text-danger");
    like.classList.remove("text-success");
  }};
  link.send( null );
}
on('body', 'click', '.window_fullscreen_hide', function() {
  document.querySelector(".window_fullscreen").style.display = "none";
  document.getElementById("window_loader").innerHTML=""}
);

on('body', 'click', '.elect_new_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/progs/elect_like/" + pk + "/");
});
on('body', 'click', '.elect_new_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/progs/elect_dislike/" + pk + "/");
});

on('body', 'click', '.blog_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/progs/blog_like/" + pk + "/");
});
on('body', 'click', '.blog_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/progs/blog_dislike/" + pk + "/");
});

on('#ajax', 'click', '.load_elect_stat_year', function() {
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("window_loader");
  open_fullscreen("/stst/elect_year/" + pk + "/", loader)
});
