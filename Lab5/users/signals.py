from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def create_group(sender, **kwargs):
    admin_group, admin_group_created = Group.objects.get_or_create(name='admins')
    customer_group, customer_group_created = Group.objects.get_or_create(name='customers')
    if admin_group_created:
        permissions = ('add_product', 'delete_product', 'change_product',
                       'view_product', 'add_comment', 'delete_comment',
                       'view_comment', 'change_comment', 'view_adminprofile',
                       'view_customerprofile', 'view_baseuser')
        for permission in permissions:
            perm = Permission.objects.get(codename=permission)
            admin_group.permissions.add(perm)
        admin_group.save()
    if customer_group_created:
        permissions = ('view_product', 'add_comment', 'delete_comment',
                       'change_comment', 'view_comment', 'delete_customerprofile',
                       'view_customerprofile', 'change_customerprofile',
                       'change_baseuser', 'view_baseuser', 'delete_baseuser')
        for permission in permissions:
            perm = Permission.objects.get(codename=permission)
            customer_group.permissions.add(perm)
