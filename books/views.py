from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy 
from django.views.generic import ListView, DetailView,UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order,MyProfile,Cart
from django.db.models import Q # for search method
from django.http import JsonResponse

import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.encoding import force_str,force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage, send_mail
from ecom_project import settings
from . tokens import generate_token
from django.contrib import messages



def index(request):
    return render(request,'index.html')
def signup(request):

    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            return redirect('signup')
        
        
        if pass1 != pass2  :
            return redirect('signup')
        
        if len(pass1)>8 & len(pass2)>8:
            return redirect('signup')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        subject = 'Welcome to SRH - JOB Login!!'
        message = 'Hello'+ myuser.username + '!! \n'+ 'Welcome to SRH!! \n Thank you for visiting our website \n we also send you a conformation email,please conform your email address in order to activate your account. \n\n Thanking you \n Sreehari'
        from_email = settings.EMAIL_HOST_USER
        to_list = {myuser.email}
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ SRH - JOB Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('signin')
    

    return render(request,'signup.html')
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')



def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.username
            return redirect('profile.html')

        else:
            return redirect('signin')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

class BooksListView(ListView):
    model = Book
    template_name = 'list.html'


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
    success_url = reverse_lazy('object_list')


class SearchResultsListView(ListView):
	model = Book
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return Book.objects.filter(
		Q(title__icontains=query) | Q(author__icontains=query)
		)

class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'signin'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Book.objects.get(id=body['productId'])
	Order.objects.create(
		product=product
	)
	return JsonResponse('Payment completed!', safe=False)

class prolist(ListView):

    model = MyProfile
    fields = ['name','email','phone','mobile','address']
    context_object_name = 'myprofile'
    template_name = 'view.html'

class proform(CreateView):
    model = MyProfile
    success_url=reverse_lazy('view')
    fields = ['profile','name','email','phone','mobile','address']
    template_name = 'profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(proform, self).form_valid(form)

class proupdate(UpdateView):
    model = MyProfile
    success_url=reverse_lazy('view')
    fields = ['profile','name','email','phone','mobile','address']
    template_name = 'profile.html'

def add_to_cart(request, product_id):
    Product = get_object_or_404(Book, pk=product_id)
    cart_item,created = Cart.objects.get_or_create(
        user=request.user,
        product= Product,
        price=Product.price,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
