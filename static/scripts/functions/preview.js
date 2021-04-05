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
