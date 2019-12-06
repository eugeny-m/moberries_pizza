from rest_framework import routers

from pizza.views import (
    PizzaViewSet,
    OrderViewSet,
    OrderedPizzaViewSet,
    PizzaPriceViewSet
)


router = routers.SimpleRouter()

router.register(r'pizza', PizzaViewSet)
router.register(r'pizza-price', PizzaPriceViewSet)
router.register(r'order', OrderViewSet)
router.register(r'ordered-pizza', OrderedPizzaViewSet)

urlpatterns = router.urls
