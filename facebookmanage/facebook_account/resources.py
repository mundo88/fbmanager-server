from import_export import resources
from .models import FacebookAccount

class FacebookAccountResource(resources.ModelResource):
    class Meta:
        model = FacebookAccount