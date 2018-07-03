import sys

from django.conf import settings

from django.core.mail import EmailMessage

settings.configure(

    DEBUG=True,

    SECRET_KEY='l(kx!xmf87o2kt@ve!f9mk-ws+7^iffz-ry0te#)ubu_xe8va+',

    ROOT_URLCONF=__name__,

    MIDDLEWARE_CLASSES=(

        'django.middleware.common.CommonMiddleware',

        'django.middleware.csrf.CsrfViewMiddleware',

        'django.middleware.clickjacking.XFrameOptionsMiddleware',

    ),
    EMAIL_HOST='smtp.gmail.com',
    # Port for sending e-mail.
    EMAIL_PORT=587,

    # Optional SMTP authentication information for EMAIL_HOST.
    EMAIL_HOST_USER='dnunezd96@gmail.com',
    EMAIL_HOST_PASSWORD='',
    EMAIL_USE_TLS=True,

)


def enviar(msj, subject, to):
    e = EmailMessage()
    e.body = msj
    e.subject = subject
    e.to = [to, ]
    e.send()


if __name__ == "__main__":
    enviar(sys.argv[1], sys.argv[2], sys.argv[3])
