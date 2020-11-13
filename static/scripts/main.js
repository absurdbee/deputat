function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

on('body', 'click', '#register_ajax', function() {
  if (!document.body.querySelector("#email").value){
    document.body.querySelector("#email").style.border = "1px #FF0000 solid";
    toast_error("Почта - обязательное поле!");
  } else if (!document.body.querySelector("#password1").value){
    document.body.querySelector("#password1").style.border = "1px #FF0000 solid";
    toast_error("Пароль - обязательное поле!")
  } else if (!document.body.querySelector("#password2").value){
    document.body.querySelector("#password2").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль еще раз!")
  }
  form_data = new FormData(document.querySelector("#signup"));
  reg_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  reg_link.open( 'POST', "/rest-auth/registration/", true );
  reg_link.onreadystatechange = function () {
  if ( reg_link.readyState == 4 && reg_link.status == 201 ) {
    window.location.href = "/"
    }};
  reg_link.send(form_data);
})
on('body', 'click', '#logg', function() {
  if (!document.body.querySelector("#email").value){
    document.body.querySelector("#email").style.border = "1px #FF0000 solid";
    toast_error("Введите никнейм!")}
  else if (!document.body.querySelector("#password").value){
    document.body.querySelector("#password").style.border = "1px #FF0000 solid";
    toast_error("Введите пароль!")}
  if (document.body.querySelector("#email").value){document.body.querySelector("#email").style.border = "rgba(0, 0, 0, 0.2)";}
  if (document.body.querySelector("#password").value){document.body.querySelector("#password").style.border = "rgba(0, 0, 0, 0.2)";}

  form_data = new FormData(document.querySelector("#login_form"));
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', "/rest-auth/login/", true );
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    window.location.href = "/";
    }};
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

function send_like(item, link){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.overrideMimeType("application/json");
  link__.open( 'GET', link, true );
  link__.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    jsonResponse = JSON.parse(link__.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    like.classList.toggle("text-success");
    dislike.classList.remove("text-danger");
  }};
  link__.send( null );
}

function send_dislike(item, link){
  like = item.querySelector(".like");
  dislike = item.querySelector(".dislike");
  link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link__.overrideMimeType("application/json");
  link__.open( 'GET', link, true );
  link__.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link__.onreadystatechange = function () {
  if ( link__.readyState == 4 && link__.status == 200 ) {
    jsonResponse = JSON.parse(link__.responseText);
    likes_count = item.querySelector(".likes_count");
    dislikes_count = item.querySelector(".dislikes_count");
    likes_count.innerHTML = jsonResponse.like_count;
    dislikes_count.innerHTML = jsonResponse.dislike_count;
    dislike.classList.toggle("text-danger");
    like.classList.remove("text-success");
  }};
  link__.send( null );
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
  link.open( 'GET', "/blog/progs/subscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.innerHTML = " Отписаться от чиновника";
          toast_success("Подписка оформлена! Все подписки - в профиле.")
        }
    }
};
link.send( null );
})

on('body', 'click', '.delete_elect_subscribe', function() {
  _this = this;
  pk = _this.getAttribute("data-pk");

  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/blog/progs/unsubscribe/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 ) {
        if ( link.status == 200 ) {
          _this.innerHTML = " Подписаться от чиновника";
          toast_success("Подписка отменена!")
        }
    }
};
link.send( null );
})
