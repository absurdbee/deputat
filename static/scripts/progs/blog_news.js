on('body', 'click', '.elect_new_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/elect_new_like/" + pk + "/");
});
on('body', 'click', '.elect_new_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/elect_new_dislike/" + pk + "/");
});
on('body', 'click', '.elect_new_comment_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/elect_new_comment_like/" + pk + "/");
});
on('body', 'click', '.elect_new_comment_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/elect_new_comment_dislike/" + pk + "/");
});

on('body', 'click', '.blog_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/blog_like/" + pk + "/");
});
on('body', 'click', '.blog_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/blog_dislike/" + pk + "/");
});
on('body', 'click', '.blog_inert', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_inert(item, "/blog/votes/blog_inert/" + pk + "/");
});
on('body', 'click', '.blog_comment_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/blog/votes/blog_comment_like/" + pk + "/");
});
on('body', 'click', '.blog_comment_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/blog/votes/blog_comment_dislike/" + pk + "/");
});
