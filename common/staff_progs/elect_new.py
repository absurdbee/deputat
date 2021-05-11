from managers.models import ElectNewUserStaff, CanWorkStaffElectNewUser
from logs.model.manage_elect_new import ElectNewWorkerManageLog, ElectNewCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_elect_new_administrator(user, request_user):
    try:
        user.elect_new_user_staff.level = "A"
        user.elect_new_user_staff.save(update_fields=['level'])
    except:
        user_staff = ElectNewUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_elect_new_moderator(user, request_user):
    try:
        user.elect_new_user_staff.level = "M"
        user.elect_new_user_staff.save(update_fields=['level'])
    except:
        user_staff = ElectNewUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_elect_new_editor(user, request_user):
    try:
        user.elect_new_user_staff.level = "E"
        user.elect_new_user_staff.save(update_fields=['level'])
    except:
        user_staff = ElectNewUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_elect_new_administrator(user, request_user):
    try:
        user.elect_new_user_staff.level = ""
        user.elect_new_user_staff.save(update_fields=['level'])
        ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_elect_new_moderator(user, request_user):
    try:
        user.elect_new_user_staff.level = ""
        user.elect_new_user_staff.save(update_fields=['level'])
        ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_elect_new_editor(user, request_user):
    try:
        user.elect_new_user_staff.level = ""
        user.elect_new_user_staff.save(update_fields=['level'])
        ElectNewWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_elect_new_administrator_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_administrator = True
        user.can_work_staff_elect_new_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffElectNew.objects.create(user=user, is_administrator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_elect_new_moderator_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_moderator = True
        user.can_work_staff_elect_new_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffElectNew.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_elect_new_editor_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_editor = True
        user.can_work_staff_elect_new_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffElectNew.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_elect_new_administrator_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_administrator = False
        user.can_work_staff_elect_new_user.save(update_fields=['is_administrator'])
        ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_elect_new_moderator_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_moderator = False
        user.can_work_staff_elect_new_user.save(update_fields=['is_moderator'])
        ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_elect_new_editor_worker(user, request_user):
    try:
        user.can_work_staff_elect_new_user.is_editor = False
        user.can_work_staff_elect_new_user.save(update_fields=['is_editor'])
        ElectNewCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
