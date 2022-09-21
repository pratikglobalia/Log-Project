from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
# from .tasks import send_mail_to_user

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response({'Data Register Successfully!!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            uemail = serializer.validated_data['email']
            upass = serializer.validated_data['password']
            user = authenticate(email=uemail, password=upass)
            if user is not None:
                login(request, user)
                token = get_tokens_for_user(user)
                data = {
                    'email' : serializer.validated_data['email'],
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'phone_no' : user.phone_no,
                    'token' : token
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)
            return Response({'Invalid email or password!!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class FindIndexView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        userdata = FindIndex.objects.filter(user=request.user).first()
        if FindIndex.objects.filter(user=request.user).exists():
            findex = FindIndex.objects.get(id=userdata.id)
            serializerdata = FindIndexSerializer(findex, data=request.data, partial=True)
            if serializerdata.is_valid():
                serializerdata.save()  
                return Response({'Data Updated!!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = FindIndexSerializer(data=request.data)
            if serializer.is_valid():    
                serializer.save(user=request.user)
                return Response({'Data Saved!!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SendMailSerializer(data=request.data)
        if serializer.is_valid():
            send_to = serializer.validated_data['send_to']
            recipient_list = list(CustomUser.objects.filter(id__in=send_to).values_list('email',flat=True))
            findexdata = FindIndex.objects.filter(user=request.user).first()
            user = request.user.first_name
            try:
                if findexdata is None:       
                    logdata = list(Log.objects.filter(created_by=request.user).values())
                    # send_mail_to_user.delay(recipient_list, logdata, user)
                    return Response({'Mail Sent!!'}, status=status.HTTP_200_OK)           
                else:
                    logobj = Log.objects.filter(created_by=request.user)
                    logdata = []
                    for i in findexdata.log_data:
                        for j in logobj.values(i):
                            logdata.append(j)
                    # send_mail_to_user.delay(recipient_list,logdata, user)
                    return Response({'Mail Sent!!'}, status=status.HTTP_200_OK)                   
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        