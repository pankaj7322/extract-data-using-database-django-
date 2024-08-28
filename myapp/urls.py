from django.urls import path
from . import views
from .views import record_audio, sql_query_view, homepage, login_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('record_audio/', views.record_audio, name='record_audio'),

    path('index/', views.index, name='index'),
    path('', login_view, name = 'login'),
    path('submit/', views.submit_form, name='submit_form'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
