from django.views import View
from users.models import User
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = str(request.user.get_location().phone) + str(self.kwargs["phone"])
        try:
            obj = PhoneCodes.objects.get(phone=phone, code=code)
        except:
            obj = None
        if obj:
            user = User.objects.get(pk=request.user.pk)
            user.type = User.STANDART
            user.phone = obj.phone
            user.save()
            obj.delete()
            data = 'ok'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Код".'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response


class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        text = ""
        if not request.is_ajax() and not request.user.is_no_phone_verified():
            raise Http404
        else:
            phone = str(request.user.get_location().phone) + str(self.kwargs["phone"])
            if len(phone) > 8:
                try:
                    user = User.objects.get(phone=phone)
                    data = 'уже зарегистрирован'
                    response = render(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=GhfrKn0XKAmA1oVnyEzOnMI5uBnFN4ck&phone=" + phone)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним'
                    response = render(request,'generic/response/code_send.html',{'response_text':data})
                    return response
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                response = render(request,'generic/response/phone.html',{'response_text':data})
                return response
