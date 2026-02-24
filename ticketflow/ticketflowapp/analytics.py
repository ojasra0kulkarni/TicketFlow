from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import Ticket


def get_ticket_analytics(queryset):
    total = queryset.count()
    status_data = queryset.values('status').annotate(total=Count('status'))
    priority_data = queryset.values('priority').annotate(total=Count('priority'))
    city_data = queryset.values('address').annotate(
        total=Count('address')
    ).order_by('-total')
    resolved = queryset.filter(closed_at__isnull=False)

    avg_resolution = resolved.annotate(
        duration=ExpressionWrapper(
            F('closed_at') - F('raised_at'),
            output_field=DurationField()
        )
    ).aggregate(avg_time=Avg('duration'))

    avg_time = avg_resolution["avg_time"]

    if avg_time:
        total_seconds = avg_time.total_seconds()
        hours = round(total_seconds / 3600, 2)
        formatted_avg = f"{hours} hrs"
    else:
        formatted_avg = "0 hrs"

    return {
        "total": total,
        "status_data": status_data,
        "priority_data": priority_data,
        "city_data": city_data,
        "avg_resolution": formatted_avg,
    }