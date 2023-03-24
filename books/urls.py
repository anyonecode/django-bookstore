
from django.urls import path
from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView,proupdate,proform,prolist
from . import views


urlpatterns = [
    path('',views.index,name='home'),
    path('booklist', BooksListView.as_view(), name = 'booklist'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('view',prolist.as_view(),name='view'),
    path('myprofile/',proform.as_view(),name='myprofile'),
    path('edit/<int:pk>',proupdate.as_view(),name='edit'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
]