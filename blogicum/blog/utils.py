from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.utils import timezone


def get_filtered_qs(queryset, **kwargs):

    filters = {
        'is_published': True,
        'pub_date__lte': timezone.now(),
        'category__is_published': True,
        **kwargs,
    }

    return queryset.filter(**filters).annotate(comment_count=Count('comments'))


def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test email from Django.'
    from_email = 'test@example.com'
    recipient_list = ['recipient@example.com']

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Test email sent.')
