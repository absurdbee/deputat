from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users.views import AuthView, SignupView


urlpatterns = [
    #url(r'^admin__ok/', admin.site.urls),
    url(r'^', include ('main.urls')),

    url(r'^blog_cat/', include('blog_cat.urls')),
    url(r'^blog/', include('blog.urls')),

    url(r'^elect/', include('elect.urls')),
    url(r'^list/', include('lists.urls')),

    url(r'^search/', include('search.urls')),
    url(r'^users/', include('users.urls')),

    url(r'^region/', include('region.urls')),
    url(r'^tags/', include('tags.urls')),

    url(r'^about/', include('about.urls')),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^stat/', include('stst.urls')),

    url(r'^terms/', include('terms.urls')),
    url(r'^policy/', include('policy.urls')),
    url(r'^notify/', include('notify.urls')),

    url(r'^gallery/', include('gallery.urls')),
    url(r'^docs/', include('docs.urls')),
    url(r'^video/', include('video.urls')),
    url(r'^music/', include('music.urls')),
    url(r'^managers/', include('managers.urls')),
    url(r'^survey/', include('survey.urls')),
    url(r'^quan/', include('quan.urls')),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^communities/', include('communities.urls')),
    url(r'^district/', include('district.urls')),
    url(r'^okrug/', include('okrug.urls')),
    url(r'^city/', include('city.urls')),
    url(r'^chat/', include('chat.urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^email-verification/$', TemplateView.as_view(template_name="account/email_verification.html"), name='email-verification'),
    url(r'^password-reset/$',TemplateView.as_view(template_name="account/password_reset.html"), name='password-reset'),
    url(r'^password-reset/confirm/$',TemplateView.as_view(template_name="account/password_reset_confirm.html"), name='password-reset-confirm'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^password-change/$',TemplateView.as_view(template_name="account/password_change.html"), name='password-change'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="logout.html"), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^account/', include('allauth.urls')),

    url(r'^auth/$', AuthView.as_view(), name="login"),
    url(r'^signup/$', SignupView.as_view(), name="signup"),

]  +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
