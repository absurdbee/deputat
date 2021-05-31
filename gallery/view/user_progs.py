from users.models import User
from gallery.models import PhotoList, Photo
from gallery.forms import PhotoListForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from users.models import User
from django.http import Http404
from common.templates import render_for_platform, get_small_template
from django.views.generic.base import TemplateView


class AddPhotoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
        return HttpResponse()

class RemovePhotoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
        return HttpResponse()


class AddPhotoIntUserList(View):
    """
    асинхронная мульти загрузка фотографий пользователя в альбом
    """
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            list, photos = PhotoList.objects.get(uuid=self.kwargs["uuid"]), []
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list)
                photos += [photo]
            return render_for_platform(request, 'user_gallery/new_list_photos.html',{'object_list': photos})
        else:
            raise Http404

class AttachPhotoInUserList(View):
    """
    мульти сохранение изображений с моментальным выводом в превью
    """
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            list, photos = request.user.get_photo_list(), []
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list)
                photos += [photo]
            return render_for_platform(request, 'user_gallery/new_list_photos.html',{'object_list': photos})
        else:
            raise Http404

class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator.pk == request.user.pk:
            photo.delete_photo(None)
            return HttpResponse()
        else:
            raise Http404

class UserPhotoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator.pk == request.user.pk:
            photo.abort_delete_photo(None)
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator.pk == request.user.pk:
            photo.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivatePhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and photo.creator.pk == request.user.pk:
            photo.make_publish()
            return HttpResponse()
        else:
            raise Http404

class PhotoListUserCreate(TemplateView):
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.form = PhotoListForm()
        self.template_name = get_small_template("user_gallery/add_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoListUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form = PhotoListForm(request.POST)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            if not list.description:
                list.description = "Без описания"
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None, is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'user_gallery/list/my_a.html',{'list': new_list})
        else:
            return HttpResponseBadRequest()
        return super(PhotoListUserCreate,self).get(request,*args,**kwargs)

class PhotoListUserEdit(TemplateView):
    template_name = None
    form = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_small_template("user_gallery/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoListUserEdit,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["list"] = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PhotoListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.list.creator.pk:
            list = self.form.save(commit=False)
            if not list.description:
                list.description = "Без описания"
            list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(PhotoListUserEdit,self).get(request,*args,**kwargs)

class PhotoListUserDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk and list.type != PhotoList.MAIN:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class PhotoListUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.creator.pk == request.user.pk:
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404


class AddPhotoInUserPhotoList(View):
    """
    Добавляем фото в любой альбом, если его там нет
    """
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(photo.pk) and list.creator.pk == request.user.pk:
            list.photo_list.add(photo)
            return HttpResponse()
        else:
            raise Http404

class RemovePhotoInUserPhotoList(View):
    """
    Удаляем фото из любого альбома, если он там есть
    """
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(photo.pk) and list.creator.pk == request.user.pk:
            list.photo_list.remove(photo)
            return HttpResponse()
        else:
            raise Http404
