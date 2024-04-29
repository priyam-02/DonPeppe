import random

from django.conf import settings
from django.contrib import messages

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import bookform
from .models import City, Register, Order_details, Orderitem, Cart
from adminapp.models import Product, sub, Cat


def hed2(request):
    v = request.user.id
    return render(request, 'hed2.html', {'v': v})


def index(request):
    return render(request, 'index.html')


def register(request):
    c = City.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        password = request.POST['password']
        c_password = request.POST['c_password']
        city_id = request.POST['city_id']

        if password == c_password:
            if Register.objects.filter(email=email).exists():
                print('email taken')
                messages.error(request, "Email Already Taken")
            else:


                user = Register(name=name, email=email, contact=contact, address=address,
                                password=password,
                                c_password=c_password, city_id_id=city_id)
                user.save()
                return redirect('/login/')
        else:
            messages.error(request, "password not matched")
    else:
        pass
    return render(request, 'register.html', {'c': c})


def login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = Register.objects.filter(password=password, email=email).count()
        print("____", user)

        if user == 1:
            user = Register.objects.filter(password=password, email=email)
            for l1 in user:
                request.session['email'] = l1.email
                request.session['id'] = l1.id
                print(l1.email)
                request.session['id'] = l1.id
                print(l1.id)
                return redirect('/')
        else:
            messages.error(request, 'Invalid email and password')
            return render(request,'login.html')
    else:
        return render(request,'login.html')


def logout(request):
    try:
        del request.session['id']
        return redirect('/login/')
    except:
        pass


def forgot(request):
    if request.method == 'POST':
        otp1 = random.randint(10000, 99999)
        e = request.POST.get('email')
        print("---------------", e)
        request.session['email'] = e
        obj = Register.objects.filter(email=e).count()
        if obj == 1:
            data = Register.objects.filter(email=e).update(otp=otp1)
            request.session['email'] = e
            subject = ' Verification code'
            message = str(otp1)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list, data)
            return redirect('/resetpw/')
        else:
            messages.error(request, 'Invalid emailaddress')
    return render(request, 'forgot.html')


def resetpw(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST['password']
        c_password = request.POST['c_password']
        user = Register.objects.filter(otp=otp).update(password=password, c_password=c_password)
        print("____", user)
        if password == c_password:
            user = Register.objects.filter(otp=otp)
            for l1 in user:
                request.session['otp'] = l1.otp
                request.session['id'] = l1.id
                print(l1.otp)
                request.session['id'] = l1.id
                request.session.flush()
                return redirect('/login/')
            else:
                messages.error(request, 'OTP does not match')
        else:
            messages.error(request, 'password does not match')
            return render(request, 'resetpw.html')
    else:
        pass
    return render(request, 'resetpw.html')



def menuf(request):
    v = request.session['id']
    u = Register.objects.get(id=v)
    cat = Cat.objects.all()
    p = Product.objects.all().order_by('Category_id_id')
    paginator = Paginator(p, 6)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    if 'q' in request.GET:
        q = request.GET.get('q')
        multiple_q = Q(Q(proname__icontains=q) | Q(price__icontains=q))
        page.object_list = Product.objects.filter(multiple_q)

    else:

        paginator = Paginator(p, 6)
        page_num = request.GET.get('page')
        page = paginator.get_page(page_num)
    if 'min_price' in request.GET:
        filter_price1 = request.GET.get('min_price')
        filter_price2 = request.GET.get('max_price')
        if filter_price1 == '':
            filter_price1 = 0
        page.object_list = Product.objects.filter(price__range=(filter_price1, filter_price2)).order_by(
            'Category_id_id')
    return render(request, 'menuf.html', {'cat': cat, 'p': p, 'u': u, 'paginator': paginator.count, 'page': page})


def menu(request, id):
    c = request.session['id']
    p1 = Register.objects.get(id=c)
    cat = Cat.objects.all()
    s1 = Product.objects.filter(sub_id=id)
    p = Product.objects.all()
    s = sub.objects.get(id=id)
    return render(request, 'menu.html', {'cat': cat, 'p': p, 's1': s1, 'p1': p1, 's': s})


def menuc(request, id):
    c = request.session['id']
    p1 = Register.objects.get(id=c)
    cat = Cat.objects.all()
    s1 = Product.objects.filter(sub_id=id)
    p = Product.objects.all()
    s = sub.objects.get(id=id)
    return render(request, 'menuc.html', {'cat': cat, 'p': p, 's1': s1, 'p1': p1, 's': s})


def cart(request):
    if request.method == 'POST':
        c = request.session['id']
        p1 = Register.objects.get(id=c)


        # r = request.POST['customer']
        p = request.POST['productd']

        q = request.POST['quantity']

        pr = request.POST.get('price')
        # pro=Product.objects.get(id=c)

        # cart_item =  Cart.objects.filter(customer=p1,productd_id=pro)
        # if cart_item:
        #     for i in cart_item:

        #

        # cart=request.POST.get('cart_id')
        # for i in pro:
        #     cart, created = Cart.objects.get_or_create(customer=p1, productd=i, completed=False)
        cart, created = Cart.objects.get_or_create(customer=p1, productd_id=p, completed=False)
        if Orderitem.objects.filter(productd_id=p, customer=p1):
            q1 = request.POST.get('quantity')

            cartitem = Orderitem.objects.filter(productd_id=p).update(quantity=q1)


        else:
            # productd=request.POST['productd']
            # r=request.session.get('r')
            # items = Orderitem.objects.get(list(r.keys()))
            # instance = Order_details.objects.create(item=items)
            #
            # for user in items:
            #     instance.item.add(user)
            # instance.save()

            cartitem, created = Orderitem.objects.get_or_create(customer=p1, cart=cart, productd_id=p, price=pr,
                                                                quantity=q)
            cartitem.save()

    return redirect('/showcart/')


def showcart(request):
    r1 = request.session['id']
    p1 = Register.objects.get(id=r1)
    c = Orderitem.objects.filter(customer_id=p1)
    pay = Orderitem.objects.all()
    cartit = Cart(request)
    amount = 0
    total_amount = 0
    shipping_amount = 0
    cart_item = Orderitem.objects.filter(customer_id=p1)
    if cart_item:
        for i in cart_item:
            temp_amount = int(i.quantity * i.productd.price)
            print('---', temp_amount)
            amount += temp_amount
            print('--------', temp_amount)
            total_amount = amount + shipping_amount
    # cart, created = Cart.objects.get_or_create(customer=p1, completed=False)
    # cartitems = cart.Orderitem_set.all()
    # else:
    #     cartitems = []
    #     cart = {"get_cart_total": 0, "get_itemtotal": 0}
    return render(request, 'cart.html',
                  {'c': c, 'r1': r1,'p1':p1, 'pay': pay, 'total_amount': total_amount, 'cart': cart, 'cartit': cartit})


def removecart(request, id):
    c = Orderitem.objects.get(id=id)
    c.delete()
    return redirect('/showcart/')


def checkout(request):
    c = request.session['id']
    p1 = Register.objects.get(id=c)
    pay = Orderitem.objects.filter(customer=c)
    cr = Cart.objects.filter(customer=c)
    amount = 0
    total_amount = 0
    shipping_amount = 0
    cart_item = Orderitem.objects.filter(customer=c)
    if cart_item:
        for i in cart_item:
            temp_amount = int(i.quantity * i.productd.price)
            print('---', temp_amount)
            amount += temp_amount
            print('--------', temp_amount)
            total_amount = amount + shipping_amount
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        city_id = request.POST['city_id']
        # pin = request.POST['pin']
        price = request.POST.get('price')
        payment = request.POST['payment']
        o = request.POST.get('oder')
        customer = request.POST['customer']
        cart = request.POST.get('cart')
        if Order_details.objects.filter(cart_id=cart):
            cartitem = Order_details.objects.filter(cart_id=cart).update(name=name, email=email, contact=contact,
                                                                         address=address, city_id=city_id,
                                                                         payment=payment, customer_id=customer,
                                                                         price=price, cart_id=cart)
        # productd=request.POST['productd']
        # r=request.session.get('r')
        # items = Orderitem.objects.get(list(r.keys()))
        # instance = Order_details.objects.create(item=items)
        #
        # for user in items:
        #     instance.item.add(user)
        # instance.save()
        else:
            user = Order_details(name=name, email=email, contact=contact, address=address, city_id=city_id,
                                 payment=payment, customer_id=customer, price=price, cart_id=cart)
            user.save()
        return redirect('/payments/')
    else:
        return render(request, 'checkout.html', {'p1': p1, 'pay': pay, 'total_amount': total_amount, 'cr': cr})


def pd(request, id):
    c = request.session['id']
    p1 = Register.objects.get(id=c)

    s = Product.objects.get(id=id)
    r = Product.objects.filter(sub_id=s.sub_id).exclude(id=id)[:4]

    return render(request, 'pd.html', {'c': c, 'p1':p1, 's': s, 'r': r})


def service(request):

    return render(request, 'ourservices.html')


def team(request):

    return render(request, 'ourteam.html')


def history(request):

    return render(request, 'ourhistory.html')


def booktable(request):
    return render(request, 'book1.html')


def thankyou(request):
    c = request.session['id']
    p1 = Register.objects.get(id=c)

    return render(request, 'thankyou.html', {'p1': p1})


def bookt2(request):
    c = request.session['id']
    p1 = Register.objects.get(id=c)

    if request.method == 'POST':
        ct = bookform(request.POST)
        if ct.is_valid():
            try:
                ct.save()
                return redirect('/thankyou/')
            except:
                pass
        else:
            pass
    else:
        ct = bookform()
    return render(request, 'book2.html', {'p1': p1, 'ct': ct})


def contact(request):

    return render(request, 'contact.html')


def payments(request):
    c = request.session['id']
    p = Order_details.objects.all().filter(customer=c).order_by('-id')[:1]
    v=Orderitem.objects.filter(customer=c)
    amount = 0
    total_amount = 0
    shipping_amount = 90
    cart_item = Orderitem.objects.filter(customer=c)
    if cart_item:
        for i in cart_item:
            temp_amount = int(i.quantity * i.productd.price)
            print('---', temp_amount)
            amount += temp_amount
            print('--------', temp_amount)
            total_amount = amount + shipping_amount


    return render(request,'orderconfirm1.html',{'c':c,'p':p,'v':v,'total_amount':total_amount,'shipping_amount':shipping_amount,'amount':amount})

# PDF Generate
from django.http import HttpResponse
from django.views.generic import View

# importing get_template from loader
from django.template.loader import get_template

# import render_to_pdf from util.py
from .utils import render_to_pdf


# Creating our view, it is a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template

        c = request.session['id']
        p = Order_details.objects.all().filter(customer=c).order_by('-id')[:1]
        v = Orderitem.objects.filter(customer=c)
        amount = 0
        total_amount = 0
        shipping_amount = 90
        cart_item = Orderitem.objects.filter(customer=c)
        if cart_item:
            for i in cart_item:
                temp_amount = int(i.quantity * i.productd.price)
                print('---', temp_amount)
                amount += temp_amount
                print('--------', temp_amount)
                total_amount = amount + shipping_amount
        data = {
            request.session.get('name'),
            request.session.get('cart.cart_id'),
            request.session.get('id'),
            request.session.get('ordered_date'),
            request.session.get('address'),
            request.session.get('productd.pimg'),
            request.session.get('productd.proname'),
            request.session.get('quantity'),
            request.session.get('total'),
            request.session.get('amount'),
            request.session.get('shipping_amount'),
            request.session.get('total_amount'),
        }
        pdf = render_to_pdf('invoice.html', {'data': data, 'p': p, 'v': v, 'total_amount': total_amount,
                                             'shipping_amount': shipping_amount, 'amount': amount})

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

# Create your views here.
