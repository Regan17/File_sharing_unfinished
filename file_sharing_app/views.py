from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer
from .tokens import generate_token
from .models import CustomUser
from .serializers import CustomUserSerializer, FileSerializer
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import File
from .serializers import FileSerializer
from .forms import FileUploadForm
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

class OpsFileUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (FileUploadParser,)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        print("Request Data:", request.data)

        # Simplified for debugging purposes
        return Response({'message': 'Received the file successfully!'}, status=status.HTTP_200_OK)

class FileDownloadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id, *args, **kwargs):
        # Ensure the user has permission to download the file
        file_object = get_object_or_404(File, id=file_id, user=request.user)

        # Prepare the file for download
        file_path = file_object.file_url.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_object.file_url.name}"'
            return response
        
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        # user.profile.signup_confirmation = True
        user.save()
        login(request,user)
        messages.success(request, "Your Account has been activated!!")
        if user.is_ops_user:
           return redirect('Opsignin')
        else:
            return redirect('client_login')
    else:
        return render(request,'file_sharing_app/index.html')


def index(request):
    return render(request,'file_sharing_app/index.html')


def ops_login(request):
    if request.method == "POST":
        # Implement Ops User login logic
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        user = authenticate(username=username, password=password)

        if user is not None and user.is_ops_user:
            login(request, user)
            messages.success(request, 'Logged in successfully as Ops User')
            return render(request,'file_sharing_app/ggl.html')
        else:
            messages.error(request, 'Invalid Ops User credentials')
            return redirect('Opsignin')

    return render(request, "file_sharing_app/ops_login.html")


class FileUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            # Check file type before saving
            allowed_types = ['pptx', 'docx', 'xlsx']
            file_extension = file_serializer.validated_data['file'].name.split('.')[-1].lower()

            if file_extension not in allowed_types:
                return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def client_user_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('home')

        # if CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, "Email is already registered!")
        #     return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        # Create a new instance of CustomUser
        client_user = CustomUser.objects.create_user(username, email, pass1)
        client_user.first_name = fname
        client_user.last_name = lname

        # Check if the checkbox is checked
        is_ops_user = request.POST.get('is_ops_user', False)
        client_user.is_ops_user = bool(is_ops_user)

        client_user.is_active = False
        client_user.save()

        messages.success(request, "Your account has been created successfully! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to GFG - Django Login!!"
        message = f"Hello {client_user.first_name}!\nWelcome to GFG!\nThank you for visiting our website. We have also sent you a confirmation email. Please confirm your email address.\n\nThanking You\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [client_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        # activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        message2 = render_to_string('email_confirmation.html', {
            'name': client_user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(client_user.pk)),
            'token': generate_token.make_token(client_user),
            # 'activation_url': activation_url,
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [client_user.email],
        )
        email.fail_silently = True
        email.send()

        if client_user.is_ops_user:
           return redirect('Opsignin')
        else:
            return redirect('client_login')

    return render(request, "file_sharing_app/client_user_signup.html")
def client_user_login(request):
    if request.method == "POST":
        # Implement client user login logic
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")
        user = authenticate(username=username, password=password)

        if user is not None and not user.is_ops_user:
            login(request, user)
            messages.success(request, 'Logged in successfully as Client User')
            return render(request,'file_sharing_app/fb.html')
        else:
            messages.error(request, 'Invalid Client User credentials')
            return redirect('client_login')

    return render(request, "file_sharing_app/client_user_login.html")

# def ops_user_upload_file(request):
#     file_type = request.POST.get('file_type')
#     file_obj = request.FILES.get('file')

#     # Check file type
#     allowed_types = ['pptx', 'docx', 'xlsx']
#     file_extension = file_obj.name.split('.')[-1].lower()
#     if file_extension not in allowed_types:
#         return JsonResponse({'error': 'Invalid file type'}, status=400)

#     # Save file to the database
#     new_file = File.objects.create(user=request.user, file_type=file_extension)
#     new_file.file_url = file_obj
#     new_file.save()

#     serializer = FileSerializer(new_file)
#     return JsonResponse(serializer.data, status=201)
def signout(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully!!")
        
    else:
        messages.warning(request, "You are not signed in. Sign in first to logout.")
    return redirect('home')
