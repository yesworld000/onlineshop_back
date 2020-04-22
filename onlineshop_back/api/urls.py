from django.urls import path
from api import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('products/', views.products_list),
    path('products/<int:product_id>', views.product_detail),
    path('products/<str:ctg>/', views.by_category),
    path('products/<str:ctg>/<int:product_id>/', views.by_category_detail),
    path('categories/', views.CategoryList.as_view()),
]
