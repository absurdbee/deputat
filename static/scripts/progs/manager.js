
on('body', 'click', '.create_user_close', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_close/")
})
on('body', 'click', '.create_user_warning_banner', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_warning_banner/")
})
on('body', 'click', '.create_user_suspend', function() {
  get_profile_sanction_window(this, "/managers/progs_user/create_suspension/")
})

on('body', 'click', '.create_user_blocker_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_close/", "create_user_close", "remove_user_close", "Аккаунт блокирован")
});
on('body', 'click', '.create_user_warning_banner_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_warning_banner/", "create_user_warning_banner", "remove_user_warning_banner", "Баннер применен")
});
on('body', 'click', '.create_user_suspend_btn', function() {
  parent = this.parentElement.parentElement.parentElement;
  send_user_sanction(this, parent, "/managers/progs_user/create_suspension/", "create_user_suspend", "remove_user_suspend", "Аккаунт заморожен")
});

on('body', 'click', '.user_unverify', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("user-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/unverify/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});

on('body', 'click', '.remove_user_close', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = item.getAttribute("user-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/delete_close/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});

on('body', 'click', '.create_user_rejected', function() {
  item = this.parentElement.parentElement.parentElement.parentElement;
  user_pk = this.parentElement.getAttribute("data-pk");
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', "/managers/progs_user/create_rejected/" + user_pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Верификация отменена!");
    item.remove();
  }};

  link_.send();
});


//////////////////////////// CLOSE ////////////////////

on('body', 'click', '.u_close_photo_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_photo/list_create_close/")
})
on('body', 'click', '.u_close_playlist', function() {
  get_item_sanction_window(this, "", "/managers/progs_audio/list_create_close/")
})
on('body', 'click', '.u_close_video_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_video/list_create_close/")
})
on('body', 'click', '.u_close_survey_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_survey/list_create_close/")
})
on('body', 'click', '.u_close_doc_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_doc/list_create_close/")
})

on('body', 'click', '#create_photo_List_close_btn', function() {
  send_item_sanction(this, this.parentElement.parentElement.parentElement, "/managers/progs_photo/list_create_close/", "u_unclose_photo_list", "u_close_photo_list", "Фотоальбом закрыт")
});
on('body', 'click', '#create_playList_close_btn', function() {
  send_item_sanction(this, this.parentElement.parentElement.parentElement, "/managers/progs_audio/list_create_close/", "u_unclose_playList", "u_close_playList", "Плейлист закрыт")
});
on('body', 'click', '#create_doc_List_close_btn', function() {
  send_item_sanction(this, this.parentElement.parentElement.parentElement, "/managers/progs_doc/list_create_close/", "u_unclose_doc_List", "u_close_doc_List", "Список документов закрыт")
});
on('body', 'click', '#create_video_List_close_btn', function() {
  send_item_sanction(this, this.parentElement.parentElement.parentElement, "/managers/progs_video/list_create_close/", "u_unclose_video_List", "u_close_video_List", "Список видеозаписей закрыт")
});
on('body', 'click', '#create_survey_List_close_btn', function() {
  send_item_sanction(this, this.parentElement.parentElement.parentElement, "/managers/progs_survey/list_create_close/", "u_unclose_survey_List", "u_close_survey_List", "Список опросов закрыт")
});

on('body', 'click', '.u_unclose_photo_list', function() {
  on_off_list_in_collections(this, "/managers/progs_photo/list_delete_close/", "u_close_photo_list", "u_unclose_photo_list", "♦ Закрыть список")
});
