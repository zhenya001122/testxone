from django.urls import path, include
from .views import CollectionCreate, CollectionList, CollectionAPIDetailView, CollectionAPIList

urlpatterns = [
    path('createcollection/', CollectionCreate.as_view(), name='create-collection'),
    path('listcollection/', CollectionList.as_view(), name='list-collection'),
    path('collectiondetail/<int:pk>/', CollectionAPIDetailView.as_view(), name='detail-collection'),
    path('collectionlist/', CollectionAPIList.as_view(),),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]