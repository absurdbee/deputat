from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from lists.models import Region
from blog.models import Blog, ElectNew
from common.model.other import PhoneCodes
from users.models import User
from django.views import View
from django.http import Http404
import json, requests
from common.utils import render_for_platform, get_small_template


class MainPageView(TemplateView, CategoryListMixin):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("main/test.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MainPageView,self).get_context_data(**kwargs)
		context["last_elect_news"] = ElectNew.objects.filter(status="P")[:10]
		context["last_blog_news"] = Blog.objects.only("pk")[:10]
		return context


class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_small_template("main/phone_verification.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPhoneSend,self).get(request,*args,**kwargs)


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        _phone = self.kwargs["phone"]
        phone = request.user.get_last_location().phone + _phone
        try:
            obj = PhoneCodes.objects.get(phone=phone)
        except:
            obj = None
        if obj:
            user = User.objects.get(pk=request.user.pk)
            user.perm = User.STANDART
            user.phone = obj.phone
            user.save()
            obj.delete()
            data = 'ok'
            response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
            return response
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Последние 4 цифры". Если не можете найти номер, нажмите на кнопку "Перезвонить повторно".'
            response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
            return response


class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes
        from users.models import User

        text = ""
        if not request.is_ajax() and not request.user.is_no_phone_verified():
            raise Http404
        else:
            _phone = self.kwargs["phone"]
            if len(_phone) > 8:
                phone = request.user.get_last_location().phone + _phone
                try:
                    user = User.objects.get(phone=phone)
                    data = 'Пользователь с таким номером уже зарегистрирован. Используйте другой номер или напишите в службу поддержки, если этот номер Вы не использовали ранее.'
                    response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=729235&key=G0NjjPZgzj7D65tcjAuCyKhR4nkTlntK&phone=" + phone)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Последние 4 цифры" и нажать "Подтвердить"'
                    response = render_for_platform(request,'generic/response/code_send.html',{'response_text':data})
                    return response
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                response = render_for_platform(request,'generic/response/phone.html',{'response_text':data})
                return response
