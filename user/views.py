import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import TemplateView

from project import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from reward.models import ReceivedReward
from user.backend import EmailBackend
from user.forms import CustomUserCreationForm, CustomUserLoginForm, UserFormChange
from user.models import CustomUser, Card


def registration(request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponse(f"Você já está logado, mané")
    context = {}
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            mail_subject = 'Activate your account'
            message = render_to_string(
                'activation_email.html',
                {
                    'user': user,
                    'domain': settings.DOMAIN,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )
            send_mail(mail_subject, message, settings.EMAIL_HOST, [user.email], fail_silently=False)
            messages.add_message(request, messages.INFO, 'Sua conta está inativa, ative-a via e-mail.')
            return redirect("login")
        else:
            context['registration_form'] = form
    else:
        form = CustomUserCreationForm()
        context['registration_form'] = form
    return render(request, 'create.html', context=context)


def generate_verification_code():
    return str(random.randint(1000, 9999))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponse("Você já está logado, mané")

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = EmailBackend().authenticate(request, email=email, password=password)
            if user:
                verification_code = generate_verification_code()
                send_verification_code_email(user.email, verification_code)
                request.session['verification_code'] = verification_code
                request.session['user_id'] = user.id
                return redirect('verify_code')
            else:
                messages.warning(request, 'Usuário e/ou senha inválidos')
        else:
            messages.warning(request, 'Usuário e/ou senha inválidos')
    else:
        form = CustomUserLoginForm()

    context = {'login_form': form}
    return render(request, 'app/login.html', context=context)


def send_verification_code_email(email, verification_code):
    send_mail(
        'Verification Code',
        f'Your verification code is: {verification_code}',
        'testexpoints@gmail.com',
        [email],
        fail_silently=False,
    )


def verify_code(request):
    if request.user.is_authenticated:
        return HttpResponse("Você já está logado, mané")

    stored_code = request.session.get('verification_code')

    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')

        if entered_code == stored_code:
            user_id = request.session.get('user_id')
            user = CustomUser.objects.get(id=user_id)

            user.is_active = True
            user.save()

            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Logado com sucesso!')
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, 'Erro ao autenticar!')
            return redirect('verify_code')
    return render(request, 'verify_code.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Conta ativada e logada com sucesso!')
        return redirect('home')
    else:
        messages.add_message(request, messages.WARNING, 'Token inválido ou expirado!')
        return redirect('home')


def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Usuário deslogado com sucesso')
    return redirect('home')


class UserView(LoginRequiredMixin, TemplateView):

    def init_forms(self, request, post=None, files=None):
        self.user_form = UserFormChange(data=post, files=files, instance=request.user)
        self.cards = Card.objects.filter(user_id=request.user.id)
        self.rewards = ReceivedReward.objects.filter(retrieved_by_id=request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({"cards": self.cards, "rewards": self.rewards, "user_form": self.user_form})
        return context

    def get(self, request, *args, **kwargs):
        self.init_forms(request)
        context = self.get_context_data()
        return render(request, 'app/user.html', context)

    def post(self, request, *args, **kwargs):
        self.init_forms(request, request.POST, request.FILES)
        if self.user_form.is_valid():
            self.user_form.save()
            messages.info(request, 'Usuário atualizado com sucesso')
        context = self.get_context_data()
        return render(request, 'app/user.html', context)
