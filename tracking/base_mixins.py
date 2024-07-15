from django.utils.timezone import now
import ipaddress
from app_settings import app_setting
class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        self.log = {'requested_at':now()}
        super().initial(request, *args, **kwargs)
        
    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        user = self._get_user(request)
        self.log.update({
            'remote_addr': self._get_ip_address(request),
            'view':self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'path':self._get_path(request),
            'host': request.get_host(),
            'method': request.method,
            'user': user,
            'username_persistant': user.get_username() if user else 'Anonymous',
            'response_ms': self._get_response_ms(),
            
            
        })
        self.handle_log()
        return response
    
    # by this line of code we make sure whoever use this code overwrite this method and if not raise this error 
    def handle_log(self):
        raise NotImplementedError
    
    # with this method we can access user ip address
    def _get_ip_address(self, request):
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', '').split(',')[0]
        
        posib = (ipaddr.lstrip('[')[0], ipaddr.split(':')[0])
        
        for addr in posib:
            try:
                return str(ipaddress.ip_address(addr))
            except:
                pass
        
        return ipaddr
    
    # in this method we wnat the view name of the request 
    def _get_view_name(self, request):
        # we get the method of the request
        method = request.method.lower()
        try:
            attribute = getattr(self, method)
            #print(type(attribute.__self__).__module__) # output > tracking.views
            #print(type(attribute.__self__).__name__) # output > HomeAPI
            # now we have to concat this two value to simulate the whole name
            return (type(attribute.__self__).__module__)+ '.'+ type(attribute.__self__).__name__
        except AttributeError:
            return None
    
    # in this method we want to get the mwthod of the request  
    def _get_view_method(self, request):
        # in DRF in the viewset we can have action that specified the method action that allowed so we have to handel that here
        if hasattr(self, 'action'):
            return self.action or None
        return request.method.lower()
           
    def _get_path(self, request):
        # check out the app settings file we create the logic in there 
        return request.path[:app_setting.PATH_LENGTH]
    
    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user
    
    def _get_response_ms(self):
        # this is how we get the time that take to show the result by decrease the now to request time 
        response_time_delta = now() - self.log['requste_at']
        # we use the * sign to make it mil secound
        response_ms = int(response_time_delta.total_seconds() * 1000)
        # because we use int its might be negetive so we use max to get the zero in case of negetive 
        return max(response_ms, 0)
    
    