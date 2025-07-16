from django.shortcuts import render
from .models import DailyEntry
from django.db.models import Count
from django.utils import timezone
import json

def dashboard(request):
    # Get last 7 days of data
    date_range = [timezone.now().date() - timezone.timedelta(days=x) for x in range(7)][::-1]
    
    # Query posts per day
    posts_data = (
        DailyEntry.objects
        .filter(submitted_at__date__gte=date_range[0])
        .values('submitted_at__date')
        .annotate(count=Count('id'))
        .order_by('submitted_at__date')
    )
    
    # Prepare chart data
    dates = [entry['submitted_at__date'].strftime('%Y-%m-%d') for entry in posts_data]
    post_counts = [entry['count'] for entry in posts_data]
    
    # Fill in missing dates with 0
    chart_dates = []
    chart_counts = []
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        chart_dates.append(date_str)
        if date_str in dates:
            chart_counts.append(post_counts[dates.index(date_str)])
        else:
            chart_counts.append(0)
    
    context = {
        'dates': json.dumps(chart_dates),
        'post_counts': json.dumps(chart_counts)
    }
    return render(request, 'core/dashboard.html', context)