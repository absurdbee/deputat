function clear_comment_dropdown(){
  try{
  dropdown = document.body.querySelector(".file_dropdown");
  btn = dropdown.parentElement.parentElement;
  btn.classList.remove("files_two");
  btn.classList.remove("files_one");
  btn.classList.add("files_null");
  btn.style.display = "block";
  dropdown.classList.remove("file_dropdown");
  } catch { null }
  try{
  files_block = document.body.querySelector(".files_block");
    files_block.innerHTML = "";
  } catch { null }
}

function is_full_dropdown(){
  dropdown = document.body.querySelector(".file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_two")){
    dropdown.style.display = "none";
    close_window()
  };
  if (dropdown.classList.contains("files_one") || dropdown.classList.contains("files_null")){
    dropdown.style.display = "block"}
}
function add_file_dropdown(){
  dropdown = document.body.querySelector(".file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_null")){
    dropdown.classList.add("files_one"),
    dropdown.classList.remove("files_null")}
  else if(dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_two"), dropdown.classList.remove("files_one")};
}
function remove_file_dropdown(){
  dropdown = document.body.querySelector(".file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_null"), dropdown.classList.remove("files_one")}
  else if(dropdown.classList.contains("files_two")){
    dropdown.classList.add("files_one"), dropdown.classList.remove("files_two")};
}
