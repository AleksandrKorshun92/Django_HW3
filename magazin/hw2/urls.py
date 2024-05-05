from django.urls import path
from .views import receive_orders, orders_story, upload_image, add_product, index

urlpatterns = [
    path("", index, name="start"),
    path("orders/<int:pk_cust>/", receive_orders, name="receive_orders"),
    path("story/<int:pk_cust>/<int:days>/", orders_story, name="orders_story"),
    path("image/", upload_image, name="upload_image"),
    path("add/", add_product, name="add_product"),
]