# this class is for the case that user do not spesified the custome setting in the settings.py file and we have to handel this 
class AppSettings:
    #this prefix is the DRF_TRACKING that we should start with at the begining in every config in the settings file 
    def __init__(self, prefix):
        self.prefix = prefix
    
    #_setting is the private method in the class that get the value from setting file if its exist and if not put the defailt value 
    # we can custome this default and name part in the custom property that we want to prepare  
    def _settings(self, name ,deflt):
        from django.conf import settings
        
        return getattr(settings, self.prefix + name, deflt)
    
    # now we create a custome property that use the _setting method to get the path lenght and have a default 200 calue if the user 
    # do not define "DRF_TRACKING_PATH_LENTH" in the settings file 
    @property
    def PATH_LENGTH(self):
        return self._settings('PATH_LENGTH', 200)

# now we create a instance and import this in the base mixin 
app_setting = AppSettings('DRF_TRACKING_')
        