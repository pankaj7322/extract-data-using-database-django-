from django.urls import path
from . import views
from .views import sql_query_view, homepage, login_view,upload_audio
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('index/', views.index, name='index'),
    path('', login_view, name = 'login'),
    path('upload/', upload_audio, name='upload_audio'),
    path('submit/', views.submit_form, name='submit_form'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

