from django.urls import path
from .views import RealEstateManageView, RealEstateDetailView, RealEstateListView

urlpatterns = [
    path('realestates/manage', RealEstateManageView.as_view(), name="realestate_manage"),
    path('realestates/detail', RealEstateDetailView.as_view(), name="realestate_detail"),
    path('realestates/lists', RealEstateListView.as_view(), name="realestate_lists")
]
