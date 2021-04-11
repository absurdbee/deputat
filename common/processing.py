
def get_elect_new_processing(post):
    post.status = "P"
    post.save(update_fields=['status'])
    return post

def get_blog_message_processing(comment):
    comment.status = "PUB"
    comment.save(update_fields=['status'])
    return comment

def get_elect_new_message_processing(comment):
    comment.status = "PUB"
    comment.save(update_fields=['status'])
    return comment

def get_doc_processing(doc, status):
    doc.status = status
    doc.save(update_fields=['status'])
    return doc
def get_doc_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list

def get_photo_processing(photo, status):
    photo.status = status
    photo.save(update_fields=['status'])
    return photo
def get_photo_album_processing(album, status):
    album.type = status
    album.save(update_fields=['type'])
    return album

def get_music_processing(music, status):
    music.status = status
    music.save(update_fields=['status'])
    return music
def get_playlist_processing(playlist, status):
    playlist.type = status
    playlist.save(update_fields=['type'])
    return playlist

def get_video_processing(video, status):
    video.status = status
    video.save(update_fields=['status'])
    return video
def get_video_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list
