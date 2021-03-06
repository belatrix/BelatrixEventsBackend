from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.db.models import Q
from django.shortcuts import get_object_or_404
from re import match as regex_match
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import NotAcceptable, ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response

from .models import User, Participant, Role
from .permissions import IsStaff
from .serializers import UserSerializer, UserCreationSerializer
from .serializers import UserUpdatePasswordSerializer, UserProfileSerializer, RoleSerializer
from .serializers import EventProfileSerializer, IdeaProfileSerializer, AttendanceProfileSerializer
from .serializers import AuthorProfileSerializer

from events.models import Event, EventParticipant, Attendance
from ideas.models import IdeaCandidate, IdeaParticipant, Idea


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def user_detail(request, user_id):
    """
    Returns user detail
    ---
    GET:
        response_serializer: participants.serializers.UserSerializer
    """
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_list(request):
    """
    Returns user list
    ---
    GET:
        response_serializer: participants.serializers.UserSerializer
        parameters:
            - name: search
              description: search terms
              type: string
              required: false
              paramType: query
    """
    users = User.objects.filter(is_active=True)

    if request.GET.get('search'):

        full_search_terms = request.GET.get('search')
        search_terms_array = full_search_terms.split()

        if len(search_terms_array) > 0:
            for term in search_terms_array:
                users = users.filter(Q(full_name__icontains=term) | Q(email__icontains=term))

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def user_profile(request):
    """
    Returns user profile
    ---
    GET:
        response_serializer: participants.serializers.UserSerializer
        parameters:
            - name: id
              description: user id
              type: int
              required: false
              paramType: query
    """
    if request.GET.get('id'):
        user = get_object_or_404(User, pk=request.GET.get('id'))
    else:
        user = request.user

    events = EventParticipant.objects.filter(participant=user)
    events_serializer = EventProfileSerializer(events, many=True)
    candidate_ideas = IdeaCandidate.objects.filter(user=user)
    candidate_serializer = IdeaProfileSerializer(candidate_ideas, many=True)
    participant_ideas = IdeaParticipant.objects.filter(user=user)
    participant_serializer = IdeaProfileSerializer(participant_ideas, many=True)
    attendances = Attendance.objects.filter(participant=user)
    attendance_serializer = AttendanceProfileSerializer(attendances, many=True)
    author_ideas = Idea.objects.filter(author=user)
    author_serializer = AuthorProfileSerializer(author_ideas, many=True)
    serializer = UserSerializer(user)

    return Response({"user": serializer.data,
                     "events": events_serializer.data,
                     "candidate": candidate_serializer.data,
                     "participant": participant_serializer.data,
                     "author": author_serializer.data,
                     "attendance": attendance_serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def user_creation(request):
    """
    Create user account
    ---
    POST:
        serializer: participants.serializers.UserCreationSerializer
        response_serializer: participants.serializers.UserSerializer
    """
    if request.method == 'POST':
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = str(serializer.validated_data['email']).lower()

        if not regex_match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ParseError("Correo invalido.")

        random_password = User.objects.make_random_password(length=4, allowed_chars='hacktrx23456789')
        subject = "[Hackatrix] Usuario creado para la Hackatrix"
        message = "Su clave temporal, que debe cambiar es: %s" % (random_password)

        try:
            new_user = User.objects.create_user(email, password=random_password)
            new_user.save()
        except Exception as e:
            print(e)
            raise NotAcceptable('Correo ya registrado.')

        participant = Participant.objects.filter(email=new_user.email)
        if len(participant) == 1:
            event = Event.objects.filter(pk=participant[0].event_id)
            if len(event) == 1:
                new_user.full_name = participant[0].full_name
                new_user.save()
                EventParticipant.objects.create(event=event[0], participant=new_user)

        try:
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
        except Exception as e:
            print(e)
            content = {'detail: Problemas con el envio de correo electronico'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = UserSerializer(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, ))
def user_update(request):
    """
    Update user data
    ---
    PATCH:
        serializer: participants.serializers.UserProfileSerializer
        response_serializer: participants.serializers.UserSerializer
    """
    if request.method == 'PATCH':
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            current_user = request.user

            if 'full_name' in serializer.validated_data:
                current_user.full_name = serializer.validated_data['full_name']
            else:
                current_user.full_name = None

            if 'phone_number' in serializer.validated_data:
                current_user.phone_number = serializer.validated_data['phone_number']
            else:
                current_user.phone_number = None

            if 'role_id' in serializer.validated_data:
                role_id = serializer.validated_data['role_id']
                current_user.role = Role.objects.get(pk=role_id)
            else:
                current_user.role = None

            current_user.save()
            serializer = UserSerializer(current_user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((IsAuthenticated, ))
def user_update_password(request):
    """
    Update user password
    ---
    PATCH:
        serializer: participants.serializers.UserUpdatePasswordSerializer
        response_serializer: participants.serializers.UserSerializer
    """
    if request.method == 'PATCH':
        serializer = UserUpdatePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

        user = request.user

        if current_password == new_password:
            raise ValidationError('Passwords iguales')
        elif user.check_password(current_password):
            user.set_password(new_password)
            user.is_password_reset_required = False
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            raise ValidationError('Password actual incorrecto')


@api_view(['POST', ])
def user_password_recovery_request(request):
    """
    Request user password recovery
    ---
    POST:
        serializer: participants.serializers.UserCreationSerializer
    """
    if request.method == 'POST':
        try:
            email = request.data['email']
        except Exception as e:
            print(e)
            raise ValidationError('Datos incompletos')

        user = get_object_or_404(User, email=email)

        user.generate_reset_password_code()

        subject = "[Hackatrix] Password nuevo solicitado"

        draft_message = """
        Una solicitud de restablecimiento de password ha sido recibida.
            Su password temporal es: %s
            Confirme su solicitud dando clic en el siguiente enlace: %s
        Si usted no solicito ningun restablecimiento, ignore este correo."""

        current_site = Site.objects.get_current()
        user_reset_confirmation_api = reverse("users:user_password_recovery_request")
        reset_url = current_site.domain + user_reset_confirmation_api + user.reset_password_code
        message = draft_message % (user.temporary_password, reset_url)

        try:
            send_email = EmailMessage(subject, message, to=[user.email])
            send_email.send()
        except Exception as e:
            print(e)
            content = {'detail: Problemas con el envio de correo electronico'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(status=status.HTTP_200_OK)


@api_view(['GET', ])
@renderer_classes((StaticHTMLRenderer,))
def user_password_recovery_confirmation(request, user_uuid):
    """
    Confirm password recovery action
    """
    if request.method == 'GET':
        user = get_object_or_404(User, reset_password_code=user_uuid)
        user.set_password(user.temporary_password)
        user.reset_password_code = None
        user.temporary_password = None
        user.is_password_reset_required = True
        user.save()
        data = "<h1>Solicitud de reestablecimiento de password confirmada.</h1>"
        return Response(data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def user_roles(request):
    """
    Return user roles
    ---
    GET:
        response_serializer: participants.serializers.RoleSerializer
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Authenticate user with provided credentials
        ---
        serializer: participants.serializers.UserAuthenticationSerializer
        response_serializer: participants.serializers.UserAuthenticationResponseSerializer
        """
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
            'is_jury': user.is_jury,
            'is_moderator': user.is_moderator,
            'is_active': user.is_active,
            'is_blocked': user.is_blocked,
            'is_password_reset_required': user.is_password_reset_required,
        })


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def user_logout(request):
    """
    Logout current user
    """
    logout(request)
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH', ])
@permission_classes((IsStaff, ))
def user_activation(request, user_id):
    """
    Deactivate user
    ---
    PATCH:
        response_serializer: participants.serializers.UserSerializer
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
