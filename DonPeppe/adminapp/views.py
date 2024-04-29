import random
import sys

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import cityform, catform, subcatform, proform
from .functions import handle_uploaded_file
from .models import Signup, Cat, sub, Product
from clientapp.models import City, Register, booktable, Orderitem, Order_details



def indexadmin(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    return render(request, 'indexadmin.html', {'v': v, 'u': u})


def header1(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    return render(request, 'header1.html', {'v': v, 'u': u})


def signup(request):
    c = City.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if Signup.objects.filter(email=email).exists():
            print('email taken')
            messages.error(request, "Email Already Taken")
        else:
            user = Signup(name=name, email=email, password=password)
            user.save()
            return redirect('/adminpanel/signin/')
    else:
        pass
    return render(request, 'adminsignup.html', {'c': c})


def signin(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = Signup.objects.filter(password=password, email=email).count()
        print("____", user)
        if user == 1:
            user = Signup.objects.filter(password=password, email=email)
            for l1 in user:
                request.session['email'] = l1.email
                request.session['id'] = l1.id
                print(l1.email)
                request.session['id'] = l1.id
                return redirect('/adminpanel/indexadmin/')
        else:
            messages.error(request, 'Invalid email and password')
        return render(request, 'adminsignin.html')
    else:
        return render(request, 'adminsignin.html')


def logoutadmin(request):
    try:
        del request.session['id']
        return redirect('/adminpanel/signin/')
    except:
        pass


def forgotad(request):
    if request.method == 'POST':
        otp1 = random.randint(10000, 99999)
        e = request.POST.get('email')
        print("---------------", e)
        request.session['email'] = e
        obj = Signup.objects.filter(email=e).count()
        if obj == 1:
            data = Signup.objects.filter(email=e).update(otp=otp1)
            request.session['email'] = e
            subject = ' Verification code'
            message = str(otp1)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]
            send_mail(subject, message, email_from, recipient_list, data)
            return redirect('/adminpanel/resetad/')
        else:
            messages.error(request, 'Email does not match')
    else:
        pass
    return render(request, 'forgotad.html')


def resetad(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST['password']
        c_password = request.POST['c_password']
        user = Signup.objects.filter(otp=otp).update(password=password, c_password=c_password)
        print("____", user)
        if password == c_password:
            user = Signup.objects.filter(otp=otp)
            for l1 in user:
                request.session['otp'] = l1.otp
                request.session['id'] = l1.id
                print(l1.otp)
                request.session['id'] = l1.id
                request.session.flush()
                return redirect('/adminpanel/signin/')
            else:
                messages.error(request, 'OTP does not match')
        else:
            messages.error(request, 'Password does not match')
            return render(request, 'resetad.html')
    else:
        pass
    return render(request, 'resetad.html')


def addcity(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    if request.method == 'POST':
        ct = cityform(request.POST)
        if ct.is_valid():
            try:
                ct.save()
                return redirect('/adminpanel/showcity/')
            except:
                pass
        else:
            pass
    else:
        ct = cityform()
    return render(request, 'addcity.html', {'ct': ct, 'u': u})


def showcity(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    city = City.objects.all()
    return render(request, 'showcity.html', {'city': city, 'u': u})


def editcity(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    city = City.objects.get(id=id)
    return render(request, 'editcity.html', {'city': city, 'u': u})


def updatecity(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    city = City.objects.get(id=id)
    form = cityform(request.POST, instance=city)
    if form.is_valid():
        form.save()
        return redirect('/adminpanel/showcity/')
    return render(request, 'editcity.html', {'city': city, 'u': u})


def deletecity(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    d = City.objects.get(id=id)
    d.delete()
    return redirect('/adminpanel/showcity/', {'u': u})


def category(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    if request.method == 'POST':
        c = catform(request.POST)
        if c.is_valid():
            try:
                c.save()
                return redirect('/adminpanel/showcat/')
            except:
                pass
        else:
            pass
    else:
        c = catform()

    return render(request, 'addcat.html', {'c': c, 'u': u})


def showcat(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.all()
    return render(request, 'showcat.html', {'cat': cat, 'u': u})


def editcat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.get(id=id)
    return render(request, 'editcat.html', {'cat': cat, 'u': u})


def updatecat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.get(id=id)
    form = catform(request.POST, instance=cat)
    if form.is_valid():
        form.save()
        return redirect('/adminpanel/showcat/')
    return render(request, 'editcat.html', {'cat': cat, 'u': u})


def deletecat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    d = Cat.objects.get(id=id)
    d.delete()
    return redirect('/adminpanel/showcat/', {'u': u})


def subcat(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    c = Cat.objects.all()
    if request.method == "POST":
        form = subcatform(request.POST)
        print("--------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/adminpanel/showsubcat/")
            except:
                print("--------", sys.exc_info())
    else:
        form = subcatform()
    return render(request, 'subcategory.html', {'form': form, 'c': c, 'u': u})


def showsubcat(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    s = sub.objects.all()
    # scat = Subcategory.objects.filter(category_id=id)
    return render(request, 'showsubcat.html', {'s': s, 'u': u})


def editsubcat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.all()
    s = sub.objects.get(id=id)
    return render(request, 'editsubcat.html', {'s': s, 'cat': cat, 'u': u})


def updatesubcat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    s = sub.objects.get(id=id)
    form = subcatform(request.POST, instance=s)
    if form.is_valid():
        form.save()
        return redirect('/adminpanel/showsubcat/')
    return render(request, 'editsubcat.html', {'s': s, 'u': u})


def deletesubcat(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    s = sub.objects.get(id=id)
    s.delete()
    return redirect('/adminpanel/showsubcat/', {'u': u})


def changepw(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    if request.method == 'POST':
        p = request.POST.get('password')
        print("---------------", p)
        request.session['password'] = p
        obj = Signup.objects.filter(password=p).count()
        if obj == 1:
            return redirect('/adminpanel/changepw1/')
        else:
            messages.error(request, 'password does not match')
    else:
        pass
    return render(request, 'changepw.html', {'u': u})


def changepw1(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    if request.method == 'POST':
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password == c_password:
            user = Signup.objects.filter(id=v).update(password=password, c_password=c_password)
            return redirect('/adminpanel/signin/')
        else:
            messages.error(request, 'password does not match')
    else:
        pass
    return render(request, 'changepw1.html', {'u': u})


def reservation(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    per = Register.objects.all()
    book = booktable.objects.all()
    return render(request, 'reservation.html', {'book': book, 'per': per, 'u': u})



def deletereserve(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)

    book = booktable.objects.get(id=id)
    book.delete()
    return redirect('/adminpanel/reservation/', {'u': u})

def addpro(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    c = Cat.objects.all()
    cities = sub.objects.all()
    if request.method == "POST":
        form = proform(request.POST, request.FILES)
        print("--------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['pimg'])

                form.save()
                return redirect("/adminpanel/prolist/")
            except:
                print("--------", sys.exc_info())
    else:
        form = proform()

    return render(request, 'addproduct.html', {'c': c, 'form': form, 'u': u, 'cities': cities})


def prolist(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.all()
    s = sub.objects.all()
    p = Product.objects.all().order_by('Category_id_id')
    return render(request, 'productlist.html', {'s': s, 'p': p, 'cat': cat, 'u': u})


def editpro(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    cat = Cat.objects.all()
    scat = sub.objects.all()
    p = Product.objects.get(id=id)
    return render(request, 'editpro.html', {'p': p, 'cat': cat, 'scat': scat, 'u': u})


def updatepro(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    p = Product.objects.get(id=id)
    form = proform(request.POST, request.FILES, instance=p)
    if form.is_valid():
        handle_uploaded_file(request.FILES['pimg'])
        form.save()
        return redirect('/adminpanel/prolist/')
    return render(request, 'editpro.html', {'p': p, 'u': u})


def deletepro(request, id):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    p = Product.objects.get(id=id)
    p.delete()
    return redirect('/adminpanel/prolist/', {'u': u})


def profile(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    c = City.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        city_id = request.POST['city_id']
        password = request.POST.get('password')
        img = request.FILES['img']
        handle_uploaded_file(request.FILES['img'])
        abcd = Signup.objects.filter(id=v).update(name=name, email=email, contact=contact, address=address,
                                                  city_id=city_id, img=img)
        return redirect('/adminpanel/vprofile/', {'abcd': abcd})

    else:
        return render(request, 'profile.html', {'v': v, 'u': u, 'c': c})


def vprofile(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    c = City.objects.all()
    s = Signup.objects.all()
    return render(request, 'vprofile.html', {'v': v, 'u': u, 'c': c, 's':s})




def load_sub(request):
    country_id = request.GET.get('Category_id')
    cities = sub.objects.filter(cat=country_id).order_by('name')
    return render(request, 'subcat_load.html', {'cities': cities})


def order1(request):
    v = request.session['id']
    u = Signup.objects.get(id=v)
    ot = Orderitem.objects.all()
    return render(request, 'order1.html', {'ot': ot, 'u': u})

def orderdetail1(request, id):
    v1 = request.session['id']
    u = Signup.objects.get(id=v1)
    c = request.session['id']
    p = Order_details.objects.filter(customer=c)
    # amount = 0
    # total_amount = 0
    shipping_amount = 90
    v = Orderitem.objects.get(id=id)

    # for i in v:
    temp_amount = int(v.quantity * v.productd.price)
    print('---', temp_amount)

    print('--------', temp_amount)
    total_amount = temp_amount + shipping_amount

    return render(request, 'orderdetail1.html',
                  {'c': c, 'p': p, 'v': v, 'u': u, 'total_amount': total_amount, 'shipping_amount': shipping_amount,
                   'temp_amount': temp_amount})


# Create your views here.
