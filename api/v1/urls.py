from rest_framework.routers import DefaultRouter

from api.v1.measurement import viewsets

router = DefaultRouter()

router.register(r'levels', viewsets.GlucoseLevelViewset, basename='levels')

urlpatterns = router.urls
