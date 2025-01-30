from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import LoginForm, StudentProfilForm, EmployeeProfilForm
from .models import student, Employee,Person
from django.contrib.auth.models import User


def get_logged_user_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        if student.objects.filter(id=logged_user_id).exists():
            return student.objects.get(id=logged_user_id)
        elif Employee.objects.filter(id=logged_user_id).exists():
            return Employee.objects.get(id=logged_user_id)
    return None

def welcome(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Vérification de l'utilisateur (dans le modèle Student ou Employee)
            user = student.objects.filter(email=email, password=password).first() or \
                   Employee.objects.filter(email=email, password=password).first()

            if user:
                # Création de la session pour l'utilisateur connecté
                request.session['user_id'] = user.id
                request.session['user_type'] = 'employee' if isinstance(user, Employee) else 'student'
                messages.success(request, "Connexion réussie.")
                return redirect('bienvenue')  # Redirige vers la page bienvenue
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez remplir correctement le formulaire.")

    else:
        form = LoginForm()

    return render(request, 'pr1.html', {'form': form})

    



def register(request):
    user_type = request.POST.get('user_type', 'student')  # Type d'utilisateur : student par défaut

    if request.method == 'POST':
        # Initialisation du formulaire approprié
        if user_type == 'student':
            form = StudentProfilForm(request.POST)
        else:  # user_type == 'employee'
            form = EmployeeProfilForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            model = student if user_type == 'student' else Employee

            if model.objects.filter(email=email).exists():
                messages.error(request, f"{'Étudiant(e)' if user_type == 'student' else 'Employé(e)'} avec cet email existe déjà.")
            else:
                # Enregistrement de l'utilisateur
                user = form.save(commit=False)
                user.password = form.cleaned_data.get('password')  # Assurez-vous de hacher le mot de passe si nécessaire
                user.save()
                messages.success(request, f"{'Étudiant(e)' if user_type == 'student' else 'Employé(e)'} enregistré(e) avec succès !")
                return redirect('welcome')  # Redirection après succès

    # Si GET ou erreurs de validation
    student_form = StudentProfilForm() if user_type == 'student' else None
    employee_form = EmployeeProfilForm() if user_type == 'employee' else None

    return render(request, 'user_profile.html', {
        'user_type': user_type,
        'student_form': student_form,
        'employee_form': employee_form,
    })

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect



from .models import Message, Friend  # Importez le modèle Friend

import django.db.models as models
def bienvenue(request):
    # Récupérer les données utilisateur depuis la session
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if not user_id:
        return redirect('welcome')  # Redirection si non connecté

    # Récupération de l'utilisateur
    if user_type == 'student':
        user = student.objects.get(id=user_id)
        extra_info = user.cursus
    else:
        user = Employee.objects.get(id=user_id)
        extra_info = user.office

    if not hasattr(user, 'full_name'):
        user.full_name = f"{user.first_name} {user.last_name}"

    # Récupération des messages publiés par l'utilisateur
    if user_type == 'student':
        user_messages = Message.objects.filter(student=user).order_by('-date_publication')[:5]
    else:
        user_messages = Message.objects.filter(employee=user).order_by('-date_publication')[:5]

    # Récupérer les amis de l'utilisateur
    user_friends = user.amis.all()
    amis_ids = user_friends.values_list('id', flat=True)

    # Récupération des messages des amis
    messages_amis = Message.objects.filter(
        models.Q(student__id__in=amis_ids) | models.Q(employee__id__in=amis_ids)
    ).order_by('-date_publication')[:5]


    # Gestion des actions
    if request.method == "POST":
        if 'publish_message' in request.POST:
            # Publier un message
            new_message = request.POST.get("message", "").strip()
            if new_message:
                if user_type == 'student':
                    Message.objects.create(contenu=new_message, student=user)
                else:
                    Message.objects.create(contenu=new_message, employee=user)
        elif 'add_friend' in request.POST:
            # Ajouter un ami
            new_friend_email = request.POST.get("friend_name", "").strip()
            try:
                if user_type == 'student':
                    new_friend = student.objects.get(email=new_friend_email)
                else:
                    new_friend = Employee.objects.get(email=new_friend_email)
                user.amis.add(new_friend)
            except (student.DoesNotExist, Employee.DoesNotExist):
                pass  # Si l'ami n'existe pas, ne rien faire

    # Récupération des derniers amis ajoutés
    user_recent_friends = user.amis.all().order_by('-id')[:5]

    return render(request, 'bienvenue.html', {
        'user': user,
        'user_type': user_type,
        'extra_info': extra_info,
        'user_messages': user_messages,
        'messages_amis': messages_amis,
        'user_friends': user_recent_friends,
    })






    return render(request, 'bienvenue.html', {
        'user': user,
        'messages_amis': messages_amis,
        'amis': amis,
        'user_messages': user_messages,  # Ajoutez cette clé
    })



def logout(request):
    # Supprimer toutes les données de la session
    request.session.flush()
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('welcome')  # Redirige vers la page de connexion


from django.shortcuts import get_object_or_404

def modifier_profil(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    if not user_id:
        return redirect('welcome')

    # Récupération de l'utilisateur connecté
    if user_type == 'student':
        user = get_object_or_404(student, id=user_id)
        form_class = StudentProfilForm
    else:
        user = get_object_or_404(Employee, id=user_id)
        form_class = EmployeeProfilForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('bienvenue')
    else:
        form = form_class(instance=user)

    return render(request, 'modifier_profil.html', {'form': form, 'user': user})

def voir_profil(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
    if not user_id:
        return redirect('welcome')

    # Récupération de l'utilisateur connecté
    if user_type == 'student':
        user = get_object_or_404(student, id=user_id)
    else:
        user = get_object_or_404(Employee, id=user_id)

    return render(request, 'voir_profil.html', {'user': user, 'user_type': user_type})