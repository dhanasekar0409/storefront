from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.Collection1ViewSet)
urlpatterns = router.urls
