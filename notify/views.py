from django.views.generic import ListView
from common.utils import get_my_template


class AllNotifyView(ListView):
    """ Все уведомления пользователя """
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_my_template("notify/all_notify.html", request.user, request.META['HTTP_USER_AGENT'])
        self.user, self.all_notify = request.user, request.user.get_user_notify()
        return super(AllNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        return self.all_notify
