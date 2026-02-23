from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import Ticket


def get_ticket_analytics():
    total = Ticket.objects.count()

    status_data = Ticket.objects.values('status').annotate(total=Count('status'))

    priority_data = Ticket.objects.values('priority').annotate(total=Count('priority'))

    city_data = Ticket.objects.values('address').annotate(total=Count('address')).order_by('-total')

    resolved = Ticket.objects.filter(closed_at__isnull=False)

    avg_resolution = resolved.annotate(
        duration=ExpressionWrapper(
            F('closed_at') - F('raised_at'),
            output_field=DurationField()
        )
    ).aggregate(avg_time=Avg('duration'))

    return {
        "total": total,
        "status_data": status_data,
        "priority_data": priority_data,
        "city_data": city_data,
        "avg_resolution": avg_resolution["avg_time"],
    }