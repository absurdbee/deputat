from managers.models import BlogUserStaff, CanWorkStaffBlogUser
from logs.model.manage_blog import BlogWorkerManageLog, BlogCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_blog_administrator(user, request_user):
    try:
        user.blog_user_staff.level = "A"
        user.blog_user_staff.save(update_fields=['level'])
    except:
        user_staff = BlogUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    DocWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_blog_moderator(user, request_user):
    try:
        user.blog_user_staff.level = "M"
        user.blog_user_staff.save(update_fields=['level'])
    except:
        user_staff = BlogUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    BlogWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_blog_editor(user, request_user):
    try:
        user.blog_user_staff.level = "E"
        user.blog_user_staff.save(update_fields=['level'])
    except:
        user_staff = BlogUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    BlogWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_blog_administrator(user, request_user):
    try:
        user.blog_user_staff.level = ""
        user.blog_user_staff.save(update_fields=['level'])
        BlogWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_blog_moderator(user, request_user):
    try:
        user.blog_user_staff.level = ""
        user.blog_user_staff.save(update_fields=['level'])
        check_manager_state()
        BlogWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
    except:
        pass

def remove_blog_editor(user, request_user):
    try:
        user.blog_user_staff.level = ""
        user.blog_user_staff.save(update_fields=['level'])
        BlogWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_blog_administrator_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_administrator = True
        user.can_work_staff_blog_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffBlog.objects.create(user=user, is_administrator=True)
    user.is_supermanager = True
    BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_blog_moderator_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_moderator = True
        user.can_work_staff_blog_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffBlog.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_doc_editor_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_editor = True
        user.can_work_staff_blog_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffBlog.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_blog_administrator_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_administrator = False
        user.can_work_staff_blog_user.save(update_fields=['is_administrator'])
        BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_blog_moderator_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_moderator = False
        user.can_work_staff_blog_user.save(update_fields=['is_moderator'])
        BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_blog_editor_worker(user, request_user):
    try:
        user.can_work_staff_blog_user.is_editor = False
        user.can_work_staff_blog_user.save(update_fields=['is_editor'])
        BlogCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
