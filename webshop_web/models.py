from __future__ import unicode_literals

from django.db import models


class ImageModel(models.Model):
    path = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "image_path: {0}".format(self.path)

    def __unicode__(self):
        return u"image_path: {0}".format(self.path)


class GalleryModel(models.Model):
    cover_image = models.ForeignKey(ImageModel)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "gallery: {0}".format(self.name)

    def __unicode__(self):
        return u"gallery: {0}".format(self.name)


class CategoryModel(models.Model):
    title = models.CharField(max_length=255, unique=True)
    gallery = models.ForeignKey(GalleryModel)
    desc = models.TextField()

    def __str__(self):
        return "category: {0}".format(self.title)

    def __unicode__(self):
        return u"category: {0}".format(self.title)


class ProductModel(models.Model):
    id_product = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    price = models.FloatField(db_index=True)
    amount = models.IntegerField()
    rating = models.FloatField(db_index=True)
    desc = models.TextField()
    gallery = models.ForeignKey(GalleryModel)

    def __str__(self):
        return "product: {0}".format(self.title)

    def __unicode__(self):
        return u"product: {0}".format(self.title)


class ClientModel(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    comment = models.TextField(max_length=255)

    def __str__(self):
        return "client: {0}".format(self.name)

    def __unicode__(self):
        return u"client: {0}".format(self.name)


class CartModel(models.Model):
    id_user = models.IntegerField(unique=True)
    total_price = models.FloatField()
    total_amount = models.IntegerField()

    def __str__(self):
        return "cart: {0}".format(self.id)

    def __unicode__(self):
        return u"cart: {0}".format(self.id)


class RecallModel(models.Model):
    author = models.CharField(max_length=50)
    text = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return "recall_from: {0}".format(self.author)

    def __unicode__(self):
        return u"recall_from: {0}".format(self.author)


# ----- Map Models -----
class ImageGalleryMap(models.Model):
    image = models.ForeignKey(ImageModel)
    gallery = models.ForeignKey(GalleryModel)

    def __str__(self):
        return "gallery '{0}' -> image '{1}'".format(self.gallery.name, self.image.path)

    def __unicode__(self):
        return u"gallery '{0}' -> image '{1}'".format(self.gallery.name, self.image.path)


class CategoryProductMap(models.Model):
    product = models.ForeignKey(ProductModel)
    category = models.ForeignKey(CategoryModel)

    def __str__(self):
        return "category '{0}' -> product '{1}'".format(self.category.title, self.product.title)

    def __unicode__(self):
        return u"category '{0}' -> product '{1}'".format(self.category.title, self.product.title)


class ProductRecallMap(models.Model):
    product = models.ForeignKey(ProductModel)
    recall = models.ForeignKey(RecallModel)

    def __str__(self):
        return "product '{0}' -> recall {1} by '{2}'".format(self.product.title, self.recall_id, self.recall.author)

    def __unicode__(self):
        return u"product '{0}' -> recall {1} by '{2}'".format(self.product.title, self.recall_id, self.recall.author)


class CartProductMap(models.Model):
    cart = models.ForeignKey(CartModel)
    product = models.ForeignKey(ProductModel)
    price = models.FloatField()
    amount = models.IntegerField()

    def __str__(self):
        return "cart '{0}' -> product '{1}'".format(self.cart_id, self.product.title)

    def __unicode__(self):
        return u"cart '{0}' -> product '{1}'".format(self.cart_id, self.product.title)


class OrderModel(models.Model):
    cart = models.ForeignKey(CartModel)
    client = models.ForeignKey(ClientModel)
    status = models.CharField(max_length=255)

    def __str__(self):
        return "order:{2}. cart '{0}' -> client '{1}'".\
            format(self.cart_id, self.client.name, self.id)

    def __unicode__(self):
        return u"order:{2}. cart '{0}' -> client '{1}'".\
                format(self.cart_id, self.client.name, self.id)
