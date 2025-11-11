from rest_framework.routers import DefaultRouter
from django.urls import path, include
from SessionAppApi.views import SessionViewSet
router=DefaultRouter()
router.register('sessions', SessionViewSet)
urlpatterns=[
    path('', include(router.urls))
]
