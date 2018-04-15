from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from re import match as regex_match
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


@api_view(['GET', ])
def user_detail(request, user_id):
    """
    Returns user detail
    """
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def user_creation(request):
    if request.method == 'POST':
        email = request.data['email'].lower()

        if not regex_match(r"[^@]+@[^@]+\.[^@]+", email):
            content = {'detail: Correo invalido'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        random_password = User.objects.make_random_password(length=4, allowed_chars='hacktrx23456789')
        subject = "[Hackatrix] Usuario creado para la Hackatrix"
        message = "Su clave temporal, que debe cambiar es: %s" % (random_password)

        try:
            new_user = User.objects.create_user(email, password=random_password)
            new_user.save()
        except Exception as e:
            print(e)
            content = {'detail: Correo ya registrado'}
            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
        except Exception as e:
            print(e)
            content = {'detail: Problemas con el envio de correo electronico'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        content = {'detail: Correo registrado correctamente'}
        return Response(content, status=status.HTTP_201_CREATED)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, ))
def user_update_password(request, user_id):
    if request.method == 'PATCH':
        try:
            current_password = request.data['current_password']
            new_password = request.data['new_password']
        except Exception as e:
            print (e)
            raise ValidationError('Datos incompletos')
        user = get_object_or_404(User, pk=user_id)
        if current_password == new_password:
            raise ValidationError('Passwords iguales')
        elif user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            raise ValidationError('Password actual incorrecto')


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_participant': user.is_participant
        })
