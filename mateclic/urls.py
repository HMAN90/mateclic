"""
URL configuration for mateclic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from public import views as publicviews
from adminmodule import views as adminviews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('public/',publicviews.home,name="home"),
    path('public/about/',publicviews.about,name="about"),
    path('public/contact/',publicviews.contact,name="contact"),
    path('public/equipments/',publicviews.equipments,name="equipments"),
    path('public/equipments/<int:equipment_id>/rent/',publicviews.rent,name="rent"),
    path('public/equipments/rent/<int:rent_id>/paymentmethod/',publicviews.rent_payment_method,name="rent-payment-method"),
    path('public/equipments/rent/<int:rent_id>/mobilemoneypayment/',publicviews.rent_mobilemoney_payment,name="rent-mobilemoney-payment"),
    path('public/equipments/rent/<int:rent_id>/mobilemoneypayment/confirmed',publicviews.rent_mobilemoney_payment_confirmed,name="rent-mobilemoney-payment-confirmed"),
    path('public/equipments/rent/<int:rent_id>/mobilemoneypayment/canceled',publicviews.rent_mobilemoney_payment_canceled,name="rent-mobilemoney-payment-canceled"),
    path('public/equipments/rent/mobilemoneypayment/check/<int:payment_id>/',publicviews.rent_mobilemoney_payment_check,name="rent-mobilemoney-payment-check"),
    path('public/register/',publicviews.register_new,name="register"),
    path('public/termsofuse/',publicviews.terms_of_use,name="terms-of-use"),
    path('public/privacypolicy/',publicviews.privacy_policy,name="privacy-policy"),
    path('public/register/provider/',publicviews.register_provider,name="register-provider"),
    path('public/providers/',publicviews.providers,name="providers"),
    path('public/providers/<int:provider_id>',publicviews.provider_equipments,name="provider-equipments-list"),
    path('public/login/',publicviews.login_view,name="login"),
    path('public/logout/',publicviews.logout_view,name="logout"),
    #path('public/register/confirm/<int:user_id>/',publicviews.confirm_registration,name="register-confirm"),
    path('public/register/confirm/',publicviews.confirm_registration,name="register-confirm"),
    #path('public/register/success/<int:user_id>/',publicviews.registration_success,name="register-success"),
    path('public/register/success/',publicviews.registration_success,name="register-success"),
    path('public/account/changepassword/',publicviews.change_password,name="change-password"),
    path('public/dashboard/',publicviews.dashboard,name="dashboard"),
    path('public/dashboard/settings/',publicviews.dashboard_settings,name="dashboard-settings"),
    path('public/dashboard/wallet/',publicviews.dashboard_wallet,name="dashboard-wallet"),
    path('public/dashboard/cashin/',publicviews.dashboard_cashin,name="dashboard-cashin"),
    path('public/dashboard/cashout/',publicviews.dashboard_cashout,name="dashboard-cashout"),
    path('public/dashboard/equipments/',publicviews.dashboard_equipments_list,name="dashboard-equipments-list"),
    path('public/dashboard/equipments/add/',publicviews.dashboard_equipment_add,name="dashboard-equipment-add"),
    path('public/dashboard/equipments/<int:equipment_id>/update/',publicviews.dashboard_equipment_update,name="dashboard-equipment-update"),

    path('adminmodule/',adminviews.admin_dashboard,name="admin-dashboard"),
    path('adminmodule/stats/',adminviews.admin_stats,name="admin-stats"),
    path('adminmodule/categories/',adminviews.admin_categories_list,name="admin-categories-list"),
    path('adminmodule/categories/add/',adminviews.admin_category_add,name="admin-category-add"),
    path('adminmodule/categories/<int:categoryId>/update/',adminviews.admin_category_update,name="admin-category-update"),
    path('adminmodule/categories/<int:categoryId>/delete/',adminviews.admin_category_delete,name="admin-category-delete"),
    path('adminmodule/stats/users/',adminviews.admin_users_stats,name="admin-users-stats"),
    path('adminmodule/stats/rents/',adminviews.admin_rents_stats,name="admin-rents-stats"),
    path('adminmodule/stats/revenue/',adminviews.admin_revenue,name="admin-revenue"),
    path('adminmodule/providers',adminviews.admin_providers_list,name="admin-providers-list"),
    path('adminmodule/equipments/stats/',adminviews.admin_equipments_stats,name="admin-equipments-stats"),
    path('adminmodule/categories/<category_id>/equipments/',adminviews.admin_category_equipments,name="admin-category-equipments"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
