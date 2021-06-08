function clear_attach_block(){
  if (document.body.querySelector(".attach_block")){
    a_b = document.body.querySelector(".attach_block"),
    a_b.innerHTML = "";
    a_b.classList = "";
    a_b.classList.add("files_0");
  }
}

function is_full_attach(){
  files_block = document.body.querySelector(".attach_block");
  if (files_block.classList.contains("files_10")){
    files_block.parentElement.querySelector(".attach_panel").style.display = "none";
    close_create_window()
  }
  else {
    files_block.parentElement.querySelector(".attach_panel").style.display = "block"
}
}
function add_file_attach(){
  files_block = document.body.querySelector(".attach_block");
  if (files_block.classList.contains("files_0")){ files_block.classList.add("files_1"), files_block.classList.remove("files_0")}
  else if (files_block.classList.contains("files_1")){ files_block.classList.add("files_2"), files_block.classList.remove("files_1")}
  else if (files_block.classList.contains("files_2")){ files_block.classList.add("files_3"), files_block.classList.remove("files_2")}
  else if (files_block.classList.contains("files_3")){ files_block.classList.add("files_4"), files_block.classList.remove("files_3")}
  else if (files_block.classList.contains("files_4")){ files_block.classList.add("files_5"), files_block.classList.remove("files_4")}
  else if (files_block.classList.contains("files_5")){ files_block.classList.add("files_6"), files_block.classList.remove("files_5")}
  else if (files_block.classList.contains("files_6")){ files_block.classList.add("files_7"), files_block.classList.remove("files_6")}
  else if (files_block.classList.contains("files_7")){ files_block.classList.add("files_8"), files_block.classList.remove("files_7")}
  else if (files_block.classList.contains("files_8")){ files_block.classList.add("files_9"), files_block.classList.remove("files_8")}
  else if (files_block.classList.contains("files_9")){ files_block.classList.add("files_10"), files_block.classList.remove("files_9")}
}
function remove_file_attach(){
  files_block = document.body.querySelector(".attach_block");
  if (files_block.classList.contains("files_1")){ files_block.classList.add("files_0"), files_block.classList.remove("files_1")}
  else if (files_block.classList.contains("files_2")){ files_block.classList.add("files_1"), files_block.classList.remove("files_2")}
  else if (files_block.classList.contains("files_3")){ files_block.classList.add("files_2"), files_block.classList.remove("files_3")}
  else if (files_block.classList.contains("files_4")){ files_block.classList.add("files_3"), files_block.classList.remove("files_4")}
  else if (files_block.classList.contains("files_5")){ files_block.classList.add("files_4"), files_block.classList.remove("files_5")}
  else if (files_block.classList.contains("files_6")){ files_block.classList.add("files_5"), files_block.classList.remove("files_6")}
  else if (files_block.classList.contains("files_7")){ files_block.classList.add("files_6"), files_block.classList.remove("files_7")}
  else if (files_block.classList.contains("files_8")){ files_block.classList.add("files_7"), files_block.classList.remove("files_8")}
  else if (files_block.classList.contains("files_9")){ files_block.classList.add("files_8"), files_block.classList.remove("files_9")}
  else if (files_block.classList.contains("files_10")){ files_block.classList.add("files_9"), files_block.classList.remove("files_10")}
}

function photo_post_attach(block, photo_pk, src) {
  is_full_attach();
  div = create_preview_photo(src, photo_pk)
  block.append(div);
  add_file_attach()
  is_full_attach();
}

function photo_post_upload_attach(photo_list, block){
  is_full_attach();
  for (var i = 0; i < photo_list.length; i++){
    parent = photo_list[i];
    div = create_preview_photo(parent.getAttribute('data-href'), parent.getAttribute("photo-pk"), parent.getAttribute("data-pk"));
    add_file_attach();
    block.append(div);
    is_full_attach();
  };
  close_create_window()
  }

function video_post_attach(block, pk, src) {
  is_full_attach();
  div = create_preview_video(src, pk)
  block.append(div);
  add_file_attach()
  is_full_attach();
}

function track_post_attach(block, _this) {
  is_full_attach();
  div = create_preview_music(_this)
  block.append(div);
  add_file_attach()
  is_full_attach();
}

function doc_post_attach(block, media_block, pk) {
  is_full_attach();
  div = create_preview_doc(media_block, pk)
  block.append(div);
  add_file_attach()
  is_full_attach();
}

function photo_list_post_attach(block, src, title, pk, count) {
  is_full_attach();
  div = create_preview_photo_list(src, title, pk, count);
  block.append(div);
  add_file_attach()
  is_full_attach();
}
function doc_list_post_attach(block, title, pk, count) {
  is_full_attach();
  div = create_preview_doc_list(title, pk, count);
  block.append(div);
  add_file_attach()
  is_full_attach();
}
function video_list_post_attach(block, title, pk, count) {
  is_full_attach();
  div = create_preview_video_list(title, pk, count);
  block.append(div);
  add_file_attach()
  is_full_attach();
}
function playlist_post_attach(block, title, pk, count) {
  is_full_attach();
  div = create_preview_playlist(title, pk, count);
  block.append(div);
  add_file_attach()
  is_full_attach();
}
