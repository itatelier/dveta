from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from base import views as default

urlpatterns = [
    url(r"^$", default.Index.as_view(), name='index'),
    url(r"^pg/card/", default.PlaygroundCard.as_view(), name='playground_card'),
    url(r"^pg/listing/", default.PlaygroundListing.as_view(), name='playground_listing'),
    url(r"^pg/forms/", default.PlaygroundForms.as_view(), name='playground_forms'),

    #REST
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Default
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^forbidden/$', default.Forbidden.as_view(), name='forbidden'),

    # Ajax actions
     url(r'^ac/$', default.AutoCompliteJsonView.as_view(), name='ac'),
    # url(r'^acid/$', default.ac_with_id.as_view(), name='ac'),

    # Dummy Views
    url(r'^dummy/', include('dummyapp.urls')),

    # Apps
    url(r'^company/', include('company.urls')),
    url(r'^contragents/', include('contragent.urls')),
    url(r'^persons/', include('person.urls')),
    url(r'^cars/', include('car.urls')),

    # Admin
    # url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
