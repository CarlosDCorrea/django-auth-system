from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse

from django.conf import settings


def create_email(username, user_id, request):
    title = 'Welcome to the Django Authentication System'
    subject = 'User creation'
    template_name = 'email_app/create_user.html'
    activation_url = reverse('activate-user')
    absolute_activation_url = f"{request.scheme}://{request.get_host()}{activation_url}"
    print(absolute_activation_url)
    context = {
        'username': username,
        'user_id': user_id,
        'activation_url': absolute_activation_url
    }
    
    template = render_to_string(template_name, context)
    return send(title, subject, template)
    
def send(title, subject, template):
    service_response = {}
    
    try:
        send_mail(
            title, 
            subject,
            settings.EMAIL_HOST_USER,
            ['the user email'],
            fail_silently=False,
            html_message=template
        )
        
        service_response['status'] = 200
        service_response['message'] = 'The mail has been send successfully'
    except Exception as e:
        service_response['status'] = 400
        service_response['message'] = f'It was not possible to send the mail due to the following error {e}'
    finally:
        return service_response