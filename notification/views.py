from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Notification

# Create your views here.
class NotificationListView(ListView):
    model = Notification
    template_name = 'users/notifications.html'

    def get_queryset(self):
        notifications = Notification.objects.filter(person=self.request.user).all().select_related('person')
        notifications.update(is_read=True)
        return notifications