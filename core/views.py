
from core.models import RiskAssessment
from django.contrib.auth import login
from core.forms import SignUpForm, UserProfileForm, HealthDataForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import BlogPost, Comment, CommentVote
from django.http import HttpResponseForbidden
from core.models import Hospital
from core.models import EducationalResource
from django.contrib import messages
from core.utils import calculate_qrisk3_score
from core.forms import BlogPostForm
from core.forms import EducationalResourceForm


def signup_view(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        health_form = HealthDataForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and health_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            health = health_form.save(commit=False)
            health.user_profile = profile
            health.save()

            login(request, user)
            messages.success(request, "Signup successful. Let's assess your heart health.")
            return redirect('assess_risk')  # Redirect after signup
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        user_form = SignUpForm()
        profile_form = UserProfileForm()
        health_form = HealthDataForm()

    return render(request, 'authentication/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'health_form': health_form
    })

@login_required
def assess_risk(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        health_form = HealthDataForm(request.POST)

        if profile_form.is_valid() and health_form.is_valid():
            user_profile = profile_form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            health_data = health_form.save(commit=False)
            health_data.user_profile = user_profile
            health_data.save()

            # Pull values for scoring
            age = user_profile.age
            sex = user_profile.sex
            smoker = user_profile.smoker
            diabetes = user_profile.diabetes
            systolic = health_data.systolic_bp
            chol_hdl_ratio = health_data.cholesterol_ratio
            bmi = health_data.bmi
            ethnicity = user_profile.ethnicity

            # QRISK3-based score
            score = calculate_qrisk3_score(
                age, sex, smoker, diabetes, systolic, chol_hdl_ratio, bmi, ethnicity
            )

            risk_category = 'High' if score > 20 else 'Low'

            RiskAssessment.objects.create(
                user_profile=user_profile,
                score=score,
                risk_category=risk_category
            )

            print(f"This is the risk score {score} and the risk category {risk_category}")

            messages.success(request, f"Assessment complete. Your risk category is {risk_category}.")
            return redirect('blog_list' if risk_category == 'Low' else 'hospital_finder')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        profile_form = UserProfileForm(instance=getattr(request.user, 'userprofile', None))
        health_form = HealthDataForm()

    return render(request, 'risk_assessment/risk_assessment.html', {
        'profile_form': profile_form,
        'health_form': health_form
    })



def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comments = blog.comments.filter(parent=None).order_by('-created_at')
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog,
        'comments': comments
    })

@login_required
def add_comment(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        if content:
            Comment.objects.create(
                blog=blog,
                user=request.user,
                content=content,
                parent=parent_comment
            )
            messages.success(request, "Your comment has been posted.")
        else:
            messages.error(request, "Comment content cannot be empty.")

    return redirect('blog_detail', pk=pk)


@login_required
def vote_comment(request, comment_id, vote_type):
    comment = get_object_or_404(Comment, id=comment_id)

    if vote_type not in ['up', 'down']:
        return HttpResponseForbidden()

    vote, created = CommentVote.objects.get_or_create(
        comment=comment,
        user=request.user,
        defaults={'vote_type': vote_type}
    )

    if created:
        messages.success(request, f"You {vote_type}voted this comment.")
    elif vote.vote_type != vote_type:
        vote.vote_type = vote_type
        vote.save()
        messages.success(request, f"You changed your vote to {vote_type}.")
    else:
        messages.info(request, f"You already {vote_type}voted this comment.")

    return redirect('blog_detail', pk=comment.blog.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_staff:  # Admin check
        comment.is_deleted_by_admin = True
        comment.save()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('blog_detail', pk=comment.blog.id)

def hospital_finder_view(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospital_finder/hospital_finder.html', {'hospitals': hospitals})

def educational_resources_view(request):
    resources = EducationalResource.objects.all().order_by('-created_at')
    return render(request, 'educational_resources/educational_resources.html', {'resources': resources})

@login_required
def dashboard(request):
    user_profile = getattr(request.user, 'userprofile', None)
    last_assessment = (
        RiskAssessment.objects.filter(user_profile=user_profile)
        .order_by('-assessed_at')
        .first()
    )
    blog_posts = BlogPost.objects.order_by('-created_at')[:3]
    resources = EducationalResource.objects.order_by('-created_at')[:3]

    return render(request, 'authentication/dashboard.html', {
        'last_assessment': last_assessment,
        'blog_posts': blog_posts,
        'resources': resources
    })


@user_passes_test(lambda u: u.is_staff)
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog post created successfully.")
            return redirect('blog_list')
    else:
        form = BlogPostForm()

    return render(request, 'blogs/create_blog.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def create_educational_resource(request):
    if request.method == 'POST':
        form = EducationalResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Educational resource created.")
            return redirect('educational_resources')
    else:
        form = EducationalResourceForm()

    return render(request, 'resources/create_resource.html', {'form': form})

def landing_page(request):
    return render(request, 'landing_page.html')

