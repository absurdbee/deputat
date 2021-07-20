function post_elect_new(_this, url, toast) {
  elect = false;
  form = _this.parentElement.parentElement.parentElement;
  elect_value = form.querySelector("#id_elect").value;
  form_data = new FormData(form);

  xxx = form.querySelector("#data-list");
  elect_list = xxx.querySelectorAll("option");
  for (var i = 0; i < elect_list.length; i++){
    if (elect_value == elect_list[i].value) {
      elect = true;
    }
  };

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  } else if (!elect_value){
    form.querySelector("#id_elect").style.border = "1px #FF0000 solid";
    toast_error("Выберите чиновника!"); return
  } else if (!elect){
    form.querySelector("#id_elect").style.border = "1px #FF0000 solid";
    toast_error("Выберите чиновника из списка!"); return
  } else { _this.disabled = true };

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'POST', url, true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    elem = link.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    close_default_window();
    document.body.querySelector("#ajax").innerHTML = response.querySelector("#ajax").innerHTML;
    toast_info(toast)
  }};
  link.send(form_data);
};

on('body', 'click', '.manager_blog_create', function(e) {
  e.preventDefault();
  loader = document.body.querySelector("#window_loader");
  open_fullscreen("/blog/progs/add_blog/", loader)
});

on('body', 'click', '.manager_elect_new_create', function() {
  loader = document.body.querySelector("#window_loader");
  open_fullscreen("/managers/elect_new/create_elect_new/", loader)
});

on('body', 'click', '.penalty_photo', function() {
  this.parentElement.parentElement.classList.add("changed");
  pk = this.getAttribute('photo-pk');
  loader = document.body.querySelector("#window_loader");
  open_fullscreen("/gallery/penalty_photo/" + pk + "/", loader)
});
on('body', 'click', '.u_photo_moderated_detail', function() {
  this.parentElement.parentElement.classList.add("changed");
  pk = this.getAttribute('photo-pk');
  loader = document.body.querySelector("#window_loader");
  open_fullscreen("/gallery/moderated_photo/" + pk + "/", loader)
});

on('body', 'click', '.u_publish_elect_new', function() {
  loader = document.body.querySelector("#window_loader");
  open_fullscreen("/managers/elect_new/create_publish/" + this.parentElement.getAttribute("data-pk") + "/", loader)
});

on('body', 'click', '#create_blog_btn', function() {
  _this = this, elect = false;
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);

  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!"); return
  } else if (!form.querySelector("#id_description").value){
    form.querySelector("#id_description").style.border = "1px #FF0000 solid";
    toast_error("Опишите ситуацию!"); return
  }
  else if (!form.querySelector("#id_image").value){
    form.querySelector("#holder_image").style.border = "1px #FF0000 solid";
    toast_error("Загрузите обложку!"); return
  }
  else { _this.disabled = true };

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/blog/progs/add_blog/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Новость создана!")
    close_default_window()
  }};

  link_.send(form_data);
});

on('body', 'click', '#u_publish_elect_new_btn', function() {
  post_elect_new(this, "/managers/elect_new/create_publish/" + this.getAttribute("data-pk") + "/", "Активность опубликована!")
});
on('body', 'click', '#manager_create_elect_new_btn', function() {
  post_elect_new(this, "/managers/elect_new/create_elect_new/", "Активность создана и опубликована!")
});

on('body', 'click', '.show_object_reports', function() {
  if (this.getAttribute("obj-pk")) {
    pk = this.getAttribute("obj-pk")
  } else {
    pk = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute("obj-pk")
  }
  open_fullscreen("/managers/load_claims/" + pk + "/", document.body.querySelector("#window_loader"))
});

on('body', 'click', '.u_load_penalty_playlist', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/music/penalty_load/" + parent.getAttribute("playlist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_penalty_video_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/video/penalty_load/" + parent.getAttribute("videolist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_penalty_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/docs/penalty_load/" + parent.getAttribute("doclist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_penalty_survey_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/survey/penalty_load/" + parent.getAttribute("surveylist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_penalty_photo_list', function() {
  parent = this.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/gallery/penalty_load/" + parent.getAttribute("photolist-pk") + "/", document.body.querySelector("#window_loader"))
});


on('body', 'click', '.u_load_moderated_photo_list', function() {
  parent = this.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/gallery/moderated_load/" + parent.getAttribute("photolist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_moderated_playlist', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/music/moderated_load/" + parent.getAttribute("playlist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_moderated_video_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/video/moderated_load/" + parent.getAttribute("videolist-pk") + "/", document.body.querySelector("#window_loader"))
});
on('body', 'click', '.u_load_moderated_doc_list', function() {
  parent = this.parentElement.parentElement.parentElement;
  parent.parentElement.classList.add("changed");
  open_fullscreen("/docs/moderated_load/" + parent.getAttribute("doclist-pk") + "/", document.body.querySelector("#window_loader"))
});

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
on('body', 'click', '.close_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_close/")
})
on('body', 'click', '.suspend_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_suspension/")
})
on('body', 'click', '.banner_create_user', function() {
  get_item_sanction_window(this, "", "/managers/progs_user/create_warning_banner/")
})
on('body', 'click', '.u_close_photo_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_photo/list_create_close/")
})
on('body', 'click', '.u_close_photo', function() {
  get_item_sanction_window(this, "", "/managers/progs_photo/create_close/")
})
on('body', 'click', '.u_close_playlist', function() {
  get_item_sanction_window(this, "", "/managers/progs_audio/list_create_close/")
})
on('body', 'click', '.u_close_track', function() {
  get_music_doc_sanction_window(this, "", "/managers/progs_audio/create_close/")
})
on('body', 'click', '.u_close_video_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_video/list_create_close/")
})
on('body', 'click', '.u_close_video', function() {
  get_item_sanction_window(this, "", "/managers/progs_video/create_close/")
})
on('body', 'click', '.u_close_survey_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_survey/list_create_close/")
})
on('body', 'click', '.u_close_doc_list', function() {
  get_item_sanction_window(this, "", "/managers/progs_doc/list_create_close/")
})
on('body', 'click', '.u_close_doc', function() {
  get_music_doc_sanction_window(this, "", "/managers/progs_doc/create_close/")
})

on('body', 'click', '#create_blog_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_blog/create_close/", "Новость закрыта")
});
on('body', 'click', '#create_elect_new_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/elect_new/create_close/", "Активность закрыта")
});
on('body', 'click', '#create_photo_List_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_photo/list_create_close/", "Фотоальбом закрыт")
});
on('body', 'click', '#create_photo_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_photo/create_close/", "Фото закрыто")
});
on('body', 'click', '#create_playlist_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_audio/list_create_close/", "Плейлист закрыт")
});
on('body', 'click', '#create_track_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_audio/create_close/", "Аудиозапись закрыта")
});
on('body', 'click', '#create_doc_list_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_doc/list_create_close/", "Список документов закрыт")
});
on('body', 'click', '#create_doc_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_doc/create_close/", "Документ закрыт")
});
on('body', 'click', '#create_video_List_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_video/list_create_close/", "Список видеозаписей закрыт")
});
on('body', 'click', '#create_video_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_video/create_close/", "Видеозапись закрыта")
});
on('body', 'click', '#create_survey_list_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_survey/list_create_close/", "Список опросов закрыт")
});
on('body', 'click', '#create_blog_comment_close_btn', function() {
  send_window_sanction_post(this.parentElement.parentElement.parentElement,"/managers/progs_blog/comment_create_close/", "Комментарий закрыт")
});

on('body', 'click', '.remove_photo_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_delete_close/", "Фотоальбом восстановлен")
});
on('body', 'click', '.photo_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_photo_close', function() {
  send_window_sanction_get(this, "/managers/progs_photo/delete_close/", "Фото восстановлено")
});
on('body', 'click', '.photo_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_photo/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_playlist_close', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_delete_close/", "Плейлист восстановлен")
});
on('body', 'click', '.playlist_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_track_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_audio/delete_close/", "Аудиозапись восстановлена")
});
on('body', 'click', '.track_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_audio/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_video_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_delete_close/", "Видеоальбом восстановлен")
});
on('body', 'click', '.video_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_video_close', function() {
  send_window_sanction_get(this, "/managers/progs_video/delete_close/", "Видеоальбом восстановлен")
});
on('body', 'click', '.video_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_video/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_doc_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_delete_close/", "Список документов восстановлен")
});
on('body', 'click', '.doc_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_doc_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_doc/delete_close/", "Документ восстановлен")
});
on('body', 'click', '.doc_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/progs_doc/unverify/", "Верификация отменена")
});
on('body', 'click', '.remove_elect_new_close', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/elect_new/delete_close/", "Активность восстановлена")
});
on('body', 'click', '.elect_new_unverify', function() {
  clean_body_changed_class();
  send_window_sanction_get(this, "/managers/elect_new/unverify/", "Верификация отменена")
});

on('body', 'click', '.remove_survey_list_close', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_delete_close/", "Список опросов восстановлен")
});
on('body', 'click', '.survey_list_unverify', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_unverify/", "Верификация отменена")
});


on('body', 'click', '.create_photo_list_close', function() {
  open_manager_window(this, "/managers/progs_photo/list_create_close/")
});
on('body', 'click', '.create_photo_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_photo/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_photo_close', function() {
  open_manager_window(this, "/managers/progs_photo/create_close/")
});
on('body', 'click', '.create_photo_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_photo/create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_playlist_close', function() {
  open_manager_window(this, "/managers/progs_audio/list_create_close/")
});
on('body', 'click', '.create_playlist_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_audio/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_track_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_audio/create_close/")
});
on('body', 'click', '.create_track_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_audio/create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.reject_suggested_elect_new', function() {
  send_window_sanction_get(this, "/managers/elect_new/suggest_rejected/", "Активность отклонена")
});

on('body', 'click', '.create_video_list_close', function() {
  open_manager_window(this, "/managers/progs_video/list_create_close/")
});
on('body', 'click', '.create_video_list_rejected', function() {
  send_window_sanction_get(this, this.parentElement.parentElement.parentElement.parentElement.parentElement, "/managers/progs_video/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_video_close', function() {
  open_manager_window(this, "/managers/progs_video/create_close/")
});
on('body', 'click', '.create_video_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_video/list_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_doc_list_close', function() {
  open_manager_window(this, "/managers/progs_doc/list_create_close/")
});
on('body', 'click', '.create_doc_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_doc/list_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_doc_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_doc/create_close/")
});
on('body', 'click', '.create_doc_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_doc/create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_elect_new_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/elect_new/create_close/")
});
on('body', 'click', '.create_elect_new_rejected', function() {
  send_window_sanction_get(this, "/managers/elect_new/create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_elect_new_comment_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/elect_new/comment_create_close/")
});
on('body', 'click', '.create_elect_new_comment_rejected', function() {
  send_window_sanction_get(this, "/managers/elect_new/comment_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_survey_list_close', function() {
  open_manager_window(this, "/managers/progs_survey/list_create_close/")
});
on('body', 'click', '.create_survey_list_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_survey/list_create_rejected/", "Жалобы отклонены")
});

on('body', 'click', '.create_blog_comment_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_blog/comment_create_close/")
});
on('body', 'click', '.create_blog_close', function() {
  clean_body_changed_class();
  open_manager_window(this, "/managers/progs_blog/create_close/")
});
on('body', 'click', '.create_blog_comment_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_blog/comment_create_rejected/", "Жалобы отклонены")
});
on('body', 'click', '.create_blog_rejected', function() {
  send_window_sanction_get(this, "/managers/progs_blog/create_rejected/", "Жалобы отклонены")
});
