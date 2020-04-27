
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('scholarships/',include('scholarships.urls')),
    path('chat/',include('talking_bot.urls')),
    path('accounts/',include('accounts.urls'))
]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

