from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from simple_registration.views import register, activate
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^activate/complete/$', direct_to_template, { 'template': 'simple_registration/activation_complete.html' }, name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$', activate, name='registration_activate'),
    url(r'^register/$', register, name='registration_register'),
    url(r'^register/complete/$', direct_to_template, { 'template': 'simple_registration/registration_complete.html' }, name='registration_complete'),
    url(r'^register/closed/$', direct_to_template, { 'template': 'simple_registration/registration_closed.html' }, name='registration_disallowed'),
    
    #Contrib.Auth Views
    url(r'^login/$', auth_views.login,                                                                                      {'template_name': 'simple_registration/login.html'},                    name='auth_login'),
    url(r'^logout/$', auth_views.logout,                                                                                    {'template_name': 'simple_registration/logout.html'},                   name='auth_logout'),
    url(r'^settings/password/change/$', auth_views.password_change,                                                         {'template_name': 'simple_registration/password_change_form.html'},     name='auth_password_change'), 
    url(r'^settings/password/change/done/$', auth_views.password_change_done,                                               {'template_name': 'simple_registration/password_change_done.html'},     name='auth_password_change_done'),
    url(r'^settings/password/reset/$', auth_views.password_reset,                                                           {'template_name': 'simple_registration/password_reset_form.html'},      name='auth_password_reset'),
    url(r'^settings/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,    {'template_name': 'simple_registration/password_reset_confirm.html'},   name='auth_password_reset_confirm'),
    url(r'^settings/password/reset/complete/$', auth_views.password_reset_complete,                                         {'template_name': 'simple_registration/password_reset_complete.html'},  name='auth_password_reset_complete'),
    url(r'^settings/password/reset/done/$', auth_views.password_reset_done,                                                 {'template_name': 'simple_registration/password_reset_done.html'},      name='auth_password_reset_done'),
)
