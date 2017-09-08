from django.conf.urls import url,include
from django.contrib import admin
from DjangoUeditor import urls as ueditor_urls
from django.conf import settings
from blogadmin import urls as blog_urls


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include(ueditor_urls)),
    url(r'', include(blog_urls)),
]

# let django recognize ueditor
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

