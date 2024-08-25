from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView 
# email 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Login 
from django.contrib.auth import authenticate, logout,login
from rest_framework.authtoken.models import Token

class PatientViewset(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer

class UserRegisterApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self , request):
        serializer = self.serializer_class(data= request.data)
      
        if serializer.is_valid():
              user = serializer.save()
              print(user)
              token = default_token_generator.make_token(user)
              print("token", token)
              uid = urlsafe_base64_encode(force_bytes(user.pk))
              confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}"
              email_subject = "Confirm Your Email"
              email_body = render_to_string("confirm_email.html", {"confirm_link": confirm_link })
              email = EmailMultiAlternatives(email_subject, " ", to=[user.email])
              email.attach_alternative(email_body, "text/html")
              email.send()

              return Response("Check Your Email Conframtion ")
        
        return Response(serializer.errors)


# actived on email verifections 
def actived(request , uid64 , token):
     try:
          uid = urlsafe_base64_decode(uid64).decode()
          user = User._default_manager.get(pk = uid)
     except(User.DoesNotExist):
          user = None 
    
     if user is not None and default_token_generator.check_token(user , token):
            user.is_active = True
            user.save()
            return redirect('register')
     else:
         return redirect('register')

     

# Login 

class UserLoginView(APIView):
     def post(self, request):
          serializer = serializers.UserLoginSerializer(data = self.request.data)
          if serializer.is_valid():
               username = serializer.validated_data["username"]
               password = serializer.validated_data["password"]

               user = authenticate(username = username , password = password)
               if user :
                    token, _ = Token.objects.get_or_create(user = user)
                    login(request, user)

                    return Response({'token' : token.key, 'user_id' : user.id})
               else : 
                    return Response({"error" : "Invalid Creditionals"})
               return Response(serializer.errors)


  