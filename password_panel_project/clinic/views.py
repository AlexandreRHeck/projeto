from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendant, Password, Clinic
from django.http import JsonResponse
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Verifica se o usuário é atendente e redireciona para o painel de gerenciamento
@login_required
def home(request):
    try:
        # Verifica se o usuário é um superusuário e redireciona para o painel admin
        if request.user.is_superuser:
            return redirect('/admin/')  # Redireciona para o admin se for superusuário

        # Verifica se o usuário é um atendente
        attendant = Attendant.objects.get(user=request.user)
        return redirect('clinic:manage_passwords')  # Redireciona para o painel de senhas
    except Attendant.DoesNotExist:
        # Se o usuário não for um atendente, exiba uma mensagem de erro
        return render(request, 'clinic/error.html', {'message': 'Você não é um atendente.'})

# Página de gerenciamento de senhas
@login_required
def manage_passwords(request, clinic):
    attendant = Attendant.objects.get(user=request.user)
    clinic_obj = Clinic.objects.get(name=clinic)  # Obtém a clínica pelo nome passado

    last_password = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called').first()

    if request.method == 'POST':
        next_number = last_password.number + 1 if last_password else 1
        new_password = Password.objects.create(
            number=next_number,
            counter=attendant.counter,
            called=True,
            clinic=clinic_obj  # Associa a nova senha à clínica
        )
        new_password.save()

    context = {
        'last_password': last_password,
        'clinic': clinic_obj
    }
    return render(request, 'clinic/manage_passwords.html', context)

# View para o painel de visualização (exibido aos pacientes)
def display_panel(request, clinic):
    last_password = Password.objects.filter(called=True, clinic__name=clinic).order_by('-time_called').first()
    recent_passwords = Password.objects.filter(called=True, clinic__name=clinic).order_by('-time_called')[:6]

    context = {
        'last_password': last_password,
        'recent_passwords': recent_passwords,
        'clinic': clinic  # Certifique-se de que o nome da clínica está sendo passado para o template
    }
    return render(request, 'clinic/display_panel.html', context)


# View para retornar a última senha chamada em formato JSON
def get_last_password(request, clinic):
    last_password = Password.objects.filter(called=True, clinic__name=clinic).order_by('-time_called').first()
    recent_passwords = Password.objects.filter(called=True, clinic__name=clinic).order_by('-time_called')[:6]

    if last_password:
        data = {
            'number': last_password.number,
            'counter': last_password.counter,
            'time_called': last_password.time_called.strftime("%H:%M"),
            'recent_passwords': [
                {
                    'number': p.number,
                    'counter': p.counter,
                    'time_called': p.time_called.strftime("%H:%M")
                } for p in recent_passwords
            ]
        }
    else:
        data = {
            'number': None,
            'counter': None,
            'time_called': None,
            'recent_passwords': []
        }

    return JsonResponse(data)

# View para retornar o histórico recente de senhas chamadas
def get_recent_passwords(request, clinic):
    recent_passwords = Password.objects.filter(called=True, clinic__name=clinic).order_by('-time_called')[:6]
    
    data = [
        {
            'number': password.number,
            'counter': password.counter,
            'time_called': password.time_called.strftime("%H:%M")
        } for password in recent_passwords
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def call_next_password(request, clinic=None):  # Certifique-se de aceitar o argumento 'clinic' apenas se for necessário
    if request.method == 'POST':
        attendant = Attendant.objects.get(user=request.user)
        clinic = attendant.clinic

        # Buscar a última senha chamada
        last_password = Password.objects.filter(called=True, clinic=clinic).order_by('-time_called').first()
        next_number = last_password.number + 1 if last_password else 1

        new_password = Password.objects.create(
            number=next_number,
            counter=attendant.counter,
            called=True,
            clinic=clinic
        )
        new_password.save()

        # Retorna a senha chamada como JSON
        data = {
            'number': new_password.number,
            'counter': new_password.counter,
            'time_called': new_password.time_called.strftime("%H:%M")
        }

        return JsonResponse(data)