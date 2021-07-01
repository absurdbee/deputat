from django.views import View
from users.models import User
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render



class PhoneSend(View):
    def post(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        if not request.is_ajax() and not request.user.is_no_phone_verified():
            raise Http404
        else:
            _phone = self.kwargs["phone"]
            if len(_phone) > 8:
                first_number = request.POST.get('first_number')
                phone = first_number + _phone
                try:
                    user = User.objects.get(phone=phone)
                    data = 'уже зарегистрирован'
                    response = render(request,'generic/response/phone.html',{'response_text':data})
                    return response
                except:
                    from users.model.profile import UserLocation
                    loc = UserLocation.objects.filter(user=request.user).last()
                    loc.phone = first_number
                    loc.save(update_fields=["phone"])
                    url = "https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=G0NjjPZgzj7D65tcjAuCyKhR4nkTlntK&phone=" + request.user.get_last_location().phone + _phone
                    response = requests.get(url=url)
                    data = response.json()
                    PhoneCodes.objects.create(phone=phone, code=data['code'])
                    data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Последние 4 цифры" и нажать "Подтвердить"'
                    response = render(request,'generic/response/code_send.html',{'response_text':data,'phone':first_number })
                    return response
            else:
                data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
                response = render(request,'generic/response/phone.html',{'response_text':data})
                return response


class PhoneVerify(View):
    def post(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = request.POST.get('first_number') + str(self.kwargs["phone"])
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


class ChangePhoneSend(View):
    def post(self,request,*args,**kwargs):
        import json, requests
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        _phone = self.kwargs["phone"]

        if len(_phone) > 8:
            phone = request.POST.get('first_number') + self.kwargs["phone"]
            try:
                user = User.objects.get(phone=phone)
                data = 'уже зарегистрирован'
                response = render(request,'generic/response/phone.html',{'response_text':data})
                return response
            except:
                response = requests.get(url="https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=G0NjjPZgzj7D65tcjAuCyKhR4nkTlntK&phone=" + phone)
                data = response.json()
                PhoneCodes.objects.create(phone=phone, code=data['code'])
                data = 'Мы Вам звоним. Последние 4 цифры нашего номера - код подтверждения, который нужно ввести в поле "Последние 4 цифры" и нажать "Подтвердить"'
                response = render(request,'generic/response/change_code_send.html',{'response_text':data})
                return response
        else:
            data = 'Введите, пожалуйста, корректное количество цифр Вашего телефона'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response


class ChangePhoneVerify(View):
    def post(self,request,*args,**kwargs):
        from common.model.other import PhoneCodes

        if not request.is_ajax():
            raise Http404
        code = self.kwargs["code"]
        phone = request.POST.get('first_number') + str(self.kwargs["phone"])
        try:
            obj = PhoneCodes.objects.get(phone=phone, code=code)
        except:
            obj = None
        if obj:
            request.user.phone = obj.phone
            user.save(update_fields=["phone"])
            obj.delete()
            data = 'ok'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response
        else:
            data = 'Код подтверждения неверный. Проверьте, пожалуйста, номер, с которого мы Вам звонили. Последние 4 цифры этого номера и есть код подтверждения, который нужно ввести с поле "Код".'
            response = render(request,'generic/response/phone.html',{'response_text':data})
            return response
