import django_filters

from .models import Job


class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location__city = django_filters.CharFilter(lookup_expr='icontains')
    salary_range = django_filters.RangeFilter()
    job_type = django_filters.ChoiceFilter(choices=Job.JOB_TYPE_CHOICES)
    posted_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Job
        fields = ['title', 'location__city', 'salary_range', 'job_type', 'posted_at']