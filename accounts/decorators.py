from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
#new
from .models import User

# def unauthenticated_user(view_func):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.is_teacher:
#                 return HttpResponseRedirect(reverse('select_item'))
#             elif request.user.is_manager:
#                 return HttpResponseRedirect(reverse('list_item'))
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrap


def patient_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 1:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         return HttpResponseRedirect(reverse('hospital:index'))
    # return wrap


def doctor_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 2:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    #         # return HttpResponseRedirect(reverse('user-profile'))
    # return wrap


def oluseg_doctor_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 4:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    #         ## return HttpResponseRedirect(reverse('user-profile'))
    # return wrap

def int_ext_doctors_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 2 or request.user.user_type == 4:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    # return wrap

def nurse_int_doctors_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 3 or request.user.user_type == 4:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    # return wrap

def nurse_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 3:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    # return wrap


def Small_Admin_only(view_func):
    def wrap(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrap
    # def wrap(request, *args, **kwargs):
    #     if request.user.user_type == 6:
    #         return view_func(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied
    # return wrap