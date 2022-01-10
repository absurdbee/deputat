from django.conf.urls import url
from users.view.load import *


urlpatterns = [
    url(r'^u_photo_load/$', UserLoadPhoto.as_view(), name="u_photo_load"),
    url(r'^u_photo_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadPhotoList.as_view(), name="u_photo_list_load"),
    url(r'^u_photo_comment_load/$', UserLoadPhotoComment.as_view(), name="u_photo_comment_load"),
    url(r'^u_img_message_load/$', UserLoadPhotoMessage.as_view(), name="u_photo_comment_load"),

    url(r'^u_video_load/$', UserLoadVideo.as_view(), name="u_video_load"),
    url(r'^u_video_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadVideoList.as_view(), name="u_video_list_load"),

    url(r'^u_doc_load/$', UserLoadDoc.as_view(), name="u_doc_load"),
    url(r'^u_doc_list_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadDocList.as_view(), name="u_doc_list_load"),

    url(r'^u_music_load/$', UserLoadMusic.as_view(), name="u_music_load"),
    url(r'^u_playlist_load/(?P<uuid>[0-9a-f-]+)/$', UserLoadMusicList.as_view(), name="u_music_list_load"),

    url(r'^change_theme/$', ChangeTheme.as_view()),
    url(r'^smiles/$', SmilesLoad.as_view()),
    url(r'^smiles_stickers/$', SmilesStickersLoad.as_view()),
    url(r'^chats/$', ChatsLoad.as_view()),
]
