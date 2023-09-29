from django.conf import settings
from django.contrib.auth import login, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
import jwt, datetime

from main.models import Modul
from api.serializers import ModulSerializer

from .models import CustomUser

# Create your views here.

class LoginAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not Found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Wrong Password!")
        
        payload = {
            'id': user.id,
            'fullname': user.fullname,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        auth = authenticate(email=email, password=password)
        login(request, auth)

        response.data = {
            'jwt': token
        }

        return response

class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request):
        user = request.user
        queryset = Modul.objects.all()
        token = request.COOKIES.get('jwt') 
        
        if not token:
            raise AuthenticationFailed('Unautehnticated!')
        
        if user.is_staff:  # Jika pengguna adalah admin, tampilkan semua modul
            pass
        else:
            # Ambil izin-izin yang sesuai dengan kategori modul dan buat daftar izin
            category_permissions = {
                'main.can_view_frontend_modul': 'FrontEnd',
                'main.can_view_backend_modul': 'BackEnd',
                'main.can_view_qa_modul': 'QA',
                'main.can_view_ui/ux_modul': 'UI/UX',
            }
            
            allowed_categories = [category for permission, category in category_permissions.items() if user.has_perm(permission)]
            status = ['published']
            # Filter queryset berdasarkan kategori yang diizinkan
            queryset = queryset.filter(category__name__in=allowed_categories, status__in=status)

        serializer = ModulSerializer(queryset, many=True)
        return Response({'status': 'success', 'message': 'Success listing data', 'data': serializer.data}) 

    

class LogoutAPI(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'messages': 'success'
        }

        return response
