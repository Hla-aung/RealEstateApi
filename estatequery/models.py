from django.db import models
from django.conf import settings

CURRENCY_CHOICES = (
    ("USD", "US Dollar"),
    ("THB", "Thai Baht"),
    ("MMK", "Myanmar Kyat"),
)
AREA_CHOICES = (
    ("sqft", "Square Feet"),
    ("acres", "Acres"),
)
RENT_OR_SALE_CHOICES = (
    ("rent", "For Rent"),
    ("sale", "For Sale"),
)
TYPE_CHOICES = (
    ("apartment", "Apartment"),
    ("condo", "Condo"),
    ("town_house", "Town House"),
    ("house", "House")
)
# Create your models here.
class RealEstate(models.Model):
    realtor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    area_value = models.DecimalField(decimal_places=2, max_digits=6)
    area_unit = models.CharField(max_length=5, choices=AREA_CHOICES)
    rent_or_sale_status = models.CharField(max_length=4, choices=RENT_OR_SALE_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_available = models.BooleanField(default=True)
    available_date = models.DateTimeField(blank=True, null=True)
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    is_parking = models.BooleanField(default=False)
    facilities = models.TextField(blank=True, null=True)
    nearby_places = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    main_photo = models.ImageField(upload_to="estatequery/", null=True)
    photo_one = models.ImageField(upload_to="estatequery/", null=True) 
    photo_two = models.ImageField(upload_to="estatequery/", null=True)
    photo_three = models.ImageField(upload_to="estatequery/", null=True)
    is_published = models.BooleanField(default=False)

    # To delete images in media file
    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_one.storage.delete(self.photo_one.name)
        self.photo_two.storage.delete(self.photo_two.name)
        self.photo_three.storage.delete(self.photo_three.name)

    def __str__(self) -> str:
        return self.title