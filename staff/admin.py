# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Doctor, Nurse, OtherStaff, UserType, Speciality

# Register your models here.
# admin.site.register(Doctor)
admin.site.register(UserType)
admin.site.register(Nurse)
admin.site.register(Speciality)
admin.site.register(OtherStaff)

