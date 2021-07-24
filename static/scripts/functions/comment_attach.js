function clear_comment_dropdown(){
  try{
  dropdowns = document.body.querySelectorAll(".current_file_dropdown");
  for (var i = 0; i < dropdowns.length; i++) {
    btn = dropdowns[i].parentElement.parentElement;
    btn.classList.remove("files_two", "files_one");
    btn.classList.add("files_null");
    btn.style.display = "block";
    dropdowns[i].classList.remove("current_file_dropdown");
  }} catch { null }
  try{
  attach_blocks = document.body.querySelectorAll(".comment_attach_block");
  for (var i = 0; i < attach_blocks.length; i++) {
    attach_blocks[i].innerHTML = "";
  }} catch { null }
}
function check_attach_block_message_post(){
  // удаляем другие активные поля прикрепления - в сообщениях, записях, если они есть.
  // также найдем все активные поля комментов и их деактивируем
  document.body.querySelector(".message_attach_block") ? clear_message_attach_block() :
  document.body.querySelector(".attach_block") ? clear_attach_block() : null
  list = document.body.querySelectorAll('.current_file_dropdown');
  for (var i = 0; i < list.length; i++) {list[i].classList.remove("current_file_dropdown")}
}
function is_full_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_two")){
    dropdown.style.display = "none";
    close_create_window()
  }
  if (dropdown.classList.contains("files_one") || dropdown.classList.contains("files_null")){
    dropdown.style.display = "block"}
}
function add_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_null")){
    dropdown.classList.add("files_one"),
    dropdown.classList.remove("files_null")}
  else if(dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_two"), dropdown.classList.remove("files_one")};
}
function remove_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_null"), dropdown.classList.remove("files_one")}
  else if(dropdown.classList.contains("files_two")){
    dropdown.classList.add("files_one"), dropdown.classList.remove("files_two")};
}

function photo_comment_attach(dropdown, photo_pk, src) {
  is_full_dropdown();
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_photo(src, photo_pk);
  attach_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}
function photo_list_comment_attach(dropdown, src, title, pk, count) {
  is_full_dropdown();
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_photo_list(src, title, pk, count);
  attach_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}
function doc_list_comment_attach(dropdown, title, pk, count) {
  is_full_dropdown();
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_doc_list(title, pk, count);
  attach_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}
function video_list_comment_attach(dropdown, title, pk, count) {
  is_full_dropdown();
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_video_list(title, pk, count);
  attach_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}
function playlist_comment_attach(dropdown, title, pk, count) {
  is_full_dropdown();
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_playlist(title, pk, count);
  attach_block.append(div);
  add_file_dropdown()
  is_full_dropdown();
}

function photo_comment_upload_attach(photo_list, dropdown){
  is_full_dropdown();

  attach_block = dropdown.parentElement.previousElementSibling;
  for (var i = 0; i < photo_list.length; i++){
    div = create_preview_photo(photo_list[i].querySelector(".progressive").getAttribute('data-href'), photo_list[i].getAttribute("photo-pk"));
    attach_block.append(div);
    add_file_dropdown()
    is_full_dropdown();
  }
close_create_window()
}

function video_comment_attach(dropdown, pk, uuid, src){
  is_full_dropdown(dropdown);
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_video(src, pk, uuid)
  attach_block.append($div);
  add_file_dropdown()
  is_full_dropdown();
}

function track_comment_attach(dropdown, _this){
  is_full_dropdown(dropdown);
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_music(_this)
  add_file_dropdown();
  attach_block.append(div)
  is_full_dropdown();
}
function doc_comment_attach(dropdown, media_block, pk){
  is_full_dropdown(dropdown);
  attach_block = dropdown.parentElement.previousElementSibling;
  div = create_preview_doc(media_block, pk)
  add_file_dropdown();
  attach_block.append(div)
  is_full_dropdown();
}
