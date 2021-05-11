from managers.models import SurveyUserStaff, CanWorkStaffSurveyUser
from logs.model.manage_survey import SurveyWorkerManageLog, SurveyCreateWorkerManageLog
from common.utils import check_manager_state, check_supermanager_state
from users.models import User


def add_survey_administrator(user, request_user):
    try:
        user.survey_user_staff.level = "A"
        user.survey_user_staff.save(update_fields=['level'])
    except:
        user_staff = SurveyUserStaff.objects.create(user=user, level="A")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_survey_moderator(user, request_user):
    try:
        user.survey_user_staff.level = "M"
        user.survey_user_staff.save(update_fields=['level'])
    except:
        user_staff = SurveyUserStaff.objects.create(user=user, level="M")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_survey_editor(user, request_user):
    try:
        user.survey_user_staff.level = "E"
        user.survey_user_staff.save(update_fields=['level'])
    except:
        user_staff = SurveyUserStaff.objects.create(user=user, level="E")
    user.type = User.MANAGER
    user.save(update_fields=['type'])
    SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_EDITOR)
    return user_staff

def remove_survey_administrator(user, request_user):
    try:
        user.survey_user_staff.level = ""
        user.survey_user_staff.save(update_fields=['level'])
        SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_manager_state()
    except:
        pass

def remove_survey_moderator(user, request_user):
    try:
        user.survey_user_staff.level = ""
        user.survey_user_staff.save(update_fields=['level'])
        SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_manager_state()
    except:
        pass

def remove_survey_editor(user, request_user):
    try:
        user.survey_user_staff.level = ""
        user.survey_user_staff.save(update_fields=['level'])
        SurveyWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_manager_state()
    except:
        pass


def add_survey_administrator_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_administrator = True
        user.can_work_staff_survey_user.save(update_fields=['is_administrator'])
    except:
        user_staff = CanWorkStaffSurvey.objects.create(user=user, is_administrator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADMIN)
    return user_staff

def add_survey_moderator_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_moderator = True
        user.can_work_staff_survey_user.save(update_fields=['is_moderator'])
    except:
        user_staff = CanWorkStaffSurvey.objects.create(user=user, is_moderator=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_MODERATOR)
    return user_staff

def add_survey_editor_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_editor = True
        user.can_work_staff_survey_user.save(update_fields=['is_editor'])
    except:
        user_staff = CanWorkStaffSurvey.objects.create(user=user, is_editor=True)
    user.type = User.SUPERMANAGER
    user.save(update_fields=['type'])
    SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=CREATE_ADVERTISER)
    return user_staff

def remove_survey_administrator_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_administrator = False
        user.can_work_staff_survey_user.save(update_fields=['is_administrator'])
        SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_ADMIN)
        check_supermanager_state()
    except:
        pass

def remove_survey_moderator_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_moderator = False
        user.can_work_staff_survey_user.save(update_fields=['is_moderator'])
        SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_MODERATOR)
        check_supermanager_state()
    except:
        pass

def remove_survey_editor_worker(user, request_user):
    try:
        user.can_work_staff_survey_user.is_editor = False
        user.can_work_staff_survey_user.save(update_fields=['is_editor'])
        SurveyCreateWorkerManageLog.objects.create(user=user, manager=request_user, action_type=DELETE_EDITOR)
        check_supermanager_state()
    except:
        pass
