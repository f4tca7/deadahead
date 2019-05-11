from django.conf import settings

def use_ga(request):
    return {'use_ga': settings.USE_GA}