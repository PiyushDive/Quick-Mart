from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .forms import LoginForm, PassChangeForm, PassResetForm, SetPassForm
from django.contrib.auth import views as auth_views
# akshay chaudhari 
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    # path('search/', views.search, name='search'),
    path('mobile/<slug:data>/', views.mobile, name='mobile_data'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('logout/', views.logout_view, name='logout'),

    path('accounts/login/', auth_views.LoginView.as_view
    (template_name='app/login.html', authentication_form=LoginForm), name='login'),
    
    path('change_password/', auth_views.PasswordChangeView.as_view
    (template_name='app/password_change.html', form_class=PassChangeForm, success_url='/passwordchangedone/'), name='change_password'),
    
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view
    (template_name= 'app/passwordchangedone.html'), name='passwordchangedone') ,

# Cart-
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

# Password Reset-

    path('password_reset/', auth_views.PasswordResetView.as_view
    (template_name='app/pass_reset.html', form_class=PassResetForm),
     name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view
    (template_name='app/pass_reset_done.html'), name='password_reset_done'),
    
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name='app/pass_reset_confirm.html', form_class=SetPassForm), name='password_reset_confirm'),
    
    path('password_reset/success/', auth_views.PasswordResetCompleteView.as_view
    (template_name='app/pass_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
