from django.contrib import admin

from MentalHealth.models import Contact, Checkout, Member, Images,Professional

# Register your models here.
admin.site.register(Checkout)
admin.site.register(Contact)
admin.site.register(Member)
admin.site.register(Images)
admin.site.register(Professional)

