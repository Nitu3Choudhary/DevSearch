from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile=Profile.objects.create(
            user = user,
            name = user.first_name,
            username = user.username,
            email=user.email,
        )
        print('Same record created in Profile')

        subject = "Welcome to Developer's Web Application"
        message = "We are glad you are here"

        send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
        )
                


        


@receiver(post_delete,sender=Profile)
def deleteUser(sender,instance,**kwargs):
    try:
        user = instance
        user.delete()
        print("User also got deleted") 

    except:
        print("User already deleted")  

                 

post_save.connect(createProfile,sender=User)        