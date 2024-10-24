from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendant, Password, Clinic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Função home: Redireciona o atendente para o painel de senhas da sua clínica
@login_required
def home(request):
    try:
        # Verifica se o usuário é um superusuário e redireciona para o painel admin
        if request.user.is_superuser:
            return redirect('/admin/')  # Redireciona para o admin se for superusuário

        # Verifica se o usuário é um atendente
        attendant = Attendant.objects.get(user=request.user)

        # Redireciona para o painel de senhas da clínica do atendente
        return redirect('clinic:manage_passwords', clinic=attendant.clinic.name)

    except Attendant.DoesNotExist:
        # Se o usuário não for um atendente, exibe uma mensagem de erro
        return render(request, 'clinic/error.html', {'message': 'Você não é um atendente.'})

# Gerenciamento de senhas: Apenas as senhas da clínica do atendente são mostradas e manipuladas
@login_required
def manage_passwords(request, clinic):
    # Verifica se a clínica é válida
    clinic_obj = Clinic.objects.get(name=clinic)
    
    # Filtra as senhas e atendentes apenas da clínica atual
    attendant = Attendant.objects.get(user=request.user, clinic=clinic_obj)
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


# Painel de exibição: Exibe as senhas apenas para a clínica correspondente
def display_panel(request, clinic):
    clinic_obj = Clinic.objects.get(name=clinic)
    last_password = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called').first()
    recent_passwords = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called')[:6]

    context = {
        'last_password': last_password,
        'recent_passwords': recent_passwords,
        'clinic': clinic_obj  # Passa a clínica para o template
    }
    return render(request, 'clinic/display_panel.html', context)


# View para retornar a última senha chamada em formato JSON
def get_last_password(request, clinic):
    try:
        clinic_obj = Clinic.objects.get(name=clinic)
    except Clinic.DoesNotExist:
        return JsonResponse({'error': 'Clinic does not exist'}, status=404)

    last_password = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called').first()
    recent_passwords = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called')[:6]

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


# Certifique-se de que o CSRF está sendo tratado corretamente
@csrf_exempt  # Somente para testes, remova em produção!
def call_next_password(request, clinic=None):
    if request.method == 'POST':
        try:
            attendant = Attendant.objects.get(user=request.user)
            clinic_obj = attendant.clinic
            
            # Buscando a última senha chamada
            last_password = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called').first()
            next_number = last_password.number + 1 if last_password else 1
            
            # Criando uma nova senha
            new_password = Password.objects.create(
                number=next_number,
                counter=attendant.counter,
                called=True,
                clinic=clinic_obj
            )
            
            data = {
                'number': new_password.number,
                'counter': new_password.counter,
                'time_called': new_password.time_called.strftime("%H:%M")
            }
            return JsonResponse(data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_recent_passwords(request, clinic):
    clinic_obj = Clinic.objects.get(name=clinic)
    recent_passwords = Password.objects.filter(called=True, clinic=clinic_obj).order_by('-time_called')[:5]  # por exemplo, os últimos 5

    data = [
        {
            'number': p.number,
            'counter': p.counter,
            'time_called': p.time_called.strftime("%H:%M"),
        } for p in recent_passwords
    ]

    return JsonResponse(data, safe=False)