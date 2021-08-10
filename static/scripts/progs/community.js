on('body', 'click', '.community_like', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_like(item, "/communities/votes/like/" + pk + "/");
});
on('body', 'click', '.community_dislike', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_dislike(item, "/communities/votes/dislike/" + pk + "/");
});
on('body', 'click', '.community_inert', function() {
  item = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = item.getAttribute("data-pk");
  send_inert(item, "/communities/votes/inert/" + pk + "/");
});
