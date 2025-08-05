from .models import Post, Notification, Category, Comment, Contact 
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
from accounts.models import User

Users= get_user_model()

# Temporary store to hold old user data between pre_save and post_save
old_user_cache = {}


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#  to notify after postaddition
@receiver (post_save, sender= Post)
@receiver(post_save, sender= Category)
def notifySuperuserAfterAddition(sender, instance, created , **kwargs):
     if created: 
        if sender == Post:
            users= Users.objects.filter(is_superuser=True)

            for admin in users:
                Notification.objects.create(
                user=admin,
                message=f"New post '{instance.title}' was created by {instance.author}",
                model_name="post.Post",
                model_id=instance.pk
                )

#  fro category addition
        elif sender == Category:
            users= Users.objects.filter(Q (is_superuser=True) | Q(is_staff=True))

                     
            for admin in users:
                Notification.objects.create(
                user=admin,
                message=f"New category {instance.name} was added ",
                model_name= "post.category",
                model_id=instance.id
                )


#  to notify after postdeletion

# @receiver(post_delete, sender=Post)

# def notifySuperuserAfterPostDelete(sender, instance, **kwargs):

#     superusers= Users.objects.filter(is_superuser=True)

#     for admin in superusers:
#      Notification.objects.create(
#         user=admin,
#         message=f" Post '{instance.title}' is deleted by {instance.author}"
#      )


#     if instance.author not in superusers:
#          Notification.objects.create(
#             user=instance.author,
#             message=f"Your post '{instance.title}' has been deleted"
#         )
         

# yesma mildaina cuz yesle poet koa uthor ko access didiaina aahile change gareko user matra dekhauxa 
# @receiver(post_save, sender=Post)
# def notifyAfterPostUpdate(sender, instance, created, **kwargs):
#     if not created:
        
#         superusers=User.objects.filter(is_superuser=True)

#         for admin in superusers:
#             Notification.objects.create(
#                 user=admin,
#                 message=f" Post '{instance.title}' has been updated by {instance.author}"
#             )

#         if instance.author not in superusers:
#              Notification.objects.create(
#                 user=instance.author,

#                 #  yo use garna mildaina kna bhaney yesle post ko author lai access gana sakidaina so use this in update_post ma 
#                 # message=f" Post '{instance.title}' has been updated by {instance.author}"
#                  message=f" Post '{instance.title}' has been updated "

#             )


#  to notify after categoryadd
# @receiver(post_save, sender= Category)
# def notifyAfterCategoryAdd(sender, instance, created, *args, **kwargs):
#     if created:

#         users= Users.objects.filter(Q (is_superuser=True) | Q(is_staff=True))

#         for admin in users:
#             Notification.objects.create(
#                 user=admin,
#                 message=f"New category {instance.name} was added ",
#                 model_name= "post.category",
#                 model_id=instance.id
#             )

#             print('notificato',Notification)



#  to notify after category update
@receiver(post_save, sender= Category)
def notifyAfterCategoryUpdate(sender, instance, created, *args, **kwargs):
    if not created:
         
        users= Users.objects.filter(Q(is_superuser=True) | Q(is_staff=True))

        for admin in users:
            Notification.objects.create(
                user=admin,
                message=f"Category {instance.name} was updated ",
                model_name="post.category",
                model_id=instance.id,
            )
        print('instance',instance)




#  to notify after categorydelete
@receiver(post_delete, sender= Category)
@receiver(post_delete, sender=User)
@receiver(post_delete, sender= Post)
def notifyAfterDelete(sender, instance, *args, **kwargs):
    if sender == Category:
         
         users= Users.objects.filter(Q(is_superuser=True) | Q(is_staff=True))

         for admin in users:
            Notification.objects.create(
                user=admin,
                message=f"Category {instance.name} was deleted ",
                model_name="post.category",
                model_id=instance.id
            )
            print('instance',instance)

    elif sender == User:

        users= Users.objects.filter(is_superuser=True)

        for admin in users:
            Notification.objects.create(
                user=admin,
                message=f"User '{instance.username}' has beeen deleted ",
                model_name="accounts.User",
                model_id=instance.id
            )


    elif sender == Post:
        superusers= Users.objects.filter(is_superuser=True)

        for admin in superusers:
            Notification.objects.create(
                user=admin,
                message=f" Post '{instance.title}' is deleted by {instance.author}",
                model_name="post.Post",
                model_id=instance.id
            )


            if instance.author not in superusers:
                Notification.objects.create(
                    user=instance.author,
                    message=f"Your post '{instance.title}' has been deleted", 
                    model_name="post.Post",
                    model_id=instance.id
                )





   


#  to notify after commentsaddition
@receiver(post_save, sender=Comment)
def notifyAfterCommentsAdd(sender, instance, created, *args, **kwargs):
    if created:
            
            posts=instance.post

            users=Users.objects.filter(is_superuser=True)

            for admin in users:
                Notification.objects.create(
                    user=admin,
                    message=f"Comment '{instance.content}' was added by '{instance.author}' in '{posts.title}' ",
                    model_name="post.Comment",
                    model_id=instance.id
                )

            #  to notify author of the post
            if posts.author not in users:
                Notification.objects.create(
                    user=posts.author,
                    message=f"Comment '{instance.content}' was added by '{instance.author}' in '{posts.title}' ",
                    model_name="post.Comment",
                    model_id=instance.id
                )
         
         



#  to notify after categorydeletion
@receiver(post_save, sender=Comment)
def notifyAfterCommentDelete(sender,instance, created, *args, **kwargs):
    if not created:

        posts=instance.post


        users=Users.objects.filter(is_superuser=True)
        for admin in users:
            Notification.objects.create(
                user=admin,
                message=f"Commene '{instance.content}' is deleted by '{instance.author}' "
            )


            Notification.objects.create(
            user=posts.author,
            message=f"Comment '{instance.content}' was deleeted by '{instance.author}' in '{posts.title}' "
            )



@receiver(post_save, sender= User)
def noftifyAfterUserAdd(sender,instance,created, *args, **kwargs):
    if created:

       users=Users.objects.filter(is_superuser=True)

       for admin in users:
           Notification.objects.create(
               user=admin,
               message=f"New user '{instance.username}' has been created ",
               model_name="accounts.User",
               model_id=instance.id
           )



# @receiver(post_save,sender=User)
# def notifyAfterUserUpdate(sender, instance, created, *args, **kwargs):

#     if not created:

#         users=User.objects.filter(is_superuser=True)

#         for admin in users:
#             Notification.objects.create(
#                 user=admin,
#                 message=f"User {instance.username} has been updated "
#             )





# from django.db.models.signals import pre_save

# @receiver(pre_save, sender=User)
# def cache_old_user(sender, instance, **kwargs):
#     if instance.pk:  # Only for existing users
#         try:
#             old_user = User.objects.get(pk=instance.pk)
#             old_user_cache[instance.pk] = old_user
#         except User.DoesNotExist:
#             pass


# @receiver(post_save, sender=User)
# def notify_user_changes(sender, instance, created, **kwargs):
#     superusers = User.objects.filter(is_superuser=True)

#     if created:
#         message = f"New user '{instance.username}' has been created"

#     else:
#         old_user = old_user_cache.pop(instance.pk, None)  # Remove after use

#         if not old_user:
#             return  # No cached user found

#         fields_to_check = ['username', 'email', 'first_name', 'last_name','password']

#         has_real_changes = any(
#             getattr(old_user, field) != getattr(instance, field)
#             for field in fields_to_check
#         )

#         if not has_real_changes:
#             return  

#         message = f"User '{instance.username}' has been updated"

#     for admin in superusers:
#         Notification.objects.create(user=admin, message=message)




# @receiver(post_delete, sender=User)
# def notifyAfterUserDelete(sender, instance, *args, **kwargs):

#     users= Users.objects.filter(is_superuser=True)
#     for admin in users:
#         Notification.objects.create(
#             user=admin,
#             message=f"User '{instance.username}' has beeen deleted "
#         )


from django.urls import reverse

@receiver(post_save, sender=Contact)
def notifyAfterContactFormSubmission(sender, created, instance, *args, **kwargs):
    if created:

        users=User.objects.filter(is_superuser=True)


        for admin in users:
            Notification.objects.create(
                user=admin,
                message=f"New Contact request  sent by '{instance.name}' ",
                model_name="post.Contact",
                model_id=instance.id
            )
