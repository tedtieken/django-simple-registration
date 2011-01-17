from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site, RequestSite
from django.db import transaction
from django.contrib import messages

# Configurable Stuff
from simple_registration.forms import SARRegistrationForm as RegistrationForm

# Custom Stuff
from sar_profile.models import Profile, ProfileAdult


def registration_allowed(request):
    return getattr(settings, 'REGISTRATION_OPEN', True)


@transaction.commit_on_success
def create_user(request, *args, **kwargs):    
    new_user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password1'])
    
    # Custom Stuff
    # Create profile object, adult object, and make adult the primary adult for this profile
    new_SAR_profile = Profile(user=new_user)
    new_SAR_profile.save()
    new_SAR_adult = ProfileAdult(profile=new_SAR_profile, first_name=kwargs['first_name'], last_name=kwargs['last_name'])
    new_SAR_adult.save()
    new_SAR_profile.primary_adult = new_SAR_adult
    new_SAR_profile.save()
            
    return new_user


def send_welcome_email(request, user, **kwargs):
    #Get site for email
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)        
        
    ctx_dict = {'site': site }
    subject = render_to_string('simple_registration/welcome_email_subject.txt', ctx_dict)
    
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('simple_registration/welcome_email.txt', ctx_dict)
    
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)



def register(request):
    if not registration_allowed(request):
        HttpResponseRedirect(reverse('registration_disallowed'))
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            kwargs = form.cleaned_data
            #kwargs.update({"EXAMPLE": "of_a_custom_value"}))
            new_user = create_user(request, **kwargs)
            send_welcome_email(request, new_user, **kwargs)
            
            messages.success(request, "Thanks for creating an account!  Your login email is %s" % kwargs['email'])
            #return HttpResponseRedirect(reverse('registration_complete'))
            
            return HttpResponseRedirect(reverse('auth_login'))
    else:
        form = RegistrationForm()
        
    return render_to_response('simple_registration/registration_form.html', locals(), context_instance=RequestContext(request))


def create_registration_profile(user):
    pass
    
def send_activation_email(user):
    pass

def activate(request, activation_key):
    return HttpResponse("Activate View has not been Implemented")
    pass



