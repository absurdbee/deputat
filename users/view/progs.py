from django.views import View
from users.models import User
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render



class PhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        if not request.is_ajax() and not request.user.is_no_phone_verified():
            raise Http404
        else:
            phone = self.kwargs["phone"]
            if len(phone) > 8:
                try:
                    user = User.objects.get(phone=phone)
                    data = 'уже зарегистрирован'
                    response = render(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    response = requests.get("https://api.ucaller.ru/v1.0/initCall?service_id=694155&key=t4Avgg7ilt0s6BHsvu9mcVA49gv6bkkU&phone=" + phone)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Код" и нажать "Подтвердить"'
                    return render(request,'generic/response/code_send.html',{'response_text':data })
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                return render(request,'generic/response/phone.html',{'response_text':data})


class PhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = self.kwargs["phone"]
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
            return render(request,'generic/response/phone.html',{'response_text':data})
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Код".'
            return render(request,'generic/response/phone.html',{'response_text':data})


class ChangePhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        phone = self.kwargs["phone"]

        if len(phone) > 8:
            try:
                user = User.objects.get(phone=phone)
                data = 'уже зарегистрирован'
                response = render(request,'generic/response/phone.html',{'response_text':data})
                return response
            except:
                response = requests.get("https://api.ucaller.ru/v1.0/initCall?service_id=729235&key=G0NjjPZgzj7D65tcjAuCyKhR4nkTlntK&phone=" + phone)
                data = response.json()
                PhoneCodes.objects.create(phone=phone, code=data['code'])
                data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Код" и нажать "Подтвердить"'
                return render(request,'generic/response/change_code_send.html',{'response_text':data })
        else:
            data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
            return render(request,'generic/response/phone.html',{'response_text':data})


class ChangePhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = self.kwargs["phone"]
        try:
            obj = PhoneCodes.objects.get(phone=phone, code=code)
        except:
            obj = None
        if obj:
            request.user.phone = obj.phone
            request.user.save(update_fields=["phone"])
            obj.delete()
            data = 'ok'
            return render(request,'generic/response/phone.html',{'response_text':data})
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Код".'
            return render(request,'generic/response/phone.html',{'response_text':data})


class SecretKeyVerify(View):
    def post(self,request,*args,**kwargs):
        from users.model.settings import UserSecretKey

        if not request.is_ajax():
            raise Http404
        key = request.POST.get('key')
        user = User.objects.get(pk=self.kwargs["pk"])
        key_items = UserSecretKey.objects.only("pk")
        if UserSecretKey.objects.filter(user=user,key=key).exists():
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse("ok")
        else:
            return render(request,'generic/response/error_code_recover.html',{'response_text':'Неверное секретное выражение!','key_items':key_items})

class SecretKeyVerify(View):
    def post(self,request,*args,**kwargs):
        from users.model.settings import UserSecretKey

        if not request.is_ajax():
            raise Http404
        key = request.POST.get('key')
        user = User.objects.get(pk=self.kwargs["pk"])
        key_items = UserSecretKey.objects.only("pk")
        if UserSecretKey.objects.filter(user=user,key=key).exists():
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse("ok")
        else:
            return render(request,'generic/response/error_code_recover.html',{'response_text':'Неверное секретное выражение!','key_items':key_items})


class RecoveryPhoneSend(View):
    def get(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import RecoveryPhoneCodes

        if not request.is_ajax() and request.user.is_authenticated:
            raise Http404
        phone = self.kwargs["phone"]

        if len(phone) > 8:
            if User.objects.filter(phone=phone).exists():
                user = User.objects.get(phone=phone)

                if user.is_have_secret_key():
                    response = render(request,'generic/response/recover_secret_key.html',{'user':user})
                else:
                    response = requests.get("https://api.ucaller.ru/v1.0/initCall?service_id=729235&key=G0NjjPZgzj7D65tcjAuCyKhR4nkTlntK&phone=" + phone)
                    data = response.json()
                    RecoveryPhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Код" и нажать "Подтвердить"'
                    return render(request,'generic/response/recover_code_send.html',{'response_text':data })
                return response
            else:
                return render(request,'generic/response/phone.html',{'response_text':'user_does_not_exists'})
        else:
            data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
            return render(request,'generic/response/phone.html',{'response_text':data})

class RecoveryPhoneVerify(View):
    def get(self,request,*args,**kwargs):
        from common.model.other import RecoveryPhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = self.kwargs["phone"]
        if RecoveryPhoneCodes.objects.filter(phone=phone, code=code).exists():
            from django.contrib.auth import login

            RecoveryPhoneCodes.objects.filter(phone=phone, code=code).delete()
            user = User.objects.get(phone=phone)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse("ok")
        else:
            return render(request,'generic/response/phone.html',{'response_text':'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Код".'})
