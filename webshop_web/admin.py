from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ProductModel)
#admin.site.register(models.CategoryModel)
#admin.site.register(models.ImageModel)
#admin.site.register(models.GalleryModel)
admin.site.register(models.CartModel)
#admin.site.register(models.RecallModel)
admin.site.register(models.ClientModel)
#admin.site.register(models.CategoryProductMap)
#admin.site.register(models.ProductRecallMap)
admin.site.register(models.CartProductMap)
#admin.site.register(models.ImageGalleryMap)
admin.site.register(models.OrderModel)