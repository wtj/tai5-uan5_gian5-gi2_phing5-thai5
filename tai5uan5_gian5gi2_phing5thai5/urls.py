from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, get_user_model
from allauth.account.views import logout
admin.autodiscover()
User=get_user_model()
def XX(request):
	logout(request)
	a=User.objects.get(pk=1)
	login(request,User.objects.get(pk=1))
	print(a)
	return XXX(request)
def XXX(request):
	return HttpResponse('{} X {} X {} X {}'.format(str(request.user),
			str(request.user.pk),request.user.username,request.user.pk==None))

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'tai5uan5_gian5gi2_phing5thai5.views.home', name='home'),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^$', TemplateView.as_view(template_name='index.html')),
	url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^XX',XX),
	
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('臺灣言語平臺.網址')),
)
