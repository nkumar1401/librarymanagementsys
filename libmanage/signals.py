
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=BorrowRequest)
def update_book_copies_on_borrow(sender, instance, created, **kwargs):
    book = instance.book
    if instance.status == 'APPROVED' and instance.approved_at and book.available_copies > 0:
        book.available_copies -= 1
        book.save(update_fields=['available_copies'])

    elif instance.status == 'RETURNED' and instance.returned_at:
        book.available_copies += 1
        book.save(update_fields=['available_copies'])
