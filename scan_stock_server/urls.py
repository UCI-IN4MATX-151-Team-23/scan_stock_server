"""scan_stock_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from web import views as web_views

urlpatterns = [
    path('v1/user', web_views.create_user),
    path('v1/user/<int:user_id>', web_views.get_user_by_id),
    path('v1/user/<int:user_id>/items', web_views.get_user_items_by_id),
    path('v1/user/login', web_views.get_user_id),
    path('v1/item', web_views.create_item),
    path('v1/item/<int:item_id>', web_views.ItemView.as_view()),
    # TODO: write Django fixtures for item templates
    # https://docs.djangoproject.com/en/4.1/howto/initial-data/#providing-data-with-fixtures
    path('v1/item_template', web_views.get_item_templates),
    path('v1/item_template/<int:item_template_id>', web_views.get_item_template_by_id),
    # path('admin/', admin.site.urls),
]
