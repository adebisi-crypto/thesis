from django.contrib import admin
from .models import BlogPost, Comment, CommentVote, EducationalResource, Hospital, UserProfile, HealthData, RiskAssessment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'content', 'is_deleted_by_admin', 'created_at')
    list_filter = ('is_deleted_by_admin', 'created_at')
    search_fields = ('user__username', 'content')

@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'vote_type')
    list_filter = ('vote_type',)

@admin.register(EducationalResource)
class EducationalResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'category')
    list_filter = ('created_at',)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'sex', 'ethnicity', 'smoker', 'diabetes')

@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'systolic_bp', 'diastolic_bp', 'cholesterol_ratio', 'bmi', 'recorded_at')

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'score', 'risk_category', 'assessed_at')
    list_filter = ('risk_category', 'assessed_at')

