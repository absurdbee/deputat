
function case_news_wall(pk) {
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('GET', "/notify/new_wall/" + pk + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          lenta = document.body.querySelector('.news_stream');
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          lenta.prepend(new_post);
          document.body.querySelector(".news_empty") ? document.body.querySelector(".news_empty").style.display = "none" : null}}
  link_.send()
};
function case_user_chat_typed(pk, first_name) {
  if (document.body.querySelector(".chat_container")) {
    if (pk == document.body.querySelector(".chat_container").getAttribute("chat-pk")) {
      console.log('пользователь пишет...');
      typed_box = document.body.querySelector(".user_typed_box");
      typed_box.innerHTML = first_name + " набирает сообщение..."
      setTimeout(function(){
        typed_box.innerHTML = "";
    }, 1000)
    }
  } if (document.body.querySelector(".chat_list_container")) {
    list = document.body.querySelector(".chat_list_container");
    chat = list.querySelector('[data-pk=' + '"' + pk + '"' + ']');
    p = chat.querySelector("p");
    if (!p.nextElementSibling.innerHTML) {
      p.style.display = "none";
      p.nextElementSibling.innerHTML = first_name + " набирает сообщение...";
      setTimeout(function(){
        p.nextElementSibling.innerHTML = "";
        p.style.display = "unset";
      }, 1000);
    } else {
      p.style.display = "unset";
    }
  }
};
function case_user_chat_read(pk) {
  if (document.body.querySelector(".chat_container")) {
    if (pk == document.body.querySelector(".chat_container").getAttribute("chat-pk")) {
      console.log('пользователь прочитал сообщения...');
      box = document.body.querySelector(".chat_container");
      list = box.querySelectorAll(".message");
      for (var i = 0; i < list.length; i++){
        list[i].classList.remove("bg-light-secondary")
      }
    }}
    else if (document.body.querySelector(".chat_list_container")) {
    list = document.body.querySelector(".chat_list_container");
    chat = list.querySelector('[data-pk=' + '"' + pk + '"' + ']');
    chat.querySelector("p").classList.remove("bg-light-secondary");
  }
};
function plus_1_badge_message() {
  chats = document.body.querySelector(".new_unread_chats");
  chats.querySelector(".tab-badge") ? (count = chats.innerHTML.replace(/\s+/g, ''), count = count*1) : count = 0;
  count += 1;
  chats.classList.add("badge-success", "tab-badge");
  chats.innerHTML = "";
  chats.innerHTML = count;
};
function case_u_message_create(chat_id, message_uuid, beep) {
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');

  if (document.body.querySelector(".chat_list_container")) {
    // если в момент получения нового сообщения получатель на странице списка чатов
    console.log("Вы на странице сообщений");
  link_.open('GET', "/chat/user_progs/load_message/" + message_uuid + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          plus_1_badge_message();
          lenta = document.body.querySelector('.is_paginate');
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          lenta.querySelector('[data-pk=' + '"' + chat_id + '"' + ']') ? (li = lenta.querySelector('[data-pk=' + '"' + chat_id + '"' + ']'), li.innerHTML = new_post.innerHTML)
          : lenta.prepend(new_post);
          document.body.querySelector(".items_empty") ? document.body.querySelector(".items_empty").style.display = "none" : null}}
  link_.send()
}
  else if (document.body.querySelector(".chat_container") && document.body.querySelector(".chat_container").getAttribute('chat-pk') == chat_id) {
    // если в момент получения нового сообщения получатель на странице чата, в котором ему написалм
    console.log("Вы на странице чата");
    link_.open('GET', "/chat/user_progs/load_chat_message/" + message_uuid + "/", true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        lenta = document.body.querySelector('.is_paginate');
        elem = link_.responseText;
        new_post = document.createElement("span");
        new_post.innerHTML = elem;
        lenta.append(new_post);
        window.scrollTo( 0, 3000 );
        document.body.querySelector(".items_empty") ? document.body.querySelector(".items_empty").style.display = "none" : null}}
  link_.send()
} else {
  // если в момент получения нового сообщения получатель не на странице чата или списка чатов
  console.log("Вы не в сообщениях");
  plus_1_badge_message();
  };
  // добавим единичку к счетчику на панели, а если пользователь на странице чата
  // то добавим программу, которая прочитает сообщение и на единичку убавит счетчик на панели

  if (beep) {
    audio = new Audio('/static/audio/apple/message.mp3');
    audio.volume = 0.4;
    audio.play()
  }
};

if (!document.body.querySelector(".anon_avatar")){
  // подключаем сокеты только для зарегистрированных пользователей
notify = document.body.querySelector(".resent_notify");
document.body.querySelector(".userpic") ? request_user_id = document.body.querySelector(".userpic").getAttribute("data-pk") : request_user_id = 0
notify.innerHTML ? (notify_count = notify.innerHTML.replace(/\s+/g, ''), notify_count = notify_count*1): notify_count = 0;

ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
ws_path = ws_scheme + '://' + window.location.host + ":8443/notify/";
webSocket = new channels.WebSocketBridge();
webSocket.connect(ws_path);

webSocket.socket.onmessage = function(e){ console.log(e.data); };
webSocket.socket.onopen = function () {console.log("Соединение установлено!")};
webSocket.socket.onclose = function () {console.log("Соединение прервано...")};

webSocket.listen(function (event) {
  switch (event.key) {
      case "notification":
        if (event.recipient_id == request_user_id){
          notify_count += 1;
          notify.innerHTML = notify_count;
          console.log("теперь кол-во уведов - " + notify_count);
          new Audio('/static/audio/apple/stargaze.mp3').play();
        }
        break;

      case "wall":
            if (event.name == "user_wall"){
              // появление новых записей на стене, сваязанных с пользователями (например, действия челов разной направленности)
              case_user_wall()
            }
            else if (event.name == "news_wall"){
              // появление новых записей на главной стене
              if (document.body.querySelector(".news_stream")) {case_news_wall(event.id)}
            }
          break;
      case "message":
        if (event.name == "u_message_create"){
          if (event.recipient_id == request_user_id ){
            case_u_message_create(event.chat_id, event.message_id, event.beep)
          }
        }
        else if (event.name == "u_message_typed"){
          if (event.recipient_id != request_user_id){
            case_user_chat_typed(event.chat_id, event.user_name)
          }
        }
        else if (event.name == "u_message_read"){
          if (event.recipient_id != request_user_id){
            case_user_chat_read(event.chat_id)
          }
        }
        break;

    default:
      console.log('error: ', event);
      break;
  }
})
}
