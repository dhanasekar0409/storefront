from cgitb import lookup
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# Parent Router
router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.Collection1ViewSet)
router.register("carts", views.CartViewSet, basename="carts")

# Child Router
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

# URLCONFIG
urlpatterns = router.urls + products_router.urls
