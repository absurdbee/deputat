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
  this.classList.add("current_file_dropdown");
  document.body.querySelector(".attach_block") ? (
      attach_block = document.body.querySelector(".attach_block"),
      attach_block.innerHTML = "",
      attach_block.classList.remove("attach_block")) : null;
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/img_comment_load/', loader)
});
