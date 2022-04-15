from django.shortcuts import render,redirect,resolve_url
from django.contrib.auth.forms import UserCreationForm
from apps.forms import SignupForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from apps.tokens import account_activation_token
from django.core.mail import EmailMessage 
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse  
from django.contrib.auth import get_user_model
# Create your views here.
def home(request):
    return render(request, 'apps/home.html')
def activate_message(request):
    return render(request, 'apps/registration/activate_mail.html')
def activation_done(request):
    return render(request, 'apps/registration/activation_done.html')

class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = 'apps/registration/signup.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        self.object = None
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  

            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id' 
            message = render_to_string('apps/registration/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email') 
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()
            return redirect('/accounts/activation')

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect('/accounts/activation_done')
    else:  
        return HttpResponse('Activation link is invalid!')            