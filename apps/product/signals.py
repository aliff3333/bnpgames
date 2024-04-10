from django.db.models import Avg, Count
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from apps.comment.models import Review
from apps.product.models import Product


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, created, **kwargs):
    if not created and instance.approved:
        product = instance.product
        # Calculate average rating and number of reviews for the product
        aggregated_data = Review.objects.filter(product=product, approved=True).aggregate(
            average_rating=Avg('rating'),
            num_reviews=Count('id')
        )
        product.rating = aggregated_data.get('average_rating', 0)
        product.reviews = aggregated_data.get('num_reviews', 0)
        product.save()


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    product = instance.product

    # Calculate the new average rating and number of reviews for the product
    aggregated_data = Review.objects.filter(product=product, approved=True).aggregate(
        average_rating=Avg('rating'),
        num_reviews=Count('id')
    )
    new_avg_rating = aggregated_data.get('average_rating')
    num_reviews = aggregated_data.get('num_reviews')

    # Update product's average rating and number of reviewers
    if new_avg_rating is None:  # If there are no more reviews
        product.rating = 3  # Set default rating to 3
        product.reviewers = 0  # Reset number of reviewers
    else:
        product.rating = new_avg_rating
        product.reviewers = num_reviews

    product.save()
