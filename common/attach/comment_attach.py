from django.db.models import Q
query = Q(type="PUB") | Q(type="MAN")
list_query = Q(type="LIS") | Q(type="MAN") | Q(type="MAI")

def get_u_blog_comment_attach(comment, user):
    block = ''
    for item in comment.attach.split(","):
        if item[:3] == "pho":
            try:
                from gallery.models import Photo
                photo = Photo.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div style="position: relative;padding: 5px;"><div class="progressive replace image_fit_200 u_blog_comment_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div style="position: relative;padding: 5px;" data-uuid="', str(video.get_list_uuid()), '"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_video_detail" video-pk="', str(video.pk), '"></div></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(query, pk=item[3:])
                span_btn, lists = '', ''
                if user.is_authenticated:
                    if user.pk == music.creator.pk:
                        options = '<span class="dropdown-item u_track_edit">Изменить</span><span class="dropdown-item u_track_remove">Удалить</span>'
                    elif user.is_manager():
                        options = '<a class="dropdown-item u_close_track pointer">Закрыть</a>'
                    else:
                        options = '<span class="dropdown-item track_claim">Пожаловаться</span>'
                    opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg style="width: 17px;padding-top:3px" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 60px;">' + options + '<span class="dropdown-item copy_link">Копировать ссылку</span></div></div>'
                    for list in user.get_playlists():
                        if list.is_item_in_list(music.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_from_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" data-pk="', str(music.pk), '"><span class="dropdown" style="position: inherit;" data-pk="', str(music.pk), '"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 60px;">', lists, '</div></span>', opt_drop, '</span>'])
                block = ''.join([block, '<div class="col-md-12" style="flex-basis: 100%;"><div class="media border p-1"><div class="media-body music_media_body" style="line-height: 8px;"><span>', music.title, '</span><div class="audio_div"><audio id="player" class="audio_player"><source src="', music.get_uri(), '" type="audio/mp3" /></audio></div>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(query, pk=item[3:])
                span_btn, lists = '', ''
                if user.is_authenticated:
                    if user.pk == doc.creator.pk:
                        options = '<span class="dropdown-item u_doc_edit">Изменить</span><span class="dropdown-item u_doc_remove">Удалить</span>'
                    elif user.is_manager():
                        options = '<a class="dropdown-item u_close_doc pointer">Закрыть</a>'
                    else:
                        options = '<span class="dropdown-item doc_claim">Пожаловаться</span>'
                    opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg class="svg_info" style="padding-top: 3px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">' + options + '<span class="dropdown-item copy_link">Копировать ссылку</span></div></div>'
                    for list in user.get_doc_lists():
                        if list.is_item_in_list(doc.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_doc_from_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_doc_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" data-pk="', str(doc.pk), '"><span class="dropdown" style="position: inherit;" data-pk="', str(doc.pk), '"><span class="btn_default pointer drop" title="Добавить в плейлист"><svg fill="currentColor" style="width:25px;height:25px;margin-top: 2px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">', lists, '</div></span>', opt_drop, '</span>'])
                block = ''.join([block, '<div class="photo" style="flex-basis: 100%;"><div class="media border"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body"><h6 class="pointer" style="padding-top: 5px;width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small" style="bottom: 5px;position: absolute;">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "sur":
            try:
                from survey.models import Survey
                survey = Survey.objects.get(query, pk=item[3:])
                _class, voted, answers, creator = "", "", "", survey.creator
                if survey.is_time_end():
                    time = "<p>Время голосования вышло</p>"
                else:
                    time = "<p>До " + str(survey.time_end) + "</p>"
                    if user.is_authenticated and not survey.is_user_voted(user.pk):
                        _class = " pointer u_survey_vote " + str(survey.is_multiple)
                if survey.image:
                    image = '<img src="' + survey.image.url + '" alt="user image">'
                else:
                    image = ""
                if survey.is_have_votes():
                    voters = '<span class="u_survey_detail pointer">'
                    for user in survey.get_6_users():
                        if user.s_avatar:
                            img = '<img src="' + user.s_avatar.url + '" style="width: 40px;border-radius:40px;" alt="image">'
                        else:
                            img = '<img src="/static/images/no_img/user.jpg" style="width: 40px;border-radius:40px;" alt="image">'
                    voters += '<figure class="staked">' + img + '</figure>'
                else:
                    voters = 'Пока никто не голосовал. Станьте первым!'
                for answer in survey.get_answers():
                    if answer.is_user_voted(user.pk):
                        voted = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>'
                    answers = ''.join([answers, '<div class="lite_color answer_style', _class, '"><div class="progress2" style="width:', str(answer.get_procent()), '%;"></div><span class="progress_span_r">', answer.text, ' - ', str(answer.get_count()), '</span><span class="progress_span_l" style="margin-left: auto;">', voted, str(answer.get_procent()), '%</span></div>'])
                block = ''.join([block, '<div style="flex: 0 0 100%;" survey-pk="', str(survey.pk), '" data-pk="', str(creator.pk), '" class="border text-center has-background-img position-relative box-shadow"><figure class="background-img">', image, '</figure><div class="container" style="list-style-type:none"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none border-bottom"></i><br><h4 class="u_survey_detail pointer">', survey.title, '</h4><a class="underline ajax" href="/users/', creator.pk, '">', str(creator), '</a>', time, '<br>', answers, voters, '</span></div></div>'])
            except:
                pass
        elif item[:3] == "lmu":
            try:
                from music.models import SoundList
                playlist = SoundList.objects.get(list_query, pk=item[3:])
                creator = playlist.creator
                if playlist.image:
                    image = '<img src="' + playlist.image.url + '" style="width:60px;height:88px;" alt="image">'
                else:
                    image = '<svg fill="currentColor" class="svg_default" style="width:70px;height:70px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if playlist.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить плейлист" class="u_add_music_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in playlist.get_users_ids():
                        add_svg = '<span title="Удалить плейлист" class="u_remove_music_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="border"><div class="card-body" playlist-pk="', str(playlist.pk), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_playlist pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_playlist pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(playlist.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список" class="u_add_doc_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список" class="u_remove_doc_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;"><div class="card-body border" doclist-pk="', str(list.pk), '" style="padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Документов: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            try:
                from gallery.models import PhotoList
                list = PhotoList.objects.get(pk=item[3:])
                creator = list.creator
                add = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add = '<a class="col pointer u_add_photo_list text-white">Добавить</a>'
                    elif user.pk in list.get_users_ids():
                        add = '<a class="col pointer u_remove_photo_list text-white">Удалить</a>'
                block = ''.join([block, '<div class="text-center bg-dark position-relative big_mobile_element col-md-6" photolist-pk="', str(list.pk), '"><figure class="background-img"><img src="', list.get_cover_photo(), '">"</figure><div class="container p-3"><h4 class="u_load_photo_list text-white pointer"><a class="nowrap">', list.name, '</a></h4><p><a class="ajax underline text-white nowrap" href="/users/', str(creator.pk), '">', str(list.creator), '</a></p><hr class="my-3"><a class="u_load_photo_list text-white pointer">', list.count_items_ru(), '</a><div class="row">', add, '</div>', '</div></div>'])
            except:
                pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoList
                list = VideoList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список видеозаписей" class="u_add_video_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список видеозаписей" class="u_remove_video_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="border"><div class="card-body" videolist-pk="', str(creator.pk), '" style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_video_list pointer">', list.name, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Видеозаписей: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
    return ''.join(["<div class='items_container'>", block, "</div>"])

def get_u_elect_new_comment_attach(comment, user):
    block = ''
    for item in comment.attach.split(","):
        if item[:3] == "pho":
            try:
                from gallery.models import Photo
                photo = Photo.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div style="position: relative;padding: 5px;"><div class="progressive replace image_fit u_elect_new_comment_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div style="position: relative;padding: 5px;" data-uuid="', str(video.get_list_uuid()), '"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_video_detail" video-pk="', str(video.pk), '"></div></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(query, pk=item[3:])
                span_btn, lists = '', ''
                if user.is_authenticated:
                    if user.pk == music.creator.pk:
                        options = '<span class="dropdown-item u_track_edit">Изменить</span><span class="dropdown-item u_track_remove">Удалить</span>'
                    elif user.is_manager():
                        options = '<a class="dropdown-item u_close_track pointer">Закрыть</a>'
                    else:
                        options = '<span class="dropdown-item track_claim">Пожаловаться</span>'
                    opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg style="width: 17px;padding-top:3px" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 60px;">' + options + '<span class="dropdown-item copy_link">Копировать ссылку</span></div></div>'
                    for list in user.get_playlists():
                        if list.is_item_in_list(music.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_from_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" data-pk="', str(music.pk), '"><span class="dropdown" style="position: inherit;" data-pk="', str(music.pk), '"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 60px;">', lists, '</div></span>', opt_drop, '</span>'])
                block = ''.join([block, '<div class="col-md-12" style="flex-basis: 100%;"><div class="media border p-1"><div class="media-body music_media_body" style="line-height: 8px;"><span>', music.title, '</span><div class="audio_div"><audio id="player" class="audio_player"><source src="', music.get_uri(), '" type="audio/mp3" /></audio></div>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(query, pk=item[3:])
                span_btn, lists = '', ''
                if user.is_authenticated:
                    if user.pk == doc.creator.pk:
                        options = '<span class="dropdown-item u_doc_edit">Изменить</span><span class="dropdown-item u_doc_remove">Удалить</span>'
                    elif user.is_manager():
                        options = '<a class="dropdown-item u_close_doc pointer">Закрыть</a>'
                    else:
                        options = '<span class="dropdown-item doc_claim">Пожаловаться</span>'
                    opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg class="svg_info" style="padding-top: 3px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">' + options + '<span class="dropdown-item copy_link">Копировать ссылку</span></div></div>'
                    for list in user.get_doc_lists():
                        if list.is_item_in_list(doc.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_doc_from_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_doc_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" data-pk="', str(doc.pk), '"><span class="dropdown" style="position: inherit;" data-pk="', str(doc.pk), '"><span class="btn_default pointer drop" title="Добавить в плейлист"><svg fill="currentColor" style="width:25px;height:25px;margin-top: 2px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">', lists, '</div></span>', opt_drop, '</span>'])
                block = ''.join([block, '<div class="photo" style="flex-basis: 100%;"><div class="media border"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body"><h6 class="pointer" style="padding-top: 5px;width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small" style="bottom: 5px;position: absolute;">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "sur":
            try:
                from survey.models import Survey
                survey = Survey.objects.get(query, pk=item[3:])
                _class, voted, answers, creator = "", "", "", survey.creator
                if survey.is_time_end():
                    time = "<p>Время голосования вышло</p>"
                else:
                    time = "<p>До " + str(survey.time_end) + "</p>"
                    if user.is_authenticated and not survey.is_user_voted(user.pk):
                        _class = " pointer u_survey_vote " + str(survey.is_multiple)
                if survey.image:
                    image = '<img src="' + survey.image.url + '" alt="user image">'
                else:
                    image = ""
                if survey.is_have_votes():
                    voters = '<span class="u_survey_detail pointer">'
                    for user in survey.get_6_users():
                        if user.s_avatar:
                            img = '<img src="' + user.s_avatar.url + '" style="width: 40px;border-radius:40px;" alt="image">'
                        else:
                            img = '<img src="/static/images/no_img/user.jpg" style="width: 40px;border-radius:40px;" alt="image">'
                    voters += '<figure class="staked">' + img + '</figure>'
                else:
                    voters = 'Пока никто не голосовал. Станьте первым!'
                for answer in survey.get_answers():
                    if answer.is_user_voted(user.pk):
                        voted = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>'
                    answers = ''.join([answers, '<div class="lite_color answer_style', _class, '"><div class="progress2" style="width:', str(answer.get_procent()), '%;"></div><span class="progress_span_r">', answer.text, ' - ', str(answer.get_count()), '</span><span class="progress_span_l" style="margin-left: auto;">', voted, str(answer.get_procent()), '%</span></div>'])
                block = ''.join([block, '<div style="flex: 0 0 100%;" survey-pk="', str(survey.pk), '" data-pk="', str(creator.pk), '" class="border text-center has-background-img position-relative box-shadow"><figure class="background-img">', image, '</figure><div class="container" style="list-style-type:none"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none border-bottom"></i><br><h4 class="u_survey_detail pointer">', survey.title, '</h4><a class="underline ajax" href="/users/', creator.pk, '">', str(creator), '</a>', time, '<br>', answers, voters, '</span></div></div>'])
            except:
                pass
        elif item[:3] == "lmu":
            try:
                from music.models import SoundList
                playlist = SoundList.objects.get(list_query, pk=item[3:])
                creator = playlist.creator
                if playlist.image:
                    image = '<img src="' + playlist.image.url + '" style="width:60px;height:88px;" alt="image">'
                else:
                    image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if playlist.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить плейлист" class="u_add_music_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in playlist.get_users_ids():
                        add_svg = '<span title="Удалить плейлист" class="u_remove_music_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="border"><div class="card-body" playlist-pk="', str(playlist.pk), '" style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_music_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_music_list pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(playlist.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список документов" class="u_add_doc_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список документов" class="u_remove_doc_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;"><div class="card-body border" doclist-pk="', str(list.pk), '" style="padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Документов: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            try:
                from gallery.models import PhotoList
                list = PhotoList.objects.get(pk=item[3:])
                creator = list.creator
                add = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add = '<a class="col pointer u_add_photo_list text-white">Добавить</a>'
                    elif user.pk in list.get_users_ids():
                        add = '<a class="col pointer u_remove_photo_list text-white">Удалить</a>'
                block = ''.join([block, '<div class="text-center bg-dark position-relative big_mobile_element col-md-6" photolist-pk="', str(list.pk), '"><figure class="background-img"><img src="', list.get_cover_photo(), '">"</figure><div class="container p-3"><h4 class="u_load_photo_list text-white pointer"><a class="nowrap">', list.name, '</a></h4><p><a class="ajax underline text-white nowrap" href="/users/', str(creator.pk), '">', str(list.creator), '</a></p><hr class="my-3"><a class="u_load_photo_list text-white pointer">', list.count_items_ru(), '</a><div class="row">', add, '</div>', '</div></div>'])
            except:
                pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoList
                list = VideoList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список видеозаписей" class="u_add_video_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список видеозаписей" class="u_remove_video_list btn_default pointer"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="border"><div class="card-body" videolist-pk="', str(list.pk), '" style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_video_list pointer">', list.name, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Видеозаписей: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
    return ''.join(["<div class='items_container'>", block, "</div>"])


def get_blog_comment_edit(comment, user):
    block = ''
    for item in comment.attach.split(","):
        if item[:3] == "pho":
            try:
                from gallery.models import Photo
                photo = Photo.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div class="col-md-6"><span class="photo_preview_delete" tooltip="Не прикреплять" flow="up"><svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path><path d="M0 0h24v24H0z" fill="none"></path></svg></span><span><input type="hidden" name="attach_items" value="pho', str(photo.pk), '"></span><img class="u_preview_photo image_fit pointer" src="', photo.file.url, '" photo-pk="', str(photo.pk), '"></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div class="col-md-6"><span class="video_preview_delete" tooltip="Не прикреплять" flow="up"><svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path><path d="M0 0h24v24H0z" fill="none"></path></svg></span><span><input type="hidden" name="attach_items" value="vid', str(video.pk), '"></span><img class="image_fit" src="', video.image.url, '"><span class="video_icon_play_v2 u_video_detail" video-pk="', str(video.pk), '"></span></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div style="display: flex; padding: 3px;"><span class="music_preview_delete" tooltip="Не прикреплять" flow="up"><svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path><path d="M0 0h24v24H0z" fill="none"></path></svg></span><span><input type="hidden" name="attach_items" value="mus', str(music.pk), '"></span><span><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></span><span style="margin-left: 10px; margin-right: 40px; overflow: hidden;"><h6 class="music_list_item pointer music_title" style="padding-top: 4px;"><a>', str(music.pk), '</a></h6></span></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div class="col-md-12" doc-pk="8" style="padding: 3px; display: flex;"><span class="doc_preview_delete" tooltip="Не прикреплять" flow="up"><svg fill="#FF0000" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path><path d="M0 0h24v24H0z" fill="none"></path></svg></span><span><input type="hidden" name="attach_items" value="doc', str(doc.pk), '"></span><span><span><svg fill="currentColor" style="width:35px;heigth:35px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"></path></svg></span></span><span class="media_title"><h6 style="padding-top: 9px;"><a href="', doc.file.url, '" style="white-space: nowrap;" target="_blank" rel="nofollow">', doc.title, '</a></h6></span></div>'])
            except:
                pass
        elif item[:3] == "sur":
            try:
                from survey.models import Survey
                survey = Survey.objects.get(query, pk=item[3:])
                _class, voted, answers, creator = "", "", "", survey.creator
                if survey.is_time_end():
                    time = "<p>Время голосования вышло</p>"
                else:
                    time = "<p>До " + str(survey.time_end) + "</p>"
                    if user.is_authenticated and not survey.is_user_voted(user.pk):
                        _class = " pointer u_survey_vote " + str(survey.is_multiple)
                if survey.image:
                    image = '<img src="' + survey.image.url + '" alt="user image">'
                else:
                    image = ""
                if survey.is_have_votes():
                    voters = '<span class="u_survey_detail pointer">'
                    for user in survey.get_6_users():
                        if user.s_avatar:
                            img = '<img src="' + user.s_avatar.url + '" style="width: 40px;border-radius:40px;" alt="image">'
                        else:
                            img = '<img src="/static/images/no_img/user.jpg" style="width: 40px;border-radius:40px;" alt="image">'
                    voters += '<figure class="staked">' + img + '</figure>'
                else:
                    voters = 'Пока никто не голосовал. Станьте первым!'
                for answer in survey.get_answers():
                    if answer.is_user_voted(user.pk):
                        voted = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>'
                    answers = ''.join([answers, '<div class="lite_color answer_style', _class, '"><div class="progress2" style="width:', str(answer.get_procent()), '%;"></div><span class="progress_span_r">', answer.text, ' - ', str(answer.get_count()), '</span><span class="progress_span_l" style="margin-left: auto;">', voted, str(answer.get_procent()), '%</span></div>'])
                block = ''.join([block, '<div style="flex: 0 0 100%;" survey-pk="', str(survey.pk), '" data-pk="', str(creator.pk), '" class="border text-center has-background-img position-relative box-shadow"><figure class="background-img">', image, '</figure><div class="container" style="list-style-type:none"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none border-bottom"></i><br><h4 class="u_survey_detail pointer">', survey.title, '</h4><a class="underline ajax" href="/users/', creator.pk, '">', str(creator), '</a>', time, '<br>', answers, voters, '</span></div></div>'])
            except:
                pass
        elif item[:3] == "lmu":
            try:
                from music.models import SoundList
                playlist = SoundList.objects.get(list_query, pk=item[3:])
                block = ''.join([block, '<div class="folder" playlist-pk="', str(playlist.pk), '" style="text-align: center;padding: 3px;"><span><input type="hidden" name="attach_items" value="lmu', str(playlist.pk), '"></span><div class="card-img-top file-logo-wrapper" style="padding: 2rem;"><a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100 u_load_playlist pointer"><svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-play"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg></div></a></div><div class="card-body pt-0"><div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_playlist pointer"><a class="nowrap">', playlist.name, ' (', str(playlist.count_items()), ')</a></p></div><small class="file-accessed pointer doc_attach_list_remove underline">Открепить</small></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(list_query, pk=item[3:])
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                block = ''.join([block, '<div class="folder" doclist-pk="', str(list.pk), '" style="text-align: center;padding: 3px;"><span><input type="hidden" name="attach_items" value="ldo', str(list.pk), '"></span><div class="card-img-top file-logo-wrapper" style="padding: 2rem;"><a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100 u_load_doc_list pointer">', image, '</div></a></div><div class="card-body pt-0"><div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_doc_list pointer"><a class="nowrap">', list.name, ' (', str(list.count_items()), ')</a></p></div><small class="file-accessed pointer doc_attach_list_remove underline">Открепить</small></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            try:
                from gallery.models import PhotoList
                list = PhotoList.objects.get(pk=item[3:])
                block = ''.join([block, '<div class="col-sm-6 col-md-4 bg-dark position-relative text-center big_mobile_element col-md-6" photolist-pk="', str(list.pk), '"><figure class="background-img"><img src="',list.get_cover_photo(), '"></figure><div class="container p-3"><h6 class="u_load_photo_list text-white pointer mb-2 nowrap">',list.name, '</h6><span class="photo_attach_list_remove underline pointer text-white">Открепить</span><hr class="my-3"><a class="u_load_photo_list pointer text-white">', list.count_items_ru(), '</a></div><span><input type="hidden" name="attach_items" value="lph', str(list.pk), '"></span></div>'])
            except:
                pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoList
                list = VideoList.objects.get(list_query, pk=item[3:])
                image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                block = ''.join([block, '<div class="folder" videolist-pk="', str(list.pk), '" style="text-align: center;padding: 3px;"><span><input type="hidden" name="attach_items" value="lvi', str(list.pk), '"></span><div class="card-img-top file-logo-wrapper" style="padding: 2rem;"><a class="nowrap"><div class="d-flex align-items-center justify-content-center w-100 u_load_video_list pointer">', image, '</div></a></div><div class="card-body pt-0"><div class="content-wrapper" style="display: flex;"><p class="card-text file-name mb-0 u_load_video_list pointer"><a class="nowrap">', list.name, ' (', str(list.count_items()), ')</a></p></div><small class="file-accessed pointer video_attach_list_remove underline">Открепить</small></div></div>'])
            except:
                pass
    return ''.join(["<div class='items_container comment_attach_block'>", block, "</div>"])
