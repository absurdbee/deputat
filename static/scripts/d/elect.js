on('body', 'click', '.elect_comment_like', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/elect/votes/elect_comment_like/" + pk + "/");
});
on('body', 'click', '.elect_comment_dislike', function() {
  item = this.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/elect/votes/elect_comment_dislike/" + pk + "/");
});
