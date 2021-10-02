function check_photo_in_block(block, _this, pk) {
    if (block.querySelector('[photo-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_photo_list_in_block(block, _this, pk) {
    if (block.querySelector('[photolist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Альбом уже прикреплён")
        return true
    } else {
        return false
    }
}
function check_video_in_block(block, _this, pk) {
    if (block.querySelector('[video-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_track_in_block(block, _this, counter) {
    if (block.querySelector('[data-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.setAttribute("tooltip", "Аудиозапись уже выбрана");
        _this.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_doc_in_block(block, _this, pk) {
    if (block.querySelector('[doc-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Документ уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_doc_list_in_block(block, _this, pk) {
    if (block.querySelector('[doclist-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Список уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_video_list_in_block(block, _this, pk) {
    if (block.querySelector('[videolist-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Список уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_playlist_in_block(block, _this, pk) {
    if (block.querySelector('[playlist-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Плейлист уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}

function photo_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("photo_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}

function video_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("video_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function music_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("music_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}
function doc_preview_delete(){
  $span = document.createElement("span");
  $span.classList.add("doc_preview_delete");
  $span.innerHTML = '<svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  return $span
}

function create_preview_photo(img_src, photo_pk, uuid){
  $div = document.createElement("div");
  $div.classList.add("row_item");

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="pho' + photo_pk + '">';
  $img = document.createElement("img");
  $img.classList.add("u_photo_preview", "image_fit", "pointer");
  $img.setAttribute("src", img_src);
  $img.setAttribute('photo-pk', photo_pk);
  $img.setAttribute('data-uuid', uuid);

  $div.append(photo_preview_delete());
  $div.append($input);
  $div.append($img);
  return $div
}
function create_preview_photo_list(src, title, pk, count){
  $div = document.createElement("div");
  $div.classList.add("col-sm-6", "col-md-4", "bg-dark", "position-relative", "text-center", "big_mobile_element", "col-md-6");
  $div.setAttribute("photolist-pk", pk);

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="lph' + pk + '">';

  $img = document.createElement("img");
  $img.setAttribute("src", src);

  $figure = document.createElement("figure");
  $figure.classList.add("background-img");
  $figure.append($img);

  $h6 = document.createElement("h6");
  $h6.innerHTML = title;
  $h6.classList.add("u_load_photo_list", "text-white", "pointer", "mb-2", "nowrap");

  $span = document.createElement("span");
  $span.classList.add("photo_attach_list_remove", "underline", "pointer", "text-white");
  $span.innerHTML = "Открепить";

  $hr = document.createElement("hr");
  $hr.classList.add("my-3");

  $a = document.createElement("a");
  $a.classList.add("u_load_photo_list", "pointer", "text-white");
  $a.innerHTML = count;

  $container = document.createElement("div");
  $container.classList.add("container", "p-3");

  $container.append($h6);
  $container.append($span);
  $container.append($hr);
  $container.append($a);

  $div.append($figure); $div.append($container); $div.append($input);
  return $div
}

function create_preview_video(img_src, pk, uuid){
  $div = document.createElement("div");
  $div.classList.add("row_item");
  $div.setAttribute("data-uuid", uuid);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="vid' + pk + '">';
  $img = document.createElement("img");
  $icon_div = document.createElement("span");
  $img.classList.add("image_fit");
  $img.src = img_src;
  $icon_div.classList.add("video_icon_play_v2", "u_video_detail");
  $icon_div.setAttribute("video-pk", pk);

  $div.append(video_preview_delete());
  $div.append($input);
  $div.append($img);
  $div.append($icon_div);
  return $div
}
function create_preview_music(_this){
  $div = document.createElement("div");
  $div.classList.add("border");
  $div.style.position = "relative";
  $div.style.width = "100%";
  $div.style.padding = "10px";
  $div.style.paddingRight = "35px";
  $div.style.marginBottom = "7px";
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="mus' + _this.getAttribute("data-pk") + '">';

  $mediaBody = document.createElement("div");
  $mediaBody.classList.add("media-body", "music_media_body");
  $mediaBody.style.lineHeight = "7px";

  $title = document.createElement("span");
  $title.innerHTML = _this.querySelector(".title").innerHTML;

  $audio = document.createElement("audio");
  $audio.classList.add("audio_player");
  $audio.innerHTML = _this.querySelector(".audio_player").innerHTML;

  $mediaBody.append($title);
  $mediaBody.append($audio);

  $div.append(music_preview_delete());
  $div.append($input);
  $div.append($mediaBody);
  return $div
}
function create_preview_doc(media_body, pk){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $span = document.createElement("span");
  $media = document.createElement("span");
  $span2 = document.createElement("span");

  $div.classList.add("col-md-6", "col-sm-12");
  $div.setAttribute("doc-pk", pk);
  $div.style.padding = "3px";
  $div.style.display = "flex";

  $input.innerHTML = '<input type="hidden" name="attach_items" value="doc' + pk + '">';
  $span.innerHTML = '<svg fill="currentColor" style="width:35px;heigth:35px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>';
  $span2.append($span);

  $media.innerHTML = media_body.innerHTML;
  $media.classList.add("media_title");
  h6 = $media.querySelector("h6");
  h6.style.paddingTop = "9px";

  $div.append(doc_preview_delete());
  $div.append($input);
  $div.append($span2);
  $div.append($media);
  return $div
}
function create_preview_doc_list(name, pk, count){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", "col-sm-12", "folder");
  $div.style.textAlign = "center";
  $div.setAttribute("doclist-pk", pk);

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="ldo' + pk + '">';

  $div_svg = document.createElement("div");
  $div_svg.classList.add("card-img-top", "file-logo-wrapper");
  $div_svg.style.padding = "2rem";
  $div_svg.innerHTML = '<a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100 u_load_doc_list pointer"><svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-folder"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg></div></a>'

  $card_body = document.createElement("div");
  $card_body.classList.add("card-body", "pt-0");
  $card_body.innerHTML = '<div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_doc_list pointer"><a class="nowrap">' + name + ' (' + count + ')</a></p></div><small class="file-accessed pointer doc_attach_list_remove underline">Открепить</small>'

  $div.append($input);
  $div.append($div_svg);
  $div.append($card_body);
  return $div
}
function create_preview_video_list(name, pk, count){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", "col-sm-12", "folder");
  $div.style.textAlign = "center";
  $div.setAttribute("videolist-pk", pk);

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="lvi' + pk + '">';

  $div_svg = document.createElement("div");
  $div_svg.classList.add("card-img-top", "file-logo-wrapper");
  $div_svg.style.padding = "2rem";
  $div_svg.innerHTML = '<a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100"><svg class="list_toggle list_svg" width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-video"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg></div></a>'

  $card_body = document.createElement("div");
  $card_body.classList.add("card-body", "pt-0");
  $card_body.innerHTML = '<div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_video_list pointer"><a class="nowrap">' + name + ' (' + count + ')</a></p></div><small class="file-accessed pointer video_attach_list_remove underline">Открепить</small>'

  $div.append($input);
  $div.append($div_svg);
  $div.append($card_body);
  return $div
}
function create_preview_playlist(name, pk, count){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", "col-sm-12", "folder");
  $div.style.textAlign = "center";
  $div.setAttribute("playlist-pk", pk);

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="lmu' + pk + '">';

  $div_svg = document.createElement("div");
  $div_svg.classList.add("card-img-top", "file-logo-wrapper");
  $div_svg.style.padding = "2rem";
  $div_svg.innerHTML = '<a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100 u_load_playlist pointer"><svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div></a>'

  $card_body = document.createElement("div");
  $card_body.classList.add("card-body", "pt-0");
  $card_body.innerHTML = '<div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_playlist pointer"><a class="nowrap">' + name + ' (' + count + ')</a></p></div><small class="file-accessed pointer doc_attach_list_remove underline">Открепить</small>'

  $div.append($input);
  $div.append($div_svg);
  $div.append($card_body);
  return $div
}

on('body', 'click', '.photo_load_one', function() {
  _this = this;
  photo_pk = _this.parentElement.getAttribute('photo-pk');
  uuid = _this.parentElement.getAttribute('list-uuid');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, uuid, src), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, uuid, src), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, uuid, src), close_fullscreen())
  }
});

on('body', 'click', '.photo_load_several', function() {
  previous = this.previousElementSibling
  _this = previous.querySelector("img");
  photo_pk = previous.getAttribute('photo-pk');
  uuid = _this.parentElement.getAttribute('list-uuid');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, uuid, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, uuid, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, uuid, src), this.classList.add("active_svg"))
  }
});

on('body', 'click', '.doc_load_several', function() {
  _this = this.previousElementSibling;
  pk = _this.getAttribute('data-pk');
  media_block = _this.querySelector(".media-body")
  if (document.body.querySelector(".current_file_dropdown")){
    check_doc_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (doc_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_block, pk), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_doc_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (doc_post_attach(document.body.querySelector(".attach_block"), media_block, pk), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_doc_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (doc_message_attach(document.body.querySelector(".message_attach_block"), media_block, pk), this.classList.add("active_svg"))
  }
});
on('body', 'click', '.track_load_several', function() {
  _this = this.previousElementSibling;
  pk = _this.getAttribute('data-pk');
  if (document.body.querySelector(".current_file_dropdown")){
    check_track_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (track_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, _this), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_track_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (track_post_attach(document.body.querySelector(".attach_block"), _this), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_track_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (track_message_attach(document.body.querySelector(".message_attach_block"), _this), this.classList.add("active_svg"))
  }
});
on('body', 'click', '.doc_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_doc_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (doc_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_doc_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (doc_list_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_doc_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (doc_list_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_fullscreen())
  }
});
on('body', 'click', '.video_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_video_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_list_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_list_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_fullscreen())
  }
});
on('body', 'click', '.music_attach_list', function() {
  _this = this;
  name = _this.parentElement.querySelector(".list_name").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_playlist_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (playlist_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_playlist_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (playlist_post_attach(document.body.querySelector(".attach_block"), name, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_playlist_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (playlist_message_attach(document.body.querySelector(".message_attach_block"), name, pk, count), close_fullscreen())
  }
});

on('body', 'click', '.video_load_one', function() {
  _this = this;
  pk = _this.getAttribute('video-pk');
  uuid = _this.getAttribute('list-pk');
  src = _this.getAttribute('src');
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, uuid, src), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_video_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_post_attach(document.body.querySelector(".attach_block"), pk, uuid, src), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_message_attach(document.body.querySelector(".message_attach_block"), pk, uuid, src), close_fullscreen())
  }
});
on('body', 'click', '.video_load_several', function() {
  previous = this.previousElementSibling
  _this = previous.querySelector("img");
  pk = _this.getAttribute('video-pk');
  uuid = _this.getAttribute('list-pk');
  src = _this.getAttribute('src');
  if (document.body.querySelector(".current_file_dropdown")){
    check_video_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (video_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, pk, uuid, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_video_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (video_post_attach(document.body.querySelector(".attach_block"), pk, uuid, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_video_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (video_message_attach(document.body.querySelector(".message_attach_block"), pk, uuid, src), this.classList.add("active_svg"))
  }
});

on('body', 'click', '.photo_attach_list', function() {
  _this = this;
  src = _this.parentElement.previousElementSibling.querySelector("img").getAttribute("src");
  title = _this.parentElement.querySelector(".nowrap").innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.parentElement.querySelector(".count").innerHTML;
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_list_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (photo_list_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, src, title, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".attach_block")){
    check_photo_list_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (photo_list_post_attach(document.body.querySelector(".attach_block"), src, title, pk, count), close_fullscreen())
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_list_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (photo_list_message_attach(document.body.querySelector(".message_attach_block"), src, title, pk, count), close_fullscreen())
  }
});
