
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
