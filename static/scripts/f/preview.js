on('#ajax', 'click', '.file_preview_delete', function() {
  parent = this.parentElement;
  block = parent.parentElement;
  remove_file_dropdown(); is_full_dropdown();
  parent.remove();
});
