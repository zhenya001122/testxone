from django.urls import path, include
from .views import UserRegistration, CollectionCreate, UserDelete

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('userupdate/<int:pk>/', UserRegistration.as_view(), name='user-update'),
    path('userdelete/<int:pk>/', UserDelete.as_view(), name='user-delete'),
    path('createcollection/', CollectionCreate.as_view(), name='create-collection'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]