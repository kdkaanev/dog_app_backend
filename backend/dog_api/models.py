from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TYPE_CHOICES = (
    ('lost', 'Lost'),
    ('found', 'Found'),
    ('adopted', 'Adopted'),
)
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
)


class DogUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='dog_user',
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]} {self.last_name[0]}"
        return self.first_name[0] or self.last_name[0]


class DogPost(models.Model):
    title = models.CharField(
        null=True,
        blank=True,
        max_length=100,
    )
    breed = models.CharField(
        null=True,
        blank=True,
        max_length=100,
    )
    photo_url = models.URLField(
        null=False,
        blank=False,
    )
    description = models.TextField()
    last_seen_location = models.CharField(
        null=True,
        blank=True,
    )
    date_posted = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True,
    )
    status = models.CharField(
        null=True,
        blank=True,
        choices=TYPE_CHOICES,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dog_posts',
    )

    def __str__(self):
        return f"{self.title.capitalize()}"


class AdoptionApplication(models.Model):
    title = models.CharField(max_length=100, default="")
    user = models.ForeignKey(
        DogUser,
        on_delete=models.CASCADE,
        related_name='adoption_applications',
    )
    dog = models.ForeignKey(
        DogPost,
        on_delete=models.CASCADE,
        related_name='adoption_applications',
    )
    status = models.CharField(
        null=False,
        blank=False,
        choices=STATUS_CHOICES,
    )
    message = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()

    dog_post = models.ForeignKey(
        DogPost,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.full_name} on {self.dog_post.title}"
