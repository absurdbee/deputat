
def get_elect_new_processing(new, type):
    new.type = type
    new.save(update_fields=['type'])
    return new

def get_blog_processing(blog):
    return blog

def get_blog_comment_processing(comment):
    comment.type = "PUB"
    comment.save(update_fields=['type'])
    return comment

def get_elect_new_comment_processing(comment):
    comment.type = "PUB"
    comment.save(update_fields=['type'])
    return comment

def get_doc_processing(doc, type):
    doc.type = type
    doc.save(update_fields=['type'])
    return doc
def get_doc_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list

def get_photo_processing(photo, type):
    photo.type = type
    photo.save(update_fields=['type'])
    return photo
def get_photo_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list

def get_music_processing(music, type):
    music.type = type
    music.save(update_fields=['type'])
    return music
def get_playlist_processing(playlist, type):
    playlist.type = type
    playlist.save(update_fields=['type'])
    return playlist

def get_video_processing(video, type):
    video.type = type
    video.save(update_fields=['type'])
    return video
def get_video_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list
