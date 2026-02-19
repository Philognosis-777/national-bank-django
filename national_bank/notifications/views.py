from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone

from .models import Notification
from .mixins import AdminRequiredMixin
from . import services


class NotificationListView(View):
    """List notifications for logged-in users. Shows unread and read, supports filters."""

    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required'}, status=401)

        qs = Notification.objects.filter(
            (models.Q(notification_type=Notification.TYPE_SYSTEM) | models.Q(target_user=request.user))
        ).order_by('-is_read', '-created_at')

        # filters
        ntype = request.GET.get('type')
        if ntype:
            qs = qs.filter(notification_type__iexact=ntype)
        priority = request.GET.get('priority')
        if priority:
            qs = qs.filter(priority__iexact=priority)

        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 25))
        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'results': [], 'count': paginator.count})

        items = [
            {
                'id': n.pk,
                'title': n.title,
                'content': n.content,
                'is_read': n.is_read,
                'priority': n.priority,
                'notification_type': n.notification_type,
                'send_at': n.send_at.isoformat() if n.send_at else None,
                'created_at': n.created_at.isoformat(),
            }
            for n in page_obj.object_list
        ]
        return JsonResponse({'results': items, 'count': paginator.count, 'num_pages': paginator.num_pages})


class NotificationDetailView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required'}, status=401)

        n = get_object_or_404(Notification, pk=pk)
        # permission: system notifications visible to all, user notifications only to target
        if n.notification_type == Notification.TYPE_USER and n.target_user != request.user:
            return JsonResponse({'detail': 'Not found'}, status=404)

        # mark as read
        services.mark_notification_read(n)

        data = {
            'id': n.pk,
            'title': n.title,
            'content': n.content,
            'is_read': n.is_read,
            'priority': n.priority,
            'notification_type': n.notification_type,
            'send_at': n.send_at.isoformat() if n.send_at else None,
            'created_at': n.created_at.isoformat(),
        }
        return JsonResponse(data)


class NotificationCreateView(AdminRequiredMixin, View):
    def post(self, request):
        data = request.POST
        title = data.get('title')
        content = data.get('content', '')
        ntype = data.get('notification_type', Notification.TYPE_SYSTEM)
        target = data.get('target_user')
        priority = data.get('priority', Notification.PRIORITY_MEDIUM)
        send_at = data.get('send_at')
        send_at_val = None
        if send_at:
            try:
                send_at_val = timezone.datetime.fromisoformat(send_at)
            except Exception:
                send_at_val = None

        n = services.create_notification(title=title, content=content, notification_type=ntype,
                                         target_user_id=target, priority=priority, send_at=send_at_val)
        return JsonResponse({'id': n.pk, 'created': True})


class NotificationUpdateView(AdminRequiredMixin, View):
    def post(self, request, pk):
        n = get_object_or_404(Notification, pk=pk)
        data = request.POST
        n.title = data.get('title', n.title)
        n.content = data.get('content', n.content)
        n.priority = data.get('priority', n.priority)
        n.notification_type = data.get('notification_type', n.notification_type)
        target = data.get('target_user')
        n.target_user_id = target if target else n.target_user_id
        send_at = data.get('send_at')
        if send_at:
            try:
                n.send_at = timezone.datetime.fromisoformat(send_at)
            except Exception:
                pass
        n.save()
        return JsonResponse({'id': n.pk, 'updated': True})


class NotificationDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        n = get_object_or_404(Notification, pk=pk)
        n.delete()
        return JsonResponse({'id': pk, 'deleted': True})
