on('#ajax', 'click', '.blogComment', function() {
  form = this.parentElement.parentElement;
  send_comment(form, form.parentElement.parentElement.parentElement.nextElementSibling, '/blog/blog_comment/', "prepend");
});

on('#ajax', 'click', '.blogReplyComment', function() {
  form = this.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.nextElementSibling.nextElementSibling;
  send_comment(form, block, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("show");
});

on('#ajax', 'click', '.blogReplyParentComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/blog/blog_reply/', "append")
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.u_comment_photo', function() {
  clear_comment_dropdown();
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/u_img_comment_load/', loader)
});

on('body', 'change', '#u_photo_comment_attach', function() {
  if (this.files.length > 2) {
      toast_error("Не больше 2 фотографий");return
  }
  form = this.parentElement;
  form_data = new FormData(form);

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user_progs/add_attach_photo/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".col-md-4");
    photo_comment_upload_attach(photo_list, document.body.querySelector(".current_file_dropdown").parentElement.parentElement
    );
    }
    close_create_window();
  }
  link_.send(form_data);
});
