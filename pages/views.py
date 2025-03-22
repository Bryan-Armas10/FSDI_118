from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

# def contact(request):
#     return render(request, 'pages/contact.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Valid form")

            #name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            message_body = render_to_string("pages/email.html", request.POST)

            # send the email
            send_mail(
                "Portfolio email",
                message,
                email,
                ['bryan.armas@sdgku.edu'],
                html_message=message_body
            )

        else:
            print("Invalid form")
        
    else:
        form = ContactForm()

    return render(request, 'pages/contact.html', {'form': form})