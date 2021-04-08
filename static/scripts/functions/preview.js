function check_photo_in_block(block, _this, pk) {
    if (block.querySelector('[photo-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_photo_album_in_block(block, _this, pk) {
    if (block.querySelector('[data-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Альбом уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
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
function check_music_in_block(block, _this, counter) {
    if (block.querySelector('[music-counter=' + '"' + pk + '"' + ']')) {
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

function create_preview_photo(img_src, photo_pk){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "photo");
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="pho' + photo_pk + '">';
  $img = document.createElement("img");
  $img.classList.add("u_preview_photo", "image_fit", "pointer");
  $img.setAttribute("src", img_src);
  $img.setAttribute('photo-pk', photo_pk);
  $div.append(photo_preview_delete());
  $div.append($input);
  $div.append($img);
  return $div
}
function create_preview_photo_album(src, title, pk, count){
  $div = document.createElement("div");
  $div.style.flexBasis = "100%";

  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="lph' + pk + '">';

  $img = document.createElement("img");
  $img.setAttribute("src", src);
  $img.style.objectFit = "cover";
  $img.style.height = "150px";
  $img.style.width = "170px";
  $figure = document.createElement("figure");
  $figure.append($img);

  $p = document.createElement("p");
  $p.innerHTML = 'Фотоальбом<br>Всего: ' + count;
  $h6 = document.createElement("h6");
  $h6.innerHTML = title;
  $h6.classList.add("my-0", "mt-1");
  $media_body = document.createElement("div");
  $media_body.classList.add("media-body");
  $media_body.style.marginLeft = "10px";

  $media_body.append($h6); $media_body.append($p);
  $span = document.createElement("span");
  $span.classList.add("photo_attach_album_remove", "btn_default", "pointer");
  $span.style.marginRight = "14px";
  $span.setAttribute("flow", "up");
  $span.setAttribute("tooltip", "Открепить");
  $span.innerHTML = '<svg class="svg_default svg_default_30" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';

  $card_body = document.createElement("div");
  $card_body.classList.add("card-body");
  $card_body.style.padding = "8px";
  $card_body.style.paddingBottom = "0";

  $flex = document.createElement("div");
  $flex.style.display = "flex";
  $flex.append($input);
  $flex.append($figure);
  $flex.append($media_body);
  $flex.append($span);

  $card_body.append($flex);
  $div.append($card_body);
  return $div
}

function create_preview_video(img_src, pk, counter){
  $div = document.createElement("div");
  $div.classList.add("col-md-4", "video");
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="attach_items" value="vid' + pk + '">';
  $img = document.createElement("img");
  $icon_div = document.createElement("span");
  $img.classList.add("image_fit");
  $img.src = img_src;
  $icon_div.classList.add("video_icon_play_v2", "u_video_list_detail");
  $icon_div.setAttribute("video-counter", counter);
  $icon_div.setAttribute("video-pk", pk);

  $div.append(video_preview_delete());
  $div.append($input);
  $div.append($img);
  $div.append($icon_div);
  return $div
}
function create_preview_music(img_src, pk, counter){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $img = document.createElement("img");
  $figure = document.createElement("figure");
  $media = document.createElement("span");

  media_body = _this.querySelector(".media-body");

  $div.classList.add("col-md-12", "music");
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.style.flexBasis = "100%";
  $div.setAttribute('music-counter', counter);

  $input.innerHTML = '<input type="hidden" name="attach_items" value="mus' + pk + '">';

  $img.src = img_src;
  $img.style.width = "30px";
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;
  $media.style.marginLeft = "10px";
  $media.style.marginRight = "40px";
  $media.style.overflow = "hidden";
  h6 = $media.querySelector("h6");
  h6.classList.add("music_list_item", "pointer", "music_title");

  $div.append(music_preview_delete());
  $div.append($input);
  $div.append($figure);
  $div.append($media);
  return $div
}
function create_preview_doc(media_body, pk){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $span = document.createElement("span");
  $figure = document.createElement("figure");
  $media = document.createElement("span");

  $div.classList.add("col-md-12", "doc");
  $div.setAttribute("data-pk", pk);
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.style.flexBasis = "100%";

  $input.innerHTML = '<input type="hidden" name="attach_items" value="doc' + pk + '">';

  $span.innerHTML = '<svg fill="currentColor" style="width:35px;heigth:35px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>';
  $figure.append($span);

  $media.innerHTML = media_body.innerHTML;
  $media.style.marginLeft = "10px";
  $media.style.marginRight = "40px";
  $media.style.overflow = "hidden";
  h6 = $media.querySelector("h6");
  h6.style.paddingTop = "8px";

  $div.append(doc_preview_delete());
  $div.append($input);
  $div.append($figure);
  $div.append($media);
  return $div
}

on('body', 'click', '.photo_load_one', function() {
  _this = this;
  photo_pk = _this.parentElement.getAttribute('photo-pk');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, src), close_create_window())
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, src), close_create_window())
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, src), close_create_window())
  }
});

on('body', 'click', '.photo_load_several', function() {
  previous = this.previousElementSibling
  _this = previous.querySelector("img");
  photo_pk = previous.getAttribute('photo-pk');
  src = _this.parentElement.getAttribute("data-href");
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, photo_pk) ? null : (photo_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, photo_pk, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".attach_block")){
    check_photo_in_block(document.body.querySelector(".attach_block"), _this, photo_pk) ? null : (photo_post_attach(document.body.querySelector(".attach_block"), photo_pk, src), this.classList.add("active_svg"))
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_in_block(document.body.querySelector(".message_attach_block"), _this, photo_pk) ? null : (photo_message_attach(document.body.querySelector(".message_attach_block"), photo_pk, src), this.classList.add("active_svg"))
  }
});

on('body', 'click', '.photo_attach_album', function() {
  _this = this;
  src = _this.nextElementSibling.querySelector("img").getAttribute("src");
  title = _this.previousElementSibling.innerHTML;
  pk = _this.getAttribute('data-pk');
  count = _this.getAttribute('data-count');
  if (document.body.querySelector(".current_file_dropdown")){
    check_photo_album_in_block(document.body.querySelector(".current_file_dropdown").parentElement.parentElement.parentElement.previousElementSibling, _this, pk) ? null : (photo_album_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, src, title, pk, count), close_create_window())
  } else if (document.body.querySelector(".attach_block")){
    check_photo_album_in_block(document.body.querySelector(".attach_block"), _this, pk) ? null : (photo_album_post_attach(document.body.querySelector(".attach_block"), src, title, pk, count), close_create_window())
  } else if (document.body.querySelector(".message_attach_block")){
    check_photo_album_in_block(document.body.querySelector(".message_attach_block"), _this, pk) ? null : (photo_album_message_attach(document.body.querySelector(".message_attach_block"), src, title, pk, count), close_create_window())
  }
});
