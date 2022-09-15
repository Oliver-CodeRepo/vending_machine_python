from django.urls import path

from api.views import CoinActionsView, CoinView, ProductActionsView, ProductView, PurchaseProductView


urlpatterns = [
    # products urls
    path('products', ProductView.as_view({'get': 'list'})),
    path('products/add', ProductActionsView.as_view({'post': 'create'})),
    path('products/update', ProductActionsView.as_view({'post': 'update'})),

    # purchase url
    path('products/purchase', PurchaseProductView.as_view({'post': 'purchase'})),
    
    # coins urls
    path('coins', CoinView.as_view({'get': 'list'})),
    path('coins/add', CoinActionsView.as_view({'post': 'create'})),
    path('coins/update', CoinActionsView.as_view({'post': 'update'})),
]