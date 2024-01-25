from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout

from gapp.models import Product,Cart,Order,contactrecords
from django.db.models import Q
from django.http import HttpResponseServerError
import random,re
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

import razorpay




















# Create your views here.

def home(request):
    context={}
    #kid=request.user.id
    #print("id of logged in user:",kid)
    #print('result',request.user.is_authenticated) #this session_login authentication notice for privcy purpose
    
    
               #-----------#
  
   #this code filiter all active product of backend means backend la jepan active product ahet te user la display karte hi queary ok



    p=Product.objects.filter(is_active=True)
    context['availableProductinfo']=p
    return render(request,'index.html',context)
                #-----------#



def product_detail(request,pid):

    context={}
    k=Product.objects.filter(id=pid)
    context['availableProductinfo']=k
    return render(request,'product_details.html',context)   

                #-------------------- 

def p_cart(request):
    return render(request,'cart.html')

                 #----------------------






    

#############################################################################
                 #register start


def validate_password(request):
    password = request.GET.get('password')
    password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$')
    
    if password_pattern.match(password):
        return JsonResponse({'valid': True})
    else:
        return JsonResponse({'valid': False})
    


def register(request):
    context = {}

    if request.method == "POST":
        fname = request.POST['firstname']
        Lname = request.POST['LastName']
        email = request.POST['email']

        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']

        if uname == "" or upass == "" or ucpass == "" or fname == '' or Lname == '' or email == '':
            context['errmsg'] = "Field cannot be empty"
            return render(request, 'register.html', context)

        elif upass != ucpass:
            context['errmsg'] = "Password must be the same"
            return render(request, 'register.html', context)

        else:
            password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$')
            if not password_pattern.match(upass):
                context['perrmsg'] = (
                    "Password must contain at least one capital letter, "
                    "one number, one symbol, and be at least 8 characters long."
                )
                return render(request, 'register.html', context)

            try:
                u = User.objects.create(username=uname, first_name=fname, last_name=Lname, email=email)# u = User.objects.create(username=uname, email=uname)
                u.set_password(upass)
                u.save()
                context['success'] = "User created successfully"
                # Redirect to the login page after successful registration
                return redirect('/login')  # Update the URL as needed
            except Exception:
                context['errmsg'] = 'User already exists'
                return render(request, 'login.html', context)

    else:
        return render(request, 'register.html', context)

      
                #register ends
    
 #############################################################################   

def contact(request):
    if request.method=='GET':
        return render(request,'contact.html')
    
    else:
        n=request.POST['fname']
        m=request.POST['fnumber']
        e=request.POST['femail']
        msg=request.POST['fmsg']


        r=contactrecords.objects.create(name=n,mobile=m,email=e,message=msg)
        r.save()

        return redirect('/contact')
    
    #return render(request,'contact.html')
    


def about(request):
    return render(request,'about.html')



 #############################################################################
 #                                login start   

def u_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']

        if uname=='' or upass=='':
            context["errmsg"]="Filed cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
               
               #####################
               # login session part

               login(request,u)#  // start login function and store id of authenticated user into django_session table
               
               ####################


               return redirect('/home')
            else:
                context["errmsg"]="user name and password incorrect"
                return render(request,'login.html',context)


    else:
        return render(request,'login.html')
    
                                   # LOGIN END
     #############################################################################   



def u_logout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cdv):
    context={}
    c1=Q(is_active=True)
    c2=Q(cat=cdv)

    p=Product.objects.filter(c1 & c2)
    context['availableProductinfo']=p

    return render(request,'index.html',context)



def sort(request,sortvalue):
    context={}
    if sortvalue=='0':
        col='price'
    else:
        col='-price'


    p=Product.objects.filter(is_active=True).order_by(col)
    context['availableProductinfo']=p
    return render(request,'index.html',context)        
   #==============


def range(request):
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')

    # Check if both min_value and max_value are provided
    if min_value is not None and max_value is not None and min_value != '' and max_value != '':
        try:
            min_value = int(min_value)
            max_value = int(max_value)
        except ValueError:
            error_message = "Please enter valid numbers for min and max values."
            context = {
                'error_message': error_message
            }
            return render(request, 'index.html', context)

        c1 = Q(price__gte=min_value)
        c2 = Q(price__lte=max_value)
        c3 = Q(is_active=True)

        products = Product.objects.filter(c1 & c2 & c3)
        
        if not products:
            no_product_message = "No products available in the given range."
            context = {
                'no_product_message': no_product_message,
                'min_value': min_value,
                'max_value': max_value
            }
            return render(request, 'index.html', context)
        
        context = {
            'availableProductinfo': products
        }
        return render(request, 'index.html', context)
    else:
        error_message = "Please enter both min and max values."
        context = {
            'error_message': error_message
        }
        return render(request, 'index.html', context)



    

    #---------------
#def addtocart(request,pid):
    if request.user.is_authenticated:#means jya vyakti ne login kela ahe tech add to cart karu shaktil


        userid=request.user.id

        #USER ID DEFINATION : 
        #In Django, the request.user object represents the currently logged-in user, and request.user.id gives you the user ID of the authenticated user. 
        # The user ID is the primary key of the user in the auth_user table, which is a default table created by Django's authentication system.


        #print(pid)
        #print(userid)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(u[0])

        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()

        cd=Cart.objects.filter(uid=userid)

        context={}
        context['availableProductinfo']=cd
        return render(request,'cart.html',context)

    else:
        return redirect('/login')    
    
def addtocart(request,pid):
    
    if request.user.is_authenticated:
        userid=request.user.id 
        #print(pid)
        #print(userid)
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        pcount=Cart.objects.filter(q1 & q2)
        l=len(pcount)
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(p[0])
        context={}
        context['availableProductinfo']=p

        if l==0:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added in the Cart!!"

        else:
            context['msg']="Product already Exists in the cart!!"
            
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')




def viewcart(request):
    # Fetch cart items for the user
    c = Cart.objects.filter(uid=request.user.id)
    np = len(c)
    s = 0
    for x in c:
        s = s + x.pid.price * x.qty  # Calculate total cart value
        #x.delete()
    
   

    # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount

    # Check if user recently placed an order and delete the session variable
    if request.session.get('order_placed'):
        del request.session['order_placed']

    context = {
        'availableProductinfo': c,
        'total': s,
        'discounted_total': discounted_total,
        'discount_amount': discount_amount,
        'quantity': np
    }
    return render(request, 'cart.html', context)
      


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def remove_placeorder(request, cid):
    try:
        place_order_item = Cart.objects.get(id=cid)
        print("Found place_order_item:", place_order_item)  # Debug print
        place_order_item.delete()
    except Cart.DoesNotExist:
        print("Place order item not found for id:", cid)  # Debug print

    return redirect('/place_order')






#def updateqty(request,qv,cid):

    c=Cart.objects.filter(id=cid)

    


    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
        else:
            # If quantity becomes zero, delete the cart item from the database
            c.delete()


    return redirect('/viewcart')

def updateqty(request, qv, cid):
    cart_item = get_object_or_404(Cart, id=cid)

    if qv == "1":
        t = cart_item.qty + 1
        cart_item.qty = t
        cart_item.save()
    else:
        if cart_item.qty > 1:
            t = cart_item.qty - 1
            cart_item.qty = t
            cart_item.save()
        else:
            # If quantity becomes zero, delete the cart item from the database
            cart_item.delete()

    return redirect('/viewcart')





def place_order(request):
    #return render(request,'placeorder.html')
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
       


    orders=Order.objects.filter(uid=request.user.id)

    np=len(orders)
    s=0
    for x in orders:
        #print(x)
        #print(x.pid.price)
        #s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800
        s=s+x.pid.price*x.qty  #s=0+2200=2200 | s=2200+600=2800

     
      # Define the discount percentage based on the cart total value
    if s >= 1000:
        discount_percentage = 30  # 10% discount for cart value >= 1000
    else:
        discount_percentage = 15  # 5% discount for cart value < 1000

    # Calculate the discount amount based on the cart total and discount percentage
    discount_amount = (discount_percentage / 100) * s

    # Calculate the discounted total
    discounted_total = s - discount_amount


    context={}
    context['availableProductinfo']=orders
    context['total']=s
    context['discounted_total'] = discounted_total
    context['discount_amount'] = discount_amount
    context['quantity']=np


    return render(request,'placeorder.html',context)


# views.py

def back_to_cart(request):
    # Retrieve the user's cart items
    cart_items = Cart.objects.filter(uid=request.user.id)

    # Delete the order objects created in the place_order view
    orders = Order.objects.filter(uid=request.user.id)
    orders.delete()

    # Clear the user's cart
    #cart_items.delete()

    return redirect('/viewcart')  # Replace with the appropriate URL for your cart page



#def place_order(request):
    if request.method == 'POST':
        userid = request.user.id
        c = Cart.objects.filter(uid=userid)
        oid = random.randrange(1000, 9999)

        # Loop through cart items and create orders
        for x in c:
            o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
            o.save()
            x.delete()  # Remove cart items after creating orders

        # Set a session variable to indicate order placement
        request.session['order_placed'] = True

        # Redirect to a relevant page after placing the order
        return redirect('thank_you_page')

    # If request method is not POST, render the place order page
    return render(request, 'place_order.html')  # Update the template name










#------------------------------------------




#---------------------------------------------


from django.contrib import messages


def search_grocery(request):
    query = request.GET.get('q')
    groceries = []
    error_message = None

    if query:
        groceries = Product.objects.filter(name__icontains=query)
        if not groceries:
            error_message = "No products match your search query."

    context = {
        'availableProductinfo': groceries,
        'query': query,
        'error_message': error_message,
    }
    return render(request, 'index.html', context)



def search_range(request):
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')
    groceries = []
    error_message = None

    if min_value and max_value:
        groceries = Product.objects.filter(price__range=(min_value, max_value))
        if not groceries:
            error_message = f"No products available within the price range ₹{min_value} - ₹{max_value}."

    context = {
        'availableProductinfo': groceries,
        'min_value': min_value,
        'max_value': max_value,
        'error_message': error_message,
    }
    return render(request, 'index.html', context)


def search_range(request):
    min_value = request.GET.get('min')
    max_value = request.GET.get('max')
    
    try:
        if min_value == '':
            min_value = None
        else:
            min_value = float(min_value)
            
        if max_value == '':
            max_value = None
        else:
            max_value = float(max_value)
    except ValueError:
        # Handle the case where the input values are not valid numbers
        min_value = None
        max_value = None

    groceries = []
    error_message = None

    if min_value is not None and max_value is not None:
        groceries = Product.objects.filter(price__range=(min_value, max_value))
        if not groceries:
            error_message = f"No products available within the price range ₹{min_value} - ₹{max_value}."

    context = {
        'availableProductinfo': groceries,
        'min_value': min_value,
        'max_value': max_value,
        'error_message': error_message,
    }
    return render(request, 'index.html', context)


    

def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    oid = None  # Initialize oid outside the loop

    for x in orders:
        s = s + x.pid.price * x.qty
        oid = x.order_id  # Set oid inside the loop to capture the latest order_id

    if s >= 1000:
        discount_percentage = 30
    else:
        discount_percentage = 15

    discount_amount = (discount_percentage / 100) * s
    discounted_total = s - discount_amount

    client = razorpay.Client(auth=("rzp_test_3B81QaBdwia9gi", "IHcoKRAeAkgAVHvgSNfXG6iw"))

    data = {"amount": int(discounted_total * 100), "currency": "INR", "receipt": oid}
    payment = client.order.create(data=data)

    context = {
        "data": payment,
        "discounted_total": discounted_total  # Pass the discounted_total to the template
    }
    return render(request, "pay.html", context)
















    





    










    






