from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from ckeditor_uploader import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('ckeditor/upload/', login_required(views.upload)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += re_path(r'^',
                       TemplateView.as_view(template_name='404.html'), name='not_found'),
