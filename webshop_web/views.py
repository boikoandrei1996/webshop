from django.shortcuts import render, redirect
from models import *
from forms import *
from webshop_engine.send_email import send_async as send


def __read_cart(user_id):
    try:
        cart = CartModel.objects.get(id_user=user_id)
        count = cart.total_amount
        sum_price = cart.total_price
    except CartModel.DoesNotExist:
        count = 0
        sum_price = 0
    return count, sum_price


def __info_about_order(client, new_order):
    info_client = u'client: {0} {1}\naddress: {2} {3}\nmobile: {4}\ncomment: {5}\n'.format(
        client.id, client.name,
        client.city, client.address,
        client.mobile,
        client.comment
    )

    products_info = []
    for pair in CartProductMap.objects.filter(cart=new_order.cart):
        prod_info = u'\n\t{0}. {1} amount: {2} price pre one: {3}'.format(
            pair.product.id, pair.product.title, pair.amount, pair.price
        )
        products_info.append(prod_info)

    info_cart = u'cart: {0} total amount: {1} total price: {2}\nProducts:'.format(
        new_order.cart.id, new_order.cart.total_amount, new_order.cart.total_price
    )

    text = info_client + info_cart + ''.join(products_info)
    return text


def __base_settings(result_dict, user_id):
    count, sum_price = __read_cart(user_id)
    result_dict['count'] = count
    result_dict['sum'] = sum_price
    return result_dict


def __get_or_create_cart_by_id_user(user_id):
    try:
        cart = CartModel.objects.get(id_user=user_id)
    except CartModel.DoesNotExist:
        cart = CartModel()
        cart.id_user = user_id
        cart.total_price = 0
        cart.total_amount = 0
        cart.save()

    return cart


def home(request):
    #print '---------------------'
    #print request.COOKIES
    #print '---------------------'
    #print request.session
    ##print '---------------------'
    #print request.user
    #print '---------------------'

    #user_id = request.session.session_key
    #print user_id
    #print type(user_id)

    user_id = int(request.session.get('_auth_user_id'))

    max_slide_count = 5
    slide_active = 3
    max_photo_on_slide = 3

    slide_items = []
    products = ProductModel.objects.get_queryset().order_by('price')
    for prod in products[:max_slide_count]:
        images = []
        for pair in ImageGalleryMap.objects.filter(gallery=prod.gallery)[:max_photo_on_slide]:
            images.append(pair.image.path)

        slide_items.append((prod, images))

    result_dict = dict()
    result_dict = __base_settings(result_dict, user_id)
    result_dict['slide_items'] = slide_items
    result_dict['slide_active'] = slide_active
    result_dict['categories'] = CategoryModel.objects.all()
    return render(request, "webshop/home.html", result_dict)


def category(request, id_category):
    try:
        cat = CategoryModel.objects.get(id=id_category)
    except CategoryModel.DoesNotExist:
        return redirect('/')

    products_from_category = []
    for pair in CategoryProductMap.objects.filter(category=cat):
        products_from_category.append(pair.product)

    user_id = int(request.session.get('_auth_user_id'))

    result_dict = dict()
    result_dict = __base_settings(result_dict, user_id)
    result_dict['category_title'] = cat.title
    result_dict['products'] = products_from_category

    return render(request, "webshop/category.html", result_dict)


def product(request, id_product):
    try:
        prod = ProductModel.objects.get(id_product=id_product)
    except CategoryModel.DoesNotExist:
        return redirect('/')

    try:
        cat = CategoryProductMap.objects.get(product=prod).category
        cat_title = cat.title
        cat_id = cat.id
    except CategoryProductMap.DoesNotExist:
        return redirect('/')

    queryset_images = ImageGalleryMap.objects.filter(gallery=prod.gallery)
    images = []
    for pair in queryset_images:
        images.append(pair.image.path)

    queryset_recalls = ProductRecallMap.objects.filter(product=prod)
    recalls = []
    for pair in queryset_recalls:
        recalls.append(pair.recall)

    user_id = int(request.session.get('_auth_user_id'))

    result_dict = dict()
    result_dict = __base_settings(result_dict, user_id)
    result_dict['category_title'] = cat_title
    result_dict['category_id'] = cat_id
    result_dict['product'] = prod
    result_dict['images'] = images
    result_dict['recalls'] = recalls

    return render(request, "webshop/product.html", result_dict)


def add_to_cart(request, id_product):
    if request.method == 'POST':
        try:
            prod = ProductModel.objects.get(id_product=int(id_product))
        except ProductModel.DoesNotExist:
            return redirect('/')

        user_id = int(request.session.get('_auth_user_id'))
        cart = __get_or_create_cart_by_id_user(user_id)

        cart.total_price += prod.price
        cart.total_amount += 1
        cart.save()

        try:
            pair = CartProductMap.objects.get(product=prod, cart=cart)
            pair.amount += 1
        except CartProductMap.DoesNotExist:
            pair = CartProductMap()
            pair.product = prod
            pair.cart = cart
            pair.price = prod.price
            pair.amount = 1
        pair.save()

        result_dict = dict()
        result_dict = __base_settings(result_dict, user_id)
        result_dict['cart_product_pairs'] = CartProductMap.objects.filter(cart=cart)
        result_dict['cart'] = cart

        return render(request, 'webshop/package_order.html', result_dict)


def delete_from_cart(request, id_product):
    if request.method == 'POST':
        title = request.POST['product_title_' + str(id_product)]
        price = float(request.POST['product_price_' + str(id_product)])
        amount = int(request.POST['product_amount_' + str(id_product)])

        try:
            prod = ProductModel.objects.get(id_product=int(id_product))
        except ProductModel.DoesNotExist:
            return redirect('/')

        user_id = int(request.session.get('_auth_user_id'))
        try:
            cart = CartModel.objects.get(id_user=user_id)
        except CartModel.DoesNotExist:
            return redirect('/')

        try:
            pair = CartProductMap.objects.get(product=prod, cart=cart)
            pair.delete()
            cart.total_price -= (price * amount)
            cart.total_amount -= amount
            cart.save()
        except CartProductMap.DoesNotExist:
            pass

        result_dict = dict()
        result_dict = __base_settings(result_dict, user_id)
        result_dict['cart_product_pairs'] = CartProductMap.objects.filter(cart=cart)
        result_dict['cart'] = cart

        return render(request, 'webshop/package_order.html', result_dict)


def view_cart(request):
    user_id = int(request.session.get('_auth_user_id'))
    cart = __get_or_create_cart_by_id_user(user_id)

    result_dict = dict()
    result_dict = __base_settings(result_dict, user_id)
    result_dict['cart_product_pairs'] = CartProductMap.objects.filter(cart=cart)
    result_dict['cart'] = cart
    result_dict['form_client'] = ClientForm()

    return render(request, 'webshop/package_order.html', result_dict)


def order(request, id_cart):
    if request.method == 'POST':
        form_client = ClientForm(request.POST)
        if form_client.is_valid():
            client = ClientModel()
            client.name = form_client.cleaned_data['name']
            client.city = form_client.cleaned_data['city']
            client.address = form_client.cleaned_data['address']
            client.mobile = form_client.cleaned_data['mobile']
            client.comment = form_client.cleaned_data['comment']
            client.save()

            new_order = OrderModel()
            new_order.cart = CartModel.objects.get(id=int(id_cart))
            new_order.client = client
            new_order.status = 'processing'
            new_order.save()

            text = __info_about_order(client, new_order)

            send(sender='BoikoAndrei1996@gmail.com',
                 recipient='boikoandrei1996@mail.ru',
                 user_name='BoikoAndrei1996@gmail.com',
                 user_passwd='17131519bsuir',
                 message_title='---New order on Case.by---',
                 text=text)

            return redirect('/')
        else:
            user_id = int(request.session.get('_auth_user_id'))
            cart = __get_or_create_cart_by_id_user(user_id)

            result_dict = dict()
            result_dict = __base_settings(result_dict, user_id)
            result_dict['cart_product_pairs'] = CartProductMap.objects.filter(cart=cart)
            result_dict['cart'] = cart
            result_dict['form_client'] = form_client

            return render(request, 'webshop/package_order.html', result_dict)

    else:
        return redirect('/cart')
