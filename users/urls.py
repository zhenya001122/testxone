from django.urls import path, include
from .views import CollectionAPIDetailView, CollectionAPIList, LincAPIDetailView, LincAPIList


urlpatterns = [
    path('linccreatelist/', LincAPIList.as_view(), name='create-linc'),
    path('lincdetail/<int:pk>/', LincAPIDetailView.as_view(), name='detail-linc'),
    path('collectioncreatelist/', CollectionAPIList.as_view(),),
    path('collectiondetail/<int:pk>/', CollectionAPIDetailView.as_view(), name='detail-collection'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]


