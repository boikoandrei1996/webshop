import json
import os
import django
from django.db.utils import IntegrityError

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

sys.path.append('/home/andrei/pyproj/webshop/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'webshop_site.settings'
django.setup()

from webshop_web.models import ImageModel, ImageGalleryMap, GalleryModel
from webshop_web.models import CategoryModel, ProductModel, CategoryProductMap


def _save_img(path):
    image = ImageModel()
    image.path = path
    try:
        image.save()
        print "add image: {0}".format(path)
    except IntegrityError:
        image = ImageModel.objects.get(path=path)
        print "get from db image: {0}".format(path)
    except Exception as e:
        print str(type(e)) + ">>>" + e.message
        raise

    return image


def _save_gallery(gallery_name, file_name, image):
    if file_name.startswith("1."):
        gallery = GalleryModel()
        gallery.name = gallery_name
        gallery.cover_image = image
        try:
            gallery.save()
            print "add gallery: {0}".format(gallery_name)
        except IntegrityError:
            gallery = GalleryModel.objects.get(name=gallery_name)
            print "get from db gallery: {0}".format(gallery_name)
        except Exception as e:
            print str(type(e)) + " >>> " + e.message
            raise
    else:
        gallery = GalleryModel.objects.get(name=gallery_name)

    return gallery


def _save_img_gallery_map(image, gallery):
    try:
        ImageGalleryMap.objects.get(image=image, gallery=gallery)
        return False
    except ImageGalleryMap.DoesNotExist:
        pass

    img_to_gallery = ImageGalleryMap()
    img_to_gallery.image = image
    img_to_gallery.gallery = gallery
    try:
        img_to_gallery.save()
    except Exception as e:
        print str(type(e)) + " >>> " + e.message
        raise

    return True


def write_media(path_start_directory, dirnames_for_skip={'wrapper'}):
    """
    function write images from start directory in database
    :param path_start_directory: path to directory, where content search
    :param dirnames_for_skip: iterable object with directory, which should be skip
    :return: None
    """
    for filename in os.listdir(path_start_directory):
        if filename in set(dirnames_for_skip):
            continue

        current_path = os.path.join(path_start_directory, filename)

        if os.path.isdir(current_path):
            write_media(current_path)
        elif os.path.isfile(current_path):
            before, after = current_path.split('static')
            image = _save_img('/static' + after)

            gallery_name = path_start_directory.split("/")[-1]
            gallery = _save_gallery(gallery_name, filename, image)

            if not _save_img_gallery_map(image, gallery):
                continue


def _save_category(item):
    cat = CategoryModel()
    title = item['title']
    cat.title = title
    cat.desc = item['desc']
    gallery_name = item["gallery_name"]
    try:
        cat.gallery = GalleryModel.objects.get(name=gallery_name)
    except GalleryModel.DoesNotExist:
        print "not found gallery name {0}".format(gallery_name)
        raise

    try:
        cat.save()
        print "add category: {0}".format(title)
    except IntegrityError:
        cat = CategoryModel.objects.get(title=title)
        print "get from db category: {0}".format(title)
    except Exception as e:
        print str(type(e)) + ">>>" + e.message
        raise

    return cat


def _save_product(item):
    prod = ProductModel()
    title = item['title']
    prod.id_product = item['id']
    prod.title = title
    prod.price = item['price']
    prod.amount = item['amount']
    prod.rating = item['rating']
    prod.desc = item['desc']
    gallery_name = item["gallery_name"]
    try:
        prod.gallery = GalleryModel.objects.get(name=gallery_name)
    except GalleryModel.DoesNotExist:
        print "not found gallery name {0}".format(gallery_name)
        raise

    try:
        prod.save()
        print "add product: {0}".format(title)
    except IntegrityError:
        prod = ProductModel.objects.get(id_product=item['id'])
        print "get from db product: {0}".format(title)
    except Exception as e:
        print str(type(e)) + ">>>" + e.message
        raise

    return prod


def _save_cat_product_map(category, prod):
    try:
        CategoryProductMap.objects.get(category=category, product=prod)
        return False
    except CategoryProductMap.DoesNotExist:
        pass

    prod_cat_map = CategoryProductMap()
    prod_cat_map.product = prod
    prod_cat_map.category = category
    try:
        prod_cat_map.save()
    except Exception as e:
        print str(type(e)) + ">>>" + e.message
        raise

    return True


def write_item(filename_categories, filename_products):
    """
    function write categories and product from json file to database
    :param filename_categories: json file with information about categories
    :param filename_products: json file with information about products
    :return: None
    """
    with open(filename_products, 'r') as file_products:
        data_products = json.load(file_products)

    for item in data_products:
        prod = _save_product(item)

    with open(filename_categories, 'r') as file_cat:
        data_categories = json.load(file_cat)

    for item in data_categories:
        category = _save_category(item)

        for product_id in item['products']:
            try:
                prod = ProductModel.objects.get(id_product=int(product_id))
            except ProductModel.DoesNotExist:
                print "not found product with id {0}".format(product_id)
                raise

            _save_cat_product_map(category, prod)


def main():
    import webshop_site.settings as settings
    write_media(os.path.join(settings.BASE_DIR, "webshop_web/static/content"))
    filename_cat = os.path.join(settings.BASE_DIR, "webshop_web/static/categories.json")
    filename_prod = os.path.join(settings.BASE_DIR, "webshop_web/static/products.json")
    write_item(filename_cat, filename_prod)


if __name__ == '__main__':
    main()
