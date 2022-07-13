# python dependencies
from re import compile

# django dependencies
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.conf import settings

# Local Imports
from common.views import get_ipinfo

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


#---------------------#
# For Login Requirend #
#---------------------#
class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user')
        """ The Login Required middleware requires authentication middleware to be 
        installed. Edit your MIDDLEWARE_CLASSES setting to insert 
        'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't work, 
        ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes
         'django.core.context_processors.auth'."""

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            full_path = request.get_full_path()
            is_image = True if '/testimonial/' in full_path else False
            if not is_image:
                if not any(m.match(path) for m in EXEMPT_URLS):
                    return redirect_to_login(
                        full_path, settings.LOGIN_URL, REDIRECT_FIELD_NAME)

        # if not request.session.get('ip_info', None):
        #     ip_info = get_ipinfo(request)
        #     request.session['ip_info'] = ip_info
        request.session['ip_info'] = {"ip": "106.51.67.101", "country": "US"}



# Uncomment for production Maintenance
#---------------------
# For Maintenance Mode 
#---------------------
# class MaintenanceMiddleware(object):
#     """Serve a temporary redirect to a maintenance url in maintenance mode"""
#     def process_request(self, request):
#         if request.method == 'POST':
#             if getattr(settings, 'MAINTENANCE_MODE', False) is True \
#                     and hasattr(settings, 'MAINTENANCE_URL'):
#                 # http? where is that defined?
#                 return http.HttpResponseRedirect(settings.MAINTENANCE_URL)
#             return None
