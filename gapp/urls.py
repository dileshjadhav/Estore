
from django.urls import path
from gapp import views

from django.conf import settings #this is for add image to thire respective product name  
from django.conf.urls.static import static #this is for add image to thire respective product name 


urlpatterns = [

    path('home/',views.home),
    path('pdetails/<pid>',views.product_detail),
    path('cart',views.p_cart),
    path('place_order',views.place_order),
    path('register',views.register),
    path('contact',views.contact),
    path('about',views.about),
    path('login',views.u_login),
    path('logout',views.u_logout),
    path('catfilter/<cdv>',views.catfilter),
    path('sort/<sortvalue>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('remove_placeorder/<cid>',views.remove_placeorder),
   
    path('makepayment',views.makepayment),
    path('search/', views.search_grocery, name='search_grocery'),
    path('validate_password/', views.validate_password),
    path('searchrange/', views.search_range, name='search_range'),

     path('back_to_cart/', views.back_to_cart, name='back_to_cart'),

    


    


    

]




 #this is for add image to thire respective product name 
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #urlpattersns=urlpatterns+static(....) ok
    