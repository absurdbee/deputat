function setEndOfContenteditable(contentEditableElement) {
    var range,selection;
    if(document.createRange) {
        range = document.createRange();
        range.selectNodeContents(contentEditableElement);
        range.collapse(false);
        selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }
    else if(document.selection) {
        range = document.body.createTextRange();
        range.moveToElementText(contentEditableElement);
        range.collapse(false);
        range.select();
    }
};
function get_toggle_messages() {
  list = document.body.querySelectorAll(".target_message");
  query = [];
  for (var i = 0; i < list.length; i++){
      query.push(list[i])
  };
  return query
};
function show_chat_console(message) {
  _console = document.body.querySelector(".console_btn_other");
  if (message.querySelector(".message_sticker") || message.querySelector(".audio") || !message.classList.contains("is_have_edited")) {
    _console.querySelector(".u_message_edit").style.display = "none"
  };

  favourite_btn = _console.querySelector(".toggle_messages_favourite");
  list_not_have_favourite_messages = true;
  for (var i = 0; i < get_toggle_messages().length; i++){
    if (!list[i].querySelector(".delete_favourite_message")) {
        list_not_have_favourite_messages = false;
      }
    };
  if (list_not_have_favourite_messages) {
    favourite_btn.innerHTML = '<path d="M0 0h24v24H0z" fill="none"/><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>'
    favourite_btn.parentElement.setAttribute("tooltip","Удалить из избранного");
    favourite_btn.classList.add("remove_favourite_messages");
    favourite_btn.classList.remove("create_favourite_messages")
  } else {
    favourite_btn.parentElement.setAttribute("tooltip","Отметить как важное");
    favourite_btn.innerHTML = '<path d="M12 7.13l.97 2.29.47 1.11 1.2.1 2.47.21-1.88 1.63-.91.79.27 1.18.56 2.41-2.12-1.28-1.03-.64-1.03.62-2.12 1.28.56-2.41.27-1.18-.91-.79-1.88-1.63 2.47-.21 1.2-.1.47-1.11.97-2.27M12 2L9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2z"/>'
    favourite_btn.classList.remove("remove_favourite_messages");
    favourite_btn.classList.add("create_favourite_messages")
  };

  _console.style.display = "unset";
  _console.previousElementSibling.style.display = "none";
  _console.previousElementSibling.style.left = "8px";
  _console.parentElement.parentElement.querySelector("h5").style.display = "none"
};

function edit_favourite_count(count, type) {
  if (document.body.querySelector(".favourite_block")) {
    block = document.body.querySelector(".favourite_block");
    try {
      _count = block.querySelector(".favourite_messages_count").innerHTML
    } catch {_count = 0};
    _count *= 1;
    if (type == "plus") {
      _count += count;
      block.parentElement.parentElement.classList.remove("hidden");
      block.querySelector(".favourite_messages_count").innerHTML = _count
    }
    else if (type == "minus") {
      _count -= count;
      block.querySelector(".favourite_messages_count").innerHTML = _count
      if (_count < 1) {
        block.parentElement.parentElement.classList.add("hidden");
      }
    }
  }
};

on('#ajax', 'click', '.u_message_unfixed', function() {
  message = this.parentElement.parentElement;
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/chat/user_progs/unfixed_message/" + message.getAttribute("data-uuid") + "/", true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        fix_span = message.parentElement.parentElement.parentElement.querySelector(".count_fixed_messages")
        fix_count = fix_span.innerHTML;
        fix_count *= 1;
        fix_count -= 1;
        fix_span.innerHTML = fix_count;
        message.remove();
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.chat_search_btn', function() {
  value = this.parentElement.previousElementSibling;
  if (!value.value) {
    return
  }
  chat = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/chat/" + chat.getAttribute("data-pk") + "/search/?q=" + value.value, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        chatview = chat.querySelector(".chatview");
        chatview.querySelector(".chatlist").style.display = "none";
        if (chatview.querySelector(".show_search_result")) {
          chatview.querySelector(".show_search_result").innerHTML = ""
        } else {
          span = document.createElement('span');
          span.classList.add("show_search_result");
          chatview.prepend(span);
        };
        span.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.delete_favourite_message', function() {
  uuid = this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-uuid")
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/chat/user_progs/unfavorite_messages/?list=" + [uuid], true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        edit_favourite_count(1, "minus");
        messages = document.body.querySelectorAll( '[data-pk=' + '"' + uuid + '"' + ']' );
        for (var i = 0; i < messages.length; i++){
          messages[i].querySelector(".favourite_icon").innerHTML = ""
        }
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.create_favourite_messages', function() {
  hide_chat_console();
  messages = [];
  list = get_toggle_messages();
  for (var i = 0; i < list.length; i++){
    if (!list[i].querySelector(".delete_favourite_message")) {
        messages.push(list[i].getAttribute("data-uuid"));
        list[i].querySelector(".favourite_icon").innerHTML = '<svg width="18" height="18" class="delete_favourite_message pointer" fill="currentColor" enable-background="new 0 0 24 24" viewBox="0 0 24 24"><path d="M12 7.13l.97 2.29.47 1.11 1.2.1 2.47.21-1.88 1.63-.91.79.27 1.18.56 2.41-2.12-1.28-1.03-.64-1.03.62-2.12 1.28.56-2.41.27-1.18-.91-.79-1.88-1.63 2.47-.21 1.2-.1.47-1.11.97-2.27M12 2L9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2z"/></svg>'
    };
    list[i].classList.remove("custom_color", "target_message")
  };

  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/chat/user_progs/favorite_messages/?list=" + messages, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        edit_favourite_count(messages.length, "plus")
      }
    }
    ajax_link.send();
});
on('#ajax', 'click', '.remove_favourite_messages', function() {
  hide_chat_console();
  messages = [];
  list = get_toggle_messages();
  for (var i = 0; i < list.length; i++){
    if (list[i].querySelector(".delete_favourite_message")) {
        messages.push(list[i].getAttribute("data-uuid"));
        list[i].querySelector(".favourite_icon").innerHTML = ''
    };
    list[i].classList.remove("custom_color", "target_message")
  };

  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', "/chat/user_progs/unfavorite_messages/?list=" + messages, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        edit_favourite_count(messages.length, "minus")
      }
    }
    ajax_link.send();
});

function hide_chat_console() {
  _console = document.body.querySelector(".console_btn_other");
  _console.querySelector(".u_message_edit").style.display = "unset";
  _console.style.display = "none";
  _console.previousElementSibling.style.display = "unset";
  _console.parentElement.parentElement.querySelector("h5").style.display = "unset"
};

on('#ajax', 'click', '.message_dropdown', function() {this.nextElementSibling.classList.toggle("show")});
on('#ajax', 'click', '.smile_sticker_dropdown', function() {
  block = this.nextElementSibling;
  if (!block.querySelector(".card")) {
    list_load(block, "/users/load/smiles_stickers/")
  };
  block.classList.toggle("show");
});


on('#ajax', 'click', '.chat_search', function() {
  header = this.parentElement.parentElement.parentElement;
  input = header.nextElementSibling;
  input.style.display = "flex";
  header.style.display = "none";
  input.querySelector(".form-control").focus();
});
on('#ajax', 'click', '.hide_chat_search', function() {
  search = this.parentElement.parentElement;
  search.previousElementSibling.style.display = "flex";
  search.style.display = "none";
  if (document.body.querySelector(".show_search_result")) {
    document.body.querySelector(".show_search_result").innerHTML = "";
    document.body.querySelector(".chatlist").style.display = "block";
  }
});

on('#ajax', 'click', '.u_chat_info', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")
  create_fullscreen("/chat/" + pk + "/info/", "worker_fullscreen");
});
on('#ajax', 'click', '.favourite_messages_list', function() {
  create_fullscreen("/chat/favourites_messages/", "worker_fullscreen");
});
on('#ajax', 'click', '.user_chat_settings', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")
  create_fullscreen("/chat/user_progs/edit/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.user_chat_settings_private', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")
  create_fullscreen("/chat/user_progs/private/" + pk + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.show_attach_files', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")
  create_fullscreen("/chat/" + pk + "/collections/", "item_fullscreen");
});
on('#ajax', 'click', '.select_chat_collections', function() {
  _this = this;
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  ajax_link.open( 'GET', "/chat/" + this.parentElement.getAttribute("chat-pk") + "/collections/?type=" + this.getAttribute("data-type"), true );
	ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  ajax_link.onreadystatechange = function () {
    if ( this.readyState == 4 && this.status == 200 ) {
      elem = document.createElement('span');
      elem.innerHTML = ajax_link.responseText;
      _this.parentElement.parentElement.parentElement.nextElementSibling.innerHTML = elem.querySelector(".load_block").innerHTML;
    }
  };
  ajax_link.send();
});

function create_user_input_card(name, pk, link) {
  $span = document.createElement("span");
  $span.setAttribute("data-pk", pk);
  $span.classList.add("btn","btn-sm","custom_color");
  $span.innerHTML = "<a href='" + link + "' target='_blank' >" + name + "</a><span class='remove_user_input pointer'>x<span>";
  $span.style.margin = "2px";
  $input = document.createElement("input");
  $input.classList.add("user_pk");
  $input.setAttribute("type", "hidden");
  $input.setAttribute("name", "users");
  $input.value = pk;
  $span.append($input);
  return $span
};

on('#ajax', 'click', '.remove_user_input', function() {
  parent = this.parentElement;
  header = parent.parentElement;
  parent.remove();
  container = header.parentElement;
  btn = container.querySelector(".form_btn");
  if (!header.querySelector(".remove_user_input")) {
    header.querySelector(".header_title").style.display = "block";
  };

  friend = container.querySelector('[data-pk=' + '"' + this.nextElementSibling.value + '"' + ']');
  friend.querySelector(".active_svg").classList.remove("active_svg");
  count = container.querySelectorAll(".active_svg").length;
  if (count > 1) {
    btn_text = "Выбрать пользователей" + " (" + count + ")";
    btn.disabled = false;
  } else if (count == 1) {
    btn_text = "Выбрать пользователя";
    btn.disabled = false;
  } else {
    btn_text = "Выбрать пользователей";
    btn.disabled = true;
  };
  btn.innerHTML = btn_text;
});

on('#ajax', 'click', '.add_member_chat_toggle', function() {
  container = this.parentElement.parentElement.parentElement;
  btn = container.querySelector(".form_btn");
  header = container.querySelector(".card-header");
  header_title = header.querySelector(".header_title");
  pk = this.getAttribute("data-pk");
  link = this.getAttribute("data-link");

  if (this.querySelector(".active_svg")) {
    input_svg = this.querySelector(".active_svg");
    input_svg.classList.remove("active_svg");
    input_svg.setAttribute("tooltip", "Выбрать друга")
    friend_input = header.querySelector('[data-pk=' + '"' + pk + '"' + ']');
    friend_input.remove();
    if (!header.querySelector(".remove_user_input")) {
      header.querySelector(".header_title").style.display = "block";
    }
  } else {
    input_svg = this.querySelector(".item_attach_circle");
    input_svg.classList.add("active_svg");
    input_svg.setAttribute("tooltip", "Отменить")
    header_title.style.display = "none";
    header.append(create_user_input_card(this.querySelector("h6").innerHTML, pk, link))
  };

  count = container.querySelectorAll(".active_svg").length;
  if (count > 1) {
    btn_text = "Выбрать пользователей" + " (" + count + ")";
    btn.disabled = false;
  } else if (count == 1) {
    btn_text = "Выбрать пользователя";
    btn.disabled = false;
  } else {
    btn_text = "Выберите пользователей";
    btn.disabled = true;
  };
  btn.innerHTML = btn_text;
});

on('#ajax', 'input', '.smile_supported', function() {
  _this = this;

  if (_this.classList.contains("chat_message_text")){
    if (document.body.querySelector(".chatlist")) {
      check_message_form_btn()
    };
    if (!_this.classList.contains("draft_created")) {
        _this.classList.add("draft_created");
        remove_class_timeout(_this);
        setTimeout(function(){
          form = _this.parentElement.parentElement;
          send_draft_message (form, "/chat/user_progs/save_draft_message/" + form.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/");
      }, 1000)
    }
  };
});

on('#ajax', 'click', '.show_chat_fixed_messages', function() {
  pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('chat-pk');
  create_fullscreen("/chat/" + pk + "/fixed_messages/", "item_fullscreen");
});

on('#ajax', 'click', '.classic_smile_item', function() {
  input = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector(".smile_supported");
  $img = document.createElement("img");
  $img.src = this.getAttribute("src");
  input.append($img);
  if (document.body.querySelector(".chatlist")) {
  show_message_form_send_btn()
  };
  setEndOfContenteditable(input);
});

function send_comment_sticker(form_post,value) {
  comment_form = false, reply_form = false, parent_form = false;
  $sticker = document.createElement("input");
  $sticker.setAttribute("name", "sticker");
  $sticker.setAttribute("type", "hidden");
  $sticker.classList.add("sticker");
  $sticker.value = value;
  form_post.append($sticker);
  form = new FormData(form_post);
  if (form_post.querySelector(".comment_form")){
    if (form_post.classList.contains("u_post_comment")) {url = '/posts/user_progs/add_comment/'}
    else if (form_post.classList.contains("c_post_comment")) {url = '/posts/community_progs/add_comment/'}
    else if (form_post.classList.contains("u_video_comment")) {url = '/video/user_progs/add_comment/'}
    else if (form_post.classList.contains("c_video_comment")) {url = '/video/community_progs/add_comment/'}
    else if (form_post.classList.contains("u_photo_comment")) {url = '/gallery/user_progs/add_comment/'}
    else if (form_post.classList.contains("c_photo_comment")) {url = '/gallery/community_progs/add_comment/'}
    else if (form_post.classList.contains("u_good_comment")) {url = '/goods/user_progs/add_comment/'}
    else if (form_post.classList.contains("c_good_comment")) {url = '/goods/community_progs/add_comment/'};
    comment_form = true
  }
  else if (form_post.querySelector(".reply_form") || form_post.querySelector(".parent_form")) {
    if (form_post.classList.contains("u_post_comment")) {url = '/posts/user_progs/reply_comment/'}
    else if (form_post.classList.contains("c_post_comment")) {url = '/posts/community_progs/reply_comment/'}
    else if (form_post.classList.contains("u_video_comment")) {url = '/video/user_progs/reply_comment/'}
    else if (form_post.classList.contains("c_video_comment")) {url = '/video/community_progs/reply_comment/'}
    else if (form_post.classList.contains("u_photo_comment")) {url = '/gallery/user_progs/reply_comment/'}
    else if (form_post.classList.contains("c_photo_comment")) {url = '/gallery/community_progs/reply_comment/'}
    else if (form_post.classList.contains("u_good_comment")) {url = '/goods/user_progs/reply_comment/'}
    else if (form_post.classList.contains("c_good_comment")) {url = '/goods/community_progs/reply_comment/'}
  };
  if (form_post.querySelector(".reply_form")) {
    reply_form = true
  } else {parent_form = true};

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('POST', url, true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          form_post.querySelector(".comment_text").innerHTML = "";
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          if (comment_form) {
            block = form_post.parentElement.previousElementSibling
          } else if (reply_form) {
            block = form_post.parentElement.parentElement.querySelector(".stream_reply_comments")
          } else if (parent_form) {
            block = form_post.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
          }

          form_post.querySelector(".comment_text").classList.remove("border_red");
          form_post.querySelector(".hide_block_menu").classList.remove("show");
          form_post.querySelector(".dropdown").classList.remove("border_red");
          form_post.querySelector(".sticker").remove();
          block.append(new_post);

      }
  };
  link_.send(form)
};

on('#ajax', 'click', '.classic_sticker_item', function() {
  if (document.body.querySelector(".chatlist")){
    url = "/chat/user_progs/send_message/" + document.body.querySelector(".pk_saver").getAttribute("chat-pk") + "/";
    send_message_sticker(url, this.getAttribute("data-pk"))
  } else if (document.body.querySelector("#send_page_message_btn")){
    url = '/chat/user_progs/send_page_message/' + document.body.querySelector("#send_page_message_btn").getAttribute("data-pk") + '/'
    send_message_sticker(url, this.getAttribute("data-pk"))
  } else if (this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector(".check_mesage_form")){
    form = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    send_comment_sticker(form, this.getAttribute("data-pk"))
  }
});

function send_message_sticker(url, value) {
  is_chat = false; is_page = false;
  console.log(value);
  if (document.body.querySelector(".chatlist")){is_chat = true} else {is_page = true};
  if (is_chat) {
    form_post = document.body.querySelector(".customize_form")
  } else {
    form_post = document.body.querySelector(".page_message_form")
  }
  $sticker = document.createElement("input");
  $sticker.setAttribute("name", "sticker");
  $sticker.setAttribute("type", "text");
  $sticker.classList.add("sticker");
  $sticker.value = value;
  form_post.append($sticker);
  form_data = new FormData(form_post);
  if (document.body.querySelector(".chatlist")){is_chat = true} else {is_page = true};

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    if (is_chat) {
      elem = link_.responseText;
      message_load = form_post.parentElement.parentElement.querySelector(".chatlist");
      new_post = document.createElement("span");
      new_post.innerHTML = elem;
      message_load.append(new_post);
      message_load.querySelector(".items_empty") ? message_load.querySelector(".items_empty").style.display = "none" : null;
      form_post.querySelector(".message_text").classList.remove("border_red");
      form_post.querySelector(".hide_block_menu").classList.remove("show");
      form_post.querySelector(".message_dropdown").classList.remove("border_red");
      form_post.querySelector(".sticker").remove();
      if (document.querySelector(".chat_container")) {
        window.scrollTo({
          top: 12000,
          behavior: "smooth"
        })
      };
    } else {
      document.querySelector(".item_fullscreen").style.display = "none";
      document.getElementById("item_loader").innerHTML="";
    }
  }};
  link_.send(form_data);
};

on('#ajax', 'click', '.user_create_chat', function() {
  create_fullscreen("/chat/user_progs/create_chat/" + this.getAttribute("data-pk") + "/", "worker_fullscreen");
});
on('#ajax', 'click', '.user_send_page_message', function() {
  create_fullscreen("/chat/user_progs/send_page_message/" + this.getAttribute("data-pk") + "/", "worker_fullscreen");
});

on('#ajax', 'click', '.u_chat_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = document.body.querySelector(".pk_saver").getAttribute('chat-pk')
  create_fullscreen("/gallery/user/chat_photo/" + pk + "/" + photo_pk + "/", "photo_fullscreen");
});
on('#ajax', 'click', '.c_chat_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = document.body.querySelector(".pk_saver").getAttribute('chat-pk')
  create_fullscreen("/gallery/community/chat_photo/" + pk + "/" + photo_pk + "/", "photo_fullscreen");
});

on('#ajax', 'click', '.user_add_members', function() {
  block = this.nextElementSibling.querySelector("#chat_members");
  if (!block.querySelector(".load_pag")){
  block.classList.add("mt-4");
  list_load(block, "/users/load/friends/")
} else { block.style.display = "block"}
});

on('#ajax', 'click', '#add_chat_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  this.disabled = true;
  pk = this.getAttribute("data-pk");
  form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/chat/user_progs/create_chat/' + pk + '/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            pk = rtr.querySelector(".pk_saver").getAttribute("data-pk");
            window.scrollTo(0,0);
            document.title = elem_.querySelector('title').innerHTML;
            if_list(rtr);
            window.history.pushState(null, "vfgffgfgf", "/chat/" + pk + "/");
            get_document_opacity_1();
        }
      }
      ajax_link.send(form_data);
});

on('#ajax', 'click', '#send_page_message_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  _text = form.querySelector(".page_message_text").innerHTML;
  if (_text.replace(/<[^>]*(>|$)|&nbsp;|&zwnj;|&raquo;|&laquo;|&gt;/g,'').trim() == "" && form.querySelector(".files_0")){
    toast_error("Напишите или прикрепите что-нибудь");
    form.querySelector(".page_message_text").classList.add("border_red");
    return
  };

  this.disabled = true;
  form.querySelector(".type_hidden").value = form.querySelector(".page_message_text").innerHTML;
  form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/chat/user_progs/send_page_message/' + this.getAttribute("data-pk") + '/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            toast_success("Сообщение отправлено");
            close_work_fullscreen();
        } else {this.disabled = false}
      }
      ajax_link.send(form_data);
});

function send_message (form_post, url) {
  text_val = form_post.querySelector(".smile_supported");
  _val = format_text(text_val);
  _text = _val.innerHTML;

  if (_text.replace(/<(?!br)(?!img)\/?[a-z][^>]*(>|$)/gi, "").trim() == "" && form_post.querySelector(".files_0") && !form_post.querySelector(".transfer")){
    toast_error("Напишите или прикрепите что-нибудь");
    form_post.querySelector(".message_text").classList.add("border_red");
    form_post.querySelector(".message_dropdown").classList.add("border_red");
    return
  };
  text = form_post.querySelector(".type_hidden");
  text.value = _text;
  form_data = new FormData(form_post);
  message_load = form_post.parentElement.parentElement.parentElement.querySelector(".chatlist");
  pk = document.body.querySelector(".pk_saver").getAttribute("chat-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    clear_message_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    message_load.append(new_post);
    message_load.querySelector(".items_empty") ? message_load.querySelector(".items_empty").style.display = "none" : null;
    form_post.querySelector(".message_text").classList.remove("border_red");
    form_post.querySelector(".hide_block_menu").classList.remove("show");
    form_post.querySelector(".message_text").innerHTML = ""
    form_post.querySelector(".message_dropdown").classList.remove("border_red");
    try{form_post.querySelector(".parent_message_block").remove()}catch{null};
    form_post.querySelector(".type_hidden").value = '';
    show_message_form_voice_btn();
    if (document.querySelector(".chat_container")) {
      window.scrollTo({
        top: 12000,
        behavior: "smooth"
      })
    };
  }};
  link_.send(form_data);
};

on('#ajax', 'click', '.u_message_fixed', function() {
  message = document.body.querySelector(".target_message");
  hide_chat_console();
  uuid = message.getAttribute("data-uuid");

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/fixed_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    hide_chat_console();
    if (message.querySelector(".attach_container")) {
      parent = "Вложения"
    } else if (message.querySelector(".text") != null) {
      parent = message.querySelector(".text").innerHTML.replace(/<br>/g,"  ")
    } else if(message.querySelector(".message_sticker")) {
        parent = "Наклейка"
    };
    creator_p = '<p><svg style="width: 17px;vertical-align: bottom;" fill="currentColor" viewBox="0 0 24 24"><g><rect fill="none" height="16" width="16"/></g><g><path d="M16,9V4l1,0c0.55,0,1-0.45,1-1v0c0-0.55-0.45-1-1-1H7C6.45,2,6,2.45,6,3v0 c0,0.55,0.45,1,1,1l1,0v5c0,1.66-1.34,3-3,3h0v2h5.97v7l1,1l1-1v-7H19v-2h0C17.34,12,16,10.66,16,9z" fill-rule="evenodd"/></g></svg>' + message.querySelector(".creator_name").innerHTML + '</p>';
    message.classList.remove("target_message", "custom_color");
    block = document.body.querySelector(".fixed_messages");
    block.innerHTML = "<div class='pointer show_chat_fixed_messages'>" + creator_p + "<div class='border-bottom' style='position:relative;padding-bottom: 5px;'><div style='overflow: hidden;text-overflow:ellipsis;padding-right:5px;'><span style='white-space: nowrap;'>" + parent + "</span></div></div></div>";

    message_load = document.body.querySelector(".chatlist");
    elem = link.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    message_load.append(new_post);
    objDiv = document.body.querySelector("#chatcontent");
    objDiv.scrollTop = objDiv.scrollHeight;
  }};
  link.send();
});

on('#ajax', 'click', '.u_message_reply', function() {
  message = document.body.querySelector(".target_message");
  hide_chat_console();
  message.classList.remove("target_message", "custom_color");
  if (message.querySelector(".attach_container")) {
    parent = "Вложения"
  } else if (message.querySelector(".text") != null) {
    parent = message.querySelector(".text").innerHTML.replace(/<br>/g,"  ")
  } else if(message.querySelector(".message_sticker")) {
      parent = "Наклейка"
  };
  creator_p = '<p><a class="underline" target="_blank" href="' + message.querySelector(".creator_link").getAttribute("href") + '">' + message.querySelector(".creator_name").innerHTML + '</a></p>'

  block = document.body.querySelector(".parent_message_block");
  block.innerHTML = "<div>" + creator_p + "<div style='position:relative;padding-bottom:7px'><input type='hidden' name='parent' value='" + message.getAttribute("data-pk") + "'><div style='overflow: hidden;text-overflow:ellipsis;padding-right:5px;'><span style='white-space: nowrap;'>" + parent + "</span><span class='remove_parent_block message_form_parent_block pointer'>x</span></div></div></div>"
  setTimeout(function(){
    form = block.parentElement;
      send_draft_message (form, "/chat/user_progs/save_draft_message/" + form.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/");
}, 1000)
});

on('#ajax', 'click', '.u_message_edit', function() {
  hide_chat_console();
  message = document.body.querySelector(".target_message");
  message.classList.remove("target_message", "custom_color");
  message.style.display = "none";

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/chat/user_progs/edit_message/" + message.getAttribute("data-uuid") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    response = document.createElement("span");
    response.innerHTML = link_.responseText;
    box = message.nextElementSibling;
    box.innerHTML = response.innerHTML;
    objDiv = document.body.querySelector(".chatlist");
    objDiv.scrollTop = objDiv.scrollHeight;
    }
  };
  link_.send();
});

function send_draft_message (form_post, url) {
  _text = form_post.querySelector(".message_text").innerHTML;
  text_val = form_post.querySelector(".smile_supported");
  _val = format_text(text_val);
  _text = _val.innerHTML;

  if (!_text == "" && _text.replace(/<(?!img)\/?[a-z][^>]*(>|$)/gi, "").trim() == "") {
    console.log("Не не!");
    return
  }

  text = form_post.querySelector(".type_hidden");
  text.value = form_post.querySelector(".message_text").innerHTML.replace("data:image", '');
  setEndOfContenteditable(text_val);
  form_data = new FormData(form_post);
  pk = document.body.querySelector(".pk_saver").getAttribute("chat-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url, true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
  }};
  link_.send(form_data);
};

on('#ajax', 'click', '#message_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  send_message (form_post, "/chat/user_progs/send_message/" + document.body.querySelector(".pk_saver").getAttribute("chat-pk") + "/")
});

on('#ajax', 'keydown', '.message_text', function(e) {
  if (e.shiftKey && e.keyCode === 13) {this.append("\n");}
  else if (e.keyCode == 13) {
    e.preventDefault();
  form_post = this.parentElement.parentElement;
  send_message (form_post, "/chat/user_progs/send_message/" + document.body.querySelector(".pk_saver").getAttribute("chat-pk") + "/")
}});
on('#ajax', 'keydown', '.page_message_text', function(e) {
  if (e.shiftKey && e.keyCode === 13) {this.append("\n");}
  else if (e.keyCode == 13) {
    this.append("\n");
}});

on('#ajax', 'click', '.chat_ajax', function(e) {
  _this = this;
  e.preventDefault();
	var url = this.getAttribute('href');
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

        width = rtr.querySelector(".main_chat_block").offsetWidth - 14;
        rtr.querySelector(".fixed_header_chat").style.width = width + "px";
        window.scrollTo( 0, 3000 );
        scrolled(rtr.querySelector('.is_paginate'));
        window.history.pushState(null, "vfgffgfgf", url);

        chats = document.body.querySelector(".new_unread_chats");
        if (chats.querySelector(".tab_badge") && _this.querySelector(".tab_badge")) {
          all_count = chats.innerHTML.replace(/\s+/g, '');
          all_count = all_count * 1;
          result = all_count - 1;
          result > 0 ? chats.innerHTML = result : chats.innerHTML = '';
          console.log("Вычитаем 1, так как в чате есть непрочитанные сообщения")
        };
        if (document.body.querySelector(".left_panel_menu")) {
          setEndOfContenteditable(document.body.querySelector(".message_text"));
        };
        }
      }
    ajax_link.send();
});

on('#ajax', 'click', '.toggle_message', function(e) {
  if (e.target.classList.contains("t_f")) {
  message = this, is_toggle = false, btn_console = document.body.querySelector(".console_btn_other");

  if (message.classList.contains("custom_color")) {
    message.classList.remove("custom_color", "target_message");
    for (var i = 0; i < list.length; i++){
      if (list[i].classList.contains("custom_color")) {
        is_toggle = true
      }
    };
    is_toggle ? show_chat_console(message) : hide_chat_console();

  } else {
    // сообщение не выбрано
    message.classList.add("custom_color", "target_message");
    show_chat_console(message)
  };

  if (get_toggle_messages().length > 1) {
    btn_console.querySelector(".one_message").style.display = "none"
  } else {
    btn_console.querySelector(".one_message").style.display = "unset"
  }
}});

on('#ajax', 'click', '.u_message_delete', function() {
  list = get_toggle_messages();
  for (var i = 0; i < list.length; i++){
    list[i].classList.remove("custom_color", "target_message");
    remove_item_and_show_restore_block(list[i], "/chat/user_progs/delete_message/", "u_message_restore", "Сообщение удалено")
  };
  hide_chat_console()
});

on('#ajax', 'click', '.remove_parent_block', function() {
  form = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  setTimeout(function(){
    send_draft_message (form, "/chat/user_progs/save_draft_message/" + form.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/");
}, 1000)
  this.parentElement.parentElement.parentElement.remove()
});

on('#ajax', 'click', '.u_message_restore', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-pk");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/restore_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    item.style.display = "flex";
    item.classList.remove("custom_color")
  }};
  link.send();
});

on('#ajax', 'click', '.edit_message_form_remove', function() {
  box = this.parentElement.parentElement;
  box.innerHTML = "";
  box.previousElementSibling.style.display = "flex"
});

on('#ajax', 'change', '#u_photo_message_attach', function() {
  if (this.files.length > 10) {
      toast_error("Не больше 10 фотографий");return
  }
  form_data = new FormData(this.parentElement);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/chat/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
      elem = link_.responseText;
      response = document.createElement("span");
      response.innerHTML = elem;
      photo_list = response.querySelectorAll(".pag");
      photo_message_upload_attach(photo_list, document.body.querySelector(".message_attach_block"));
    };
    close_work_fullscreen();
    show_message_form_send_btn();
  }
  link_.send(form_data);
});

on('#ajax', 'click', '.edit_message_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  _text = form_post.querySelector(".message_text").innerHTML;
  if (_text.replace(/<(?!br)(?!img)\/?[a-z][^>]*(>|$)/gi, "").trim() == "" && !form_post.querySelector(".special_block").innerHTML){
    toast_error("Напишите или прикрепите что-нибудь");
    form_post.querySelector(".message_text").classList.add("border_red");
    form_post.querySelector(".message_dropdown").classList.add("border_red");
    return
  };

  text = form_post.querySelector(".type_hidden");
  text.value = form_post.querySelector(".message_text").innerHTML.replace("data:image", '');
  form_data = new FormData(form_post);
  message = form_post.parentElement.previousElementSibling;

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/chat/user_progs/edit_message/" + message.getAttribute("data-uuid") + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    message.innerHTML = new_post.innerHTML;
    form_post.parentElement.innerHTML = "";
    message.style.display = "flex"
  }};

  link_.send(form_data);
});


on('#ajax', 'click', '.u_message_transfer', function() {
  create_fullscreen('/users/load/chats/', "item_fullscreen");
  hide_chat_console();
});

on('#ajax', 'click', '.go_transfer_messages', function() {
  url = "/chat/" + this.getAttribute("data-pk") + "/";
  list = get_toggle_messages();
  get_document_opacity_1();
  saver = document.createElement("div");
  for (var i = 0; i < list.length; i++) {
    $input = document.createElement("input");
    $input.setAttribute("type", "hidden");
    $input.setAttribute("name", "transfer");
    $input.setAttribute("value", list[i].getAttribute("data-uuid"));
    $input.classList.add("transfer");
    saver.append($input)
  };

  if (list.length > 1) {
    count = list.length
    a = count % 10, b = count % 100;
    if (a == 1 && b != 11){
      preview = "<span class='pointer underline'>" + count + " сообщение</span>"
    }
    else if (a >= 2 && a <= 4 && (b < 10 || b >= 20)) {
      preview = "<span class='pointer underline'>" + count + " сообщения</span>"
    }
    else {
      preview = "<span class='pointer underline'>" + count + " сообщений</span>"
    };
    creator_p = '<p>Пересланные сообщения</p>'
  } else {
    message = document.body.querySelector(".target_message");
    if (message.querySelector(".attach_container")) {
      preview = "Вложения"
    } else if (message.querySelector(".text") != null) {
      text = message.querySelector(".text").innerHTML;
      preview = text.replace(/[<]br[^>]*[>]/gi, " ");
    } else if(message.querySelector(".message_sticker")) {
        preview = "Наклейка"
    };
    creator_p = '<p><a class="underline" target="_blank" href="' + message.querySelector(".creator_link").getAttribute("href") + '">' + message.querySelector(".creator_name").innerHTML + '</a></p>'
  };
  if (url == window.location.href) {
    block = rtr.querySelector(".parent_message_block");
    block.innerHTML = "<div>" + creator_p + "<div style='position:relative;padding-bottom:7px'><div>" + preview + "<span class='remove_parent_block message_form_parent_block pointer'>x</span></div></div></div>";
    block.append(saver);
  } else {
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
      objDiv = document.querySelector(".chat_container");
      objDiv.scrollTop = objDiv.scrollHeight;
      window.history.pushState(null, "vfgffgfgf", url);
      scrolled(rtr.querySelector('.chat_container'));
      block = rtr.querySelector(".parent_message_block");
      block.innerHTML = "<div>" + creator_p + "<div style='position:relative;padding-bottom:7px'><div style='overflow: hidden;text-overflow:ellipsis;padding-right:5px;'><span style='white-space: nowrap;'>" + preview + "</span><span class='remove_parent_block pointer message_form_parent_block'>x</span></div></div></div>";
      block.append(saver);
      show_message_form_send_btn();
    }
  }
  ajax_link.send();
};
setTimeout(function(){
  form = document.body.querySelector(".customize_form");
    send_draft_message (form, "/chat/user_progs/save_draft_message/" + form.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/");
}, 1000)
});

on('#ajax', 'click', '.on_full_chat_notify', function() {
  document.body.querySelector(".notify_box").innerHTML= ''
  chat_send_change(this, "/chat/user_progs/beep_on/", "off_full_chat_notify", "Откл. уведомления");
});
on('#ajax', 'click', '.off_full_chat_notify', function() {
  document.body.querySelector(".notify_box").innerHTML= ' <svg style="width: 14px;" enable-background="new 0 0 24 24" height="14px" viewBox="0 0 24 24" width="17px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M4.34 2.93L2.93 4.34 7.29 8.7 7 9H3v6h4l5 5v-6.59l4.18 4.18c-.65.49-1.38.88-2.18 1.11v2.06c1.34-.3 2.57-.92 3.61-1.75l2.05 2.05 1.41-1.41L4.34 2.93zM10 15.17L7.83 13H5v-2h2.83l.88-.88L10 11.41v3.76zM19 12c0 .82-.15 1.61-.41 2.34l1.53 1.53c.56-1.17.88-2.48.88-3.87 0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zm-7-8l-1.88 1.88L12 7.76zm4.5 8c0-1.77-1.02-3.29-2.5-4.03v1.79l2.48 2.48c.01-.08.02-.16.02-.24z"/></svg>'
  chat_send_change(this, "/chat/user_progs/beep_off/", "on_full_chat_notify", "Вкл. уведомления");
});

on('#ajax', 'click', '.remove_user_from_chat', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/" + item.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/remove_member/" + user_pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    item.remove()
  }};
  link.send();
});
on('#ajax', 'click', '.user_exit_in_user_chat', function() {
  if (this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")){
    pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk");
  } else { pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")}
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/exit_user_from_user_chat/" + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    ajax_get_reload("/chat/");
  }};
  link.send();
});
on('#ajax', 'click', '.u_clean_chat_messages', function() {
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/clean_messages/" + this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    ajax_get_reload("/chat/");
  }};
  link.send();
});

on('body', 'click', '.add_perm_user_chat', function() {
  _this = this;
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/" + item.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/add_admin/" + user_pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.classList.remove("add_perm_user_chat");
    _this.classList.add("remove_perm_user_chat");
    _this.innerHTML = "Расжаловать";
    item.querySelector('.member_role').innerHTML = "Администратор"
  }};
  link.send();
});
on('body', 'click', '.remove_perm_user_chat', function() {
  _this = this;
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/" + item.parentElement.parentElement.parentElement.getAttribute("chat-pk") + "/remove_admin/" + user_pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.classList.remove("remove_perm_user_chat");
    _this.classList.add("add_perm_user_chat");
    _this.innerHTML = "Сделать админом";
    item.querySelector('.member_role').innerHTML = "Участник"
  }};
  link.send();
});

on('#ajax', 'click', '#u_chat_settings_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  pk = form.getAttribute("data-pk");
  form_data = new FormData(form);
  this.disabled = true;

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/chat/user_progs/edit/' + pk + '/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            form.classList.remove("cool_private_form");
            close_work_fullscreen();
        }
      };
      ajax_link.send(form_data);
});

on('#ajax', 'click', '#add_chat_exclude_users_btn', function() {
  form = this.parentElement.parentElement;
  post_include_exclude_users(form, '/chat/user_progs/load_exclude_users/' + form.parentElement.getAttribute("chat-pk") + '/')
});
on('#ajax', 'click', '#add_chat_include_users_btn', function() {
  form = this.parentElement.parentElement;
  post_include_exclude_users(form, '/chat/user_progs/load_include_users/' + form.parentElement.getAttribute("chat-pk") + '/')
});


on('#ajax', 'click', '.u_add_members_in_chat', function() {
  if (this.getAttribute("chat-pk")) {
    pk = this.getAttribute("chat-pk")
  } else if (this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")){
    pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("chat-pk")
  } else {pk=null};
  create_fullscreen("/chat/user_progs/invite_members/?chat_pk=" + pk, "worker_fullscreen");
});
on('#ajax', 'click', '#append_friends_to_chat_btn', function() {
  form = this.parentElement.parentElement, is_chat = false;
  this.disabled = true;
  if (form.parentElement.getAttribute("chat-pk")) {
    pk = form.parentElement.getAttribute("chat-pk");
    is_chat = true
  } else { pk=null};

  if (is_chat) {
    form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', "/chat/user_progs/invite_members/?chat_pk=" + pk, true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            message_load = document.body.querySelector(".chatlist");
            message_load.append(elem_);
            objDiv = document.querySelector("#chatcontent");
            objDiv.scrollTop = objDiv.scrollHeight;
            close_work_fullscreen();
            message_load.querySelector(".items_empty") ? message_load.querySelector(".items_empty").style.display = "none" : null;
        }
      };
      ajax_link.send(form_data);
    } else {
      users_block = form.querySelector(".card-header");
      users_list = users_block.querySelectorAll(".custom_color");
      collector = document.body.querySelector(".collector");
      final_list = "Выбраны друзья: ";
      for (var i = 0; i < users_list.length; i++){
        a = users_list[i].querySelector("a");
        final_list += '<a href="' + a.getAttribute("href") + '" target="_blank">' + a.innerHTML + '</a>'
        final_list += '<input type="hidden" name="users" value="' + users_list[i].getAttribute("data-pk") + '" />'
      };
      collector.innerHTML = final_list;
      close_work_fullscreen();
    }
});