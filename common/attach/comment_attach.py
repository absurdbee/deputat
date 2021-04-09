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
                block = ''.join([block, '<div class="photo"><div class="progressive replace image_fit_200 u_blog_comment_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div class="video"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_blog_comment_video" video-pk="', str(video.pk), '" data-uuid="', str(video.uuid), '" video-counter="0"></div></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(query, pk=item[3:])
                if music.artwork_url:
                    figure = ''.join(['<figure><a class="music_list_comment music_thumb pointer"><img style="width:30px;heigth:auto" src="', music.artwork_url.url, '" alt="img" /></a></figure>'])
                else:
                    figure = '<figure><a class="music_list_comment music_thumb pointer"><svg fill="currentColor" style="width:30px;heigth:30px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 5h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S10 13.88 10 12.5s1.12-2.5 2.5-2.5c.57 0 1.08.19 1.5.51V5h4v2zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z"/></svg></a></figure>'
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_all_audio_playlists():
                        if list.is_track_in_list(music.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" style="margin-left:auto;display:flex" data-pk="', str(music.pk), '" user-pk="', str(post.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 25px;">', lists, '<span class="dropdown-item u_create_music_list_track_add" style="padding-left: 30px;">В новый плейлист</span></div></span></span>'])
                block = ''.join([block, '<div class="music" data-path="', music.uri, '" data-duration="', music.duration, '" style="width: 100%;position: relative;"><div class="media" music-counter="0">', figure, '<div class="media-body" style="display: flex;"><h6 class="music_list_comment music_title"><a>', music.title, '</a></h6>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(query, pk=item[3:])
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_all_docs_lists():
                        if list.is_doc_in_list(doc.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_doc_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_doc_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                span_btn = ''.join([span_btn, '<span class="span_btn" doc-pk="', str(doc.pk), '" data-pk="', str(post.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop" title="Добавить в плейлист"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 32px;">', lists, '<span class="dropdown-item u_create_doc_list_doc_add" style="padding-left: 30px;">В новый список</span></div></span></span>'])
                block = ''.join([block, '<div style="flex-basis: 100%;margin-bottom:10px"><div class="media" style="position: relative;"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body" style="padding: 0"><h6 class="pointer" style="width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
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
                    image = '<img src="' + playlist.image.url + '" style="width:120px;height:120px;" alt="image">'
                else:
                    image = '<svg fill="currentColor" class="svg_default border" style="width:120px;height:120px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
                add_svg = '', ''
                if user.is_authenticated:
                    if playlist.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить плейлист" class="u_add_music_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in playlist.get_users_ids():
                        add_svg = '<span title="Удалить плейлист" class="u_remove_music_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(playlist.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_music_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_music_list pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(playlist.count_tracks()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                repost_svg, add_svg = '', ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список документов" class="u_add_doc_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список документов" class="u_remove_doc_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Документов: ', str(list.count_docs()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            #try:
            from gallery.models import Album
            album = Album.objects.get(pk=item[3:])
            creator = album.creator
            add = ''
            if user.is_authenticated:
                if album.is_user_can_add_list(user.pk):
                    add = '<a class="col pointer u_add_photo_album">В коллекцию</a>'
                elif user.pk in album.get_users_ids():
                    add = '<a class="col pointer u_remove_photo_album">Удалить</a>'
            block = ''.join([block, '<div class="text-center bg-dark position-relative big_mobile_element col-md-6" data-pk="', str(album.pk), '"><div><figure class="background-img"><img src="', album.get_cover_photo(), '">"</figure><div class="container p-3"><h4 class="u_load_photo_album text-white pointer"><a class="nowrap">', album.title, '</a></h4><p><a class="ajax underline text-white nowrap" href="/users/', str(creator.pk), '">', str(album.creator), '</a></p><hr class="my-3"><a class="u_load_photo_album text-white pointer">', album.count_photo_ru(), '</a><div class="row">', add, '</div>', '</div></div></div>'])
            #except:
            #    pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoAlbum
                list = VideoAlbum.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
                repost_svg, add_svg = '', ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список видеозаписей" class="u_add_video_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список видеозаписей" class="u_remove_video_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_video_list pointer">', list.title, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Видеозаписей: ', str(list.count_video()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
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
                block = ''.join([block, '<div class="photo"><div class="progressive replace image_fit u_elect_new_comment_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(query, pk=item[3:])
                block = ''.join([block, '<div class="video"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_elect_new_comment_video" video-pk="', str(video.pk), '" data-uuid="', str(video.uuid), '" video-counter="0"></div></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(query, pk=item[3:])
                if music.artwork_url:
                    figure = ''.join(['<figure><a class="music_list_comment music_thumb pointer"><img style="width:30px;heigth:auto" src="', music.artwork_url.url, '" alt="img" /></a></figure>'])
                else:
                    figure = '<figure><a class="music_list_comment music_thumb pointer"><svg fill="currentColor" style="width:30px;heigth:30px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 5h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S10 13.88 10 12.5s1.12-2.5 2.5-2.5c.57 0 1.08.19 1.5.51V5h4v2zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z"/></svg></a></figure>'
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_all_audio_playlists():
                        if list.is_track_in_list(music.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" style="margin-left:auto;display:flex" data-pk="', str(music.pk), '" user-pk="', str(post.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 25px;">', lists, '<span class="dropdown-item u_create_music_list_track_add" style="padding-left: 30px;">В новый плейлист</span></div></span></span>'])
                block = ''.join([block, '<div class="music" data-path="', music.uri, '" data-duration="', music.duration, '" style="width: 100%;position: relative;"><div class="media" music-counter="0">', figure, '<div class="media-body" style="display: flex;"><h6 class="music_list_comment music_title"><a>', music.title, '</a></h6>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(query, pk=item[3:])
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_all_docs_lists():
                        if list.is_doc_in_list(doc.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_doc_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_doc_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                span_btn = ''.join([span_btn, '<span class="span_btn" doc-pk="', str(doc.pk), '" data-pk="', str(post.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop" title="Добавить в плейлист"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 32px;">', lists, '<span class="dropdown-item u_create_doc_list_doc_add" style="padding-left: 30px;">В новый список</span></div></span></span>'])
                block = ''.join([block, '<div style="flex-basis: 100%;margin-bottom:10px"><div class="media" style="position: relative;"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body" style="padding: 0"><h6 class="pointer" style="width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
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
                    image = '<img src="' + playlist.image.url + '" style="width:120px;height:120px;" alt="image">'
                else:
                    image = '<svg fill="currentColor" class="svg_default border" style="width:120px;height:120px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
                add_svg = '', ''
                if user.is_authenticated:
                    if playlist.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить плейлист" class="u_add_music_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in playlist.get_users_ids():
                        add_svg = '<span title="Удалить плейлист" class="u_remove_music_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(playlist.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_music_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_music_list pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(playlist.count_tracks()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список документов" class="u_add_doc_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список документов" class="u_remove_doc_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Документов: ', str(list.count_docs()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            try:
                from gallery.models import Album
                album = Album.objects.get(list_query, pk=item[3:])
                creator = album.creator
                add = ''
                if user.is_authenticated:
                    if album.is_user_can_add_list(user.pk):
                        add = '<a class="col pointer u_add_photo_album">В коллекцию</a>'
                    elif user.pk in album.get_users_ids():
                        add = '<a class="col pointer u_remove_photo_album">Удалить</a>'
                block = ''.join([block, '<div class="custom_color text-center has-background-img position-relative box-shadow" data-pk="', str(creator.pk), '" data-uuid="', str(album.uuid), '" style="width: 100%;flex-basis: 100%;"><figure class="background-img"><img src="', album.get_cover_photo().file.url, '">"</figure><div class="container"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none"></i><br><h4 class="u_load_photo_album pointer"><a>', album.title, '</a></h4><p class="lead"><a class="ajax underline" href="/users/', creator.pk, '">', str(album.creator), '</a></p><hr class="my-3"><a class="u_load_photo_album pointer">', album.count_photo_ru(), '</a><div class="row">', add, '</div>', '</div></div>'])
            except:
                pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoAlbum
                list = VideoAlbum.objects.get(list_query, pk=item[3:])
                creator = list.creator
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
                add_svg = ''
                if user.is_authenticated:
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список видеозаписей" class="u_add_video_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список видеозаписей" class="u_remove_video_list btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_video_list pointer">', list.title, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', creator.pk, '">', str(creator.get_full_name_genitive()), '</a><br>Видеозаписей: ', str(list.count_video()), '</p></div><span class="playlist_share">', add_svg, '</span></div></div></div>'])
            except:
                pass
    return ''.join(["<div class='items_container'>", block, "</div>"])
