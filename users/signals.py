from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    email_html_message = """
        <html>
            <body>
                <p>Olá {current_user},</p>
                <p>Você solicitou a redefinição da sua senha no site.</p>
                <p>Para redefinir sua senha, clique no link abaixo:</p>
                <p><a href="{reset_password_url}">{reset_password_url}</a></p>
                <p>Atenciosamente,</p>
                <p>A equipe da BiblioteKA</p>
            </body>
        </html>
    """.format(**context)
    
    email_plaintext_message = """
        Olá {current_user},

        Você solicitou a redefinição da sua senha no site.

        Para redefinir sua senha, clique no link abaixo:
        {reset_password_url}

        Atenciosamente,
        A equipe da BiblioteKA
    """.format(**context)


    msg = EmailMultiAlternatives(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "noreply@biblioteka.local",
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
