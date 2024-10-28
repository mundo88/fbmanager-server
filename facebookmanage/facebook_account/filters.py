import django_filters
from facebook_account.models import FacebookAccount

class CommaSeparatedIDFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class FbAccountFilterSet(django_filters.FilterSet):
    id = CommaSeparatedIDFilter(field_name='id', lookup_expr='in')
    
    class Meta:
        model = FacebookAccount
        fields = ['id']