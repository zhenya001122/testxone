from django.urls import path, include
from .views import CollectionCreate

urlpatterns = [
    path('createcollection/', CollectionCreate.as_view(), name='create-collection'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]