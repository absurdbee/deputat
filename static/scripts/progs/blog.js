on('#ajax', 'click', '.blogComment', function() {
  form = this.parentElement.parentElement.parentElement;
  send_comment(form, form.parentElement.previousElementSibling, '/posts/user_progs/post-comment/');
});

on('#ajax', 'click', '.blogReplyComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.querySelector(".stream_reply_comments");
  send_comment(form, block, '/posts/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});

on('#ajax', 'click', '.blogReplyParentComment', function() {
  form = this.parentElement.parentElement.parentElement.parentElement;
  block = form.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  send_comment(form, block.parentElement, '/posts/user_progs/reply-comment/')
  form.parentElement.style.display = "none";
  block.classList.add("replies_open");
});
