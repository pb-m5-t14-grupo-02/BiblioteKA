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
            <body style="font-family: Arial, Helvetica, sans-serif; border: 10px solid rgb(71, 71, 71); margin: 0;">
	            <header style="background-color: rgb(109, 109, 109); display: flex; justify-content: space-between; align-items: center;">
                    <h1 style="margin-left: 15px;">Traças de Alexandria</h1>
                    <picture style="margin: 15px; background-color: rgb(86, 86, 86); border-radius: 100%; padding: 25px;">
                        <img style="height: 80px;" src="https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683307565/emails/book-stack_a5yipz.png"/>
                    </picture>
	            </header>
                <main style="margin: 15px; text-align: center;">
                    <h2>Redefinição de senha</h2>
                    <p>Olá {current_user},</p>
                    <p>Você solicitou a redefinição da sua senha no site.</p>
                    <p>Para redefinir sua senha, clique no link abaixo:</p>
                    <p><a href="{reset_password_url}">{reset_password_url}</a></p>
                    <small style="text-align: right; display: block;">Atenciosamente, Traças de Alexandria</small>
                </main>
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
