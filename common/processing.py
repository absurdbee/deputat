
def get_elect_new_processing(post):
    post.status = "P"
    post.save(update_fields=['status'])
    return post

def get_blog_message_processing(comment):
    comment.type = "PUB"
    comment.save(update_fields=['type'])
    return comment

def get_elect_new_message_processing(comment):
    comment.type = "PUB"
    comment.save(update_fields=['type'])
    return comment

def get_doc_processing(doc, status):
    doc.type = status
    doc.save(update_fields=['type'])
    return doc
def get_doc_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list


def get_photo_processing(photo, status):
    photo.type = status
    photo.save(update_fields=['type'])
    return photo
def get_photo_album_processing(album, status):
    album.type = status
    album.save(update_fields=['type'])
    return album
