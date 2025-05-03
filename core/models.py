
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Core Health Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10)
    ethnicity = models.CharField(max_length=100)
    smoker = models.BooleanField()
    diabetes = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class HealthData(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
    cholesterol_ratio = models.FloatField()
    bmi = models.FloatField()
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'HealthData for {self.user_profile.user.username}'

class RiskAssessment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.FloatField()
    risk_category = models.CharField(max_length=50)
    assessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Assessment for {self.user_profile.user.username} - {self.risk_category}'

class EducationalResource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

# Blog and Comment Models
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_deleted_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user} on {self.blog}'

class CommentVote(models.Model):
    VOTE_TYPE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.vote_type.capitalize()} by {self.user} on comment {self.comment.pk}'

