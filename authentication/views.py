from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule
from .serializers import StudentUserSerializer, ClassSerializer, ScheduleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from project import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

def home(request):
    return render(request, "authentication/signin.html")

def home_page(request):
    fname = request.session.get('fname', '') 
    return render(request, "authentication/index.html", {'fname': fname})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('home')
        
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your account has been created successfully! Please check your email to confirm your address and activate your account.")
        
        # Welcome Email
        subject = "Welcome to GFG - Django Login!"
        message = render_to_string('welcome_email.html', {'name': myuser.first_name})
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True, html_message=message)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email at GFG - Django Login!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.content_subtype = "html"
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
    
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            request.session['fname'] = user.first_name
            return redirect('home_page')  
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin') 
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

class StudentUserViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho StudentUser (Học viên)
    """
    queryset = StudentUser.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClassViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho Class (Lớp học)
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

from rest_framework.decorators import action
from rest_framework.response import Response

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def student_schedule(self, request):
        """
        API lấy thời khóa biểu của học viên theo student_code
        """
        student_code = request.query_params.get('student_code')
        if not student_code:
            return Response({"error": "Thiếu mã học viên (student_code)"}, status=400)

        try:
            student = StudentUser.objects.get(student_code=student_code)
            schedules = Schedule.objects.filter(class_assigned__students=student)
            serializer = self.get_serializer(schedules, many=True)
            return Response(serializer.data)
        except StudentUser.DoesNotExist:
            return Response({"error": "Học viên không tồn tại"}, status=404)

def schedule_list(request):
    schedules = Schedule.objects.all().values(
        "class_assigned__class_name", "teacher__username", "day_of_week",
        "session", "start_time", "end_time", "room"
    )
    return JsonResponse(list(schedules), safe=False)

