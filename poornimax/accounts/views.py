from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, UserQuestionnaire
from django.conf import settings

User = get_user_model()

def load_signup(request):
    return render(request, 'accounts/signup.html')

def load_login(request):
    return render(request, 'accounts/login.html')

def login_signup(request):
    return render(request, 'accounts/login_signup.html')

@login_required
def x(request):
    return render(request, 'accounts/x.html')

@login_required
def z(request):
    return render(request, 'accounts/z.html')


def signup_access(request):
    if request.method == 'POST':
        data = request.POST
        profile_picture = request.FILES.get('profile_picture')
        email = data.get('college_email')

        if not email.endswith('@poornima.org'):
            messages.error(request, "Use only your college email (@poornima.org).")
            return redirect('accounts:load_signup')

        if User.objects.filter(username=data['username']).exists():
            messages.error(request, 'Username already taken.')
            return redirect('accounts:load_signup')

        if User.objects.filter(college_email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('accounts:load_signup')

        if data['password'] != data['confirm_password']:
            messages.error(request, 'Passwords do not match.')
            return redirect('accounts:load_signup')

        user = User.objects.create_user(
            full_name=data['full_name'],
            college_email=email,
            username=data['username'],
            password=data['password'],
            dob=data['dob'],
            college=data['college'],
            department=data['department'],
            gender=data['gender'],
            bio=data['bio'],
            profile_picture=profile_picture
        )

        messages.success(request, "Account created! You can now log in.")
        return redirect('accounts:load_login')

    return render(request, 'accounts/signup.html')

def login_access(request):
    if request.method == 'POST':
        email = request.POST.get('college_email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            # Check if user has answered the questionnaire
            if not user.has_answered_questionnaire:
                return redirect('accounts:questionnaire_view')  # redirect to questionnaire page

            # Otherwise, go to home
            return redirect('feed:home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid email or password'})

    return redirect(reverse('accounts:load_login'))

# Commented out old OTP verification completely for reference:
"""
def verify_otp(request):
    ...
"""

@login_required
def answers_view(request):
    user = request.user
    questionnaire = UserQuestionnaire.objects.get(user=user)

    def to_list(value):
        return [v.strip() for v in value.split(',')] if value else []

    context = {
        'user': user,
        'questionnaire': questionnaire,
        'hobbies': to_list(questionnaire.hobbies_interests),
    }
    return render(request, 'accounts/ans.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserQuestionnaire, Profile

@login_required
def questionnaire_view(request):
    user = request.user

    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    # Redirect if user has already completed questionnaire
    if profile.has_answered_questionnaire:
        messages.info(request, "You have already completed the questionnaire.")
        return redirect('feed:home')

    # Choices
    looking_for_choices = [choice[0] for choice in UserQuestionnaire._meta.get_field('looking_for').choices]

    context = {
        'personality_choices': ['Introvert', 'Extrovert', 'A mix of both'],
        'comm_style_choices': ['Mostly texting', 'Voice & video calls', 'A bit of everything'],
        'hobbies_choices': ['Gaming', 'Music', 'Movies & Shows', 'Coding', 'Sports', 'Art & Design', 'Reading', 'Travel', 'Foodie'],
        'year_choices': ['1st Year', '2nd Year', '3rd Year', 'Final Year', 'Postgraduate'],
        'status_choices': ['Single', 'Taken', "It's Complicated", 'Focusing on me'],
        'looking_for_choices': looking_for_choices,
    }

    # Pre-fill if questionnaire exists
    try:
        questionnaire = UserQuestionnaire.objects.get(user=user)
        context['questionnaire'] = questionnaire
        if questionnaire.hobbies_interests:
            context['selected_hobbies'] = questionnaire.hobbies_interests.split(',')
    except UserQuestionnaire.DoesNotExist:
        questionnaire = None
        context['selected_hobbies'] = []

    if request.method == 'POST':
        data = request.POST

        # Validate required fields
        required_fields = ['personality', 'communication_style', 'year', 'relationship_status', 'looking_for']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            messages.error(request, f"Please fill in all required fields: {', '.join(missing_fields)}")
            return render(request, 'accounts/questionnaire.html', context)

        # Create or update questionnaire
        questionnaire, created = UserQuestionnaire.objects.get_or_create(user=user)
        questionnaire.personality = data.get('personality')
        questionnaire.communication_style = data.get('communication_style')
        questionnaire.year = data.get('year')
        questionnaire.relationship_status = data.get('relationship_status')
        questionnaire.looking_for = data.get('looking_for')

        # Handle hobbies
        hobbies_list = data.getlist('hobbies_interests')
        if len(hobbies_list) > 5:
            messages.error(request, "Please select a maximum of 5 hobbies.")
            return render(request, 'accounts/questionnaire.html', context)
        questionnaire.hobbies_interests = ','.join(hobbies_list)

        questionnaire.save()

        # Update profile
        profile.has_answered_questionnaire = True
        profile.save()

        messages.success(request, "Your profile is set up! Let's find your vibe.")
        return redirect('feed:home')

    return render(request, 'accounts/questionnaire.html', context)


@login_required
def edit_profile(request):
    user = request.user
    questionnaire, _ = UserQuestionnaire.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.bio = request.POST.get('bio')
        user.department = request.POST.get('department')
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        user.save()

        questionnaire.year = request.POST.get('year')
        questionnaire.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('feed:profile', user_id=request.user.id)

    return render(request, 'accounts/edit_profile.html', {
        'user': user,
        'questionnaire': questionnaire
    })


@login_required
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('accounts:login_signup')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login_signup')
