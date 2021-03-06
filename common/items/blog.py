from blog.models import Blog
from common.model.comments import BlogComment

def linebreaks(value, autoescape=None):
    from django.utils.html import linebreaks
    from django.utils.safestring import mark_safe
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(linebreaks(value, autoescape))


def blog(user, blog):
    from django.utils.http import urlencode

    blog_url = "/blog/" + blog.slug + "/"
    block, tags, votes_on, card_drop = '', '', '', '<span class="dropdown-item copy_link" data-link="' + blog_url + '">Копировать ссылку</span>'

    if user.is_anonymous:
        user_like, user_dislike, user_inert = "btn_default", "btn_default", "btn_default"
        if not blog.votes_on:
            votes_on = 'style="display:none"'
    else:
        user_like, user_dislike, user_inert = "btn_default blog_like", "btn_default blog_dislike", "btn_default blog_inert"
        if blog.votes_on:
            if blog.is_have_likes() and blog.likes().filter(user_id=user.pk).exists():
                user_like = "btn_success blog_like"
            if blog.is_have_dislikes() and blog.dislikes().filter(user_id=user.pk).exists():
                user_dislike = "btn_danger blog_dislike"
            if blog.is_have_inerts() and blog.inerts().filter(user_id=user.pk).exists():
                user_inert = "btn_inert blog_inert"
        else:
            votes_on = 'style="display:none"'
        if user.is_supermanager():
            card_drop += '<span><span class="dropdown-item u_blog_remove">Удалить</span></span><span class="dropdown-item u_edit_blog">Редактировать</span>'
        else:
            card_drop += '<span class="dropdown-item claim_blog">Пожаловаться</span>'
            if blog.is_blog_in_bookmarks(user.pk):
                card_drop += '<span><span class="dropdown-item remove_blog_bookmark">Из коллекции</span></span>'
    if blog.comments_enabled:
        comments_enabled = ''
    else:
        comments_enabled = 'style="display:none"'

    for tag in blog.get_manager_tags():
        tags += '<a class="ajax" href="/tags/' + tag.name + '/">' + tag.name + '</a>'

    return ''.join([block, '<div class="event_card" data-pk="' + str(blog.pk) + '"><div class="event_img text-center"><span>\
    <span><img class="img-fluid card-img-top blog_window pointer" style="width:100%" src="' + blog.get_image() + '" alt="img"></span></span></div><div class="card-body event_body">\
    <h4 class="event_name"><div style="display: flex;"><span class="text-body blog_window pointer">' + blog.title + '</span>\
    <div class="dropdown" style="margin-left: auto;"><a style="cursor:pointer" class="icon-circle icon-30 btn_default drop">\
    <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path>\
    <path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z">\
    </path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top:18px">' + card_drop + '</div></div></div><span class="card-text item-company">\
    ' + blog.get_created() + ' | ' + tags + '</span></h4><div class="card-text event_description event_blog_description"><span><span class="blog_window pointer">' + blog.description[:180] + '...</span></span>\
    <div class="" style="padding: 5px;position: absolute;bottom: 3px;width: 100%;">\
    <span class="like ', user_like, ' pointer"', votes_on, ' title="Нравится"><svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0zm0 0h24v24H0V0z" fill="none"/><path d="M9 21h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.58 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2zM9 9l4.34-4.34L12 10h9v2l-3 7H9V9zM1 9h4v12H1z"/></svg>\
    <span class="likes_count margin_right_5">', str(blog.likes_count()), '</span></span><span class="dislike  ', user_dislike, ' pointer" ', votes_on, ' title="Не нравится">\
    <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0zm0 0h24v24H0V0z" fill="none"/><path d="M15 3H6c-.83 0-1.54.5-1.84 1.22l-3.02 7.05c-.09.23-.14.47-.14.73v2c0 1.1.9 2 2 2h6.31l-.95 4.57-.03.32c0 .41.17.79.44 1.06L9.83 23l6.59-6.59c.36-.36.58-.86.58-1.41V5c0-1.1-.9-2-2-2zm0 12l-4.34 4.34L12 14H3v-2l3-7h9v10zm4-12h4v12h-4z"/></svg>\
    <span class="dislikes_count margin_right_5">', str(blog.dislikes_count()), '</span></span><span class="inert  ', user_inert, '  pointer"', votes_on, ' title="Ниочём">\
    <svg width="22" height="22" fill="currentColor"viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M7 11v2h10v-2H7zm5-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>\
    <span class="inerts_count margin_right_5">', str(blog.inerts_count()), '</span></span><span class="dropdown"><span title="Поделиться" class="btn_default pointer get_blog_repost">\
    <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg>\
    <span class="repost_count margin_right_5">', str(blog.count_reposts()), '</span></span><div class="dropdown-menu" style="top: -162px;" data-pk="', str(blog.pk), '" data-link="/blog/', blog.slug,'" data-title="', blog.title,'"><span class="dropdown-header" style="font-weight:bold">Поделиться</span><span class="dropdown-item blog_share_vkontakte">VKontakte</span><span class="dropdown-item blog_share_facebook">Facebook</span><span class="dropdown-item blog_share_twitter">Twitter</span><span class="dropdown-item blog_share_telegram">Telegram</span></div></span><span ', comments_enabled, '  title="Комментарий" class="btn_default blog_window_comment" style="cursor:pointer;margin-right: 5px;">\
    <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>\
    <span class="comment-count margin_right_5">', str(blog.count_comments()), '</span></span><span title="Просмотры" style="right: 0;">\
    <svg width="22" height="22" fill="currentColor" class="svg_default" style="padding-bottom: 2px;font-size:17px" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"/></svg>', str(blog.count_views()), '</span></div></div><div class="load_full_data"></div></div></div>'])

def get_wall_blog(user, notify):
    blog = Blog.objects.get(pk=notify.object_id)
    if "_" in blog.type:
        return ''
    return blog(user, blog)

def get_comment_blog(user, notify):
    comment = BlogComment.objects.get(pk=notify.object_id)
    if "_" in comment.type:
        return ''
    if comment.parent:
        _blog = comment.parent.blog
    else:
        _blog = comment.blog
    if notify.is_have_user_set():
        return '<p style="padding-left: 7px"><a href="/users/' + str(notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">' + notify.creator.get_full_name() + '</a> '\
        + notify.get_verb_display() + ' новость ' + str(notify.count_user_set_comment()) + '</p>' + blog(user, _blog)
    elif notify.is_have_object_set():
        first_notify = notify.get_first_object_set()
        return '<p style="padding-left: 7px;"><a href="/users/' + str(first_notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
        first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
         + ' новость</p>' + blog(user, _blog)
    else:
        return '<p style="padding-left: 7px;"><a href="/users/' + str(notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
        notify.creator.get_full_name() + '</a>' + notify.get_verb_display()\
         + ' новость </p>' + blog(user, _blog)


def notify_blog(user, notify):
    blog = Blog.objects.get(pk=notify.object_id)
    return '<div data-pk="' + blog.pk + '"><div><div><p class="pointer elect_new_window card-img-top">' + blog.title + '</p></div></div></div>'

def get_notify_blog(user, notify):
    if notify.verb == 'BLO':
        return get_notify_blog(user, notify)
    elif notify.verb == 'BLOC':
        comment = BlogComment.objects.get(pk=notify.object_id)
        if "_" in comment.type:
            return ''
        if comment.parent:
            _blog = comment.parent.blog
        else:
            _blog = comment.blog
        if notify.is_have_user_set():
            return '<p style="padding-left: 7px"><a href="/users/' + str(notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">' + notify.creator.get_full_name() + '</a> '\
            + notify.get_verb_display() + ' новость ' + str(notify.count_user_set_comment()) + '</p>' + blog(user, _blog)
        elif notify.is_have_object_set():
            first_notify = notify.get_first_object_set()
            return '<p style="padding-left: 7px;"><a href="/users/' + str(first_notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
            first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
             + ' новость</p>' + blog(user, _blog)
        else:
            return '<p style="padding-left: 7px;"><a href="/users/' + str(notify.creator.pk) + '/" class="ajax" style="font-weight: bold;">'+ \
            notify.creator.get_full_name() + '</a>' + notify.get_verb_display()\
             + ' новость </p>' + blog(user, _blog)
