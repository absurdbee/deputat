
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
    doc.status = status
    doc.save(update_fields=['status'])
    return doc
