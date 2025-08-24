# portfolio/views.py
from django.shortcuts import render

PREVIEWS = [
  "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1522252234503-e356532cafd5?auto=format&fit=crop&w=1200&q=80",
  "https://images.unsplash.com/photo-1529101091764-c3526daf38fe?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?auto=format&fit=crop&w=1200&q=80",  
  "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1529101091764-c3526daf38fe?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1522252234503-e356532cafd5?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1542744173-05336fcc7ad4?auto=format&fit=crop&w=1200&q=80", 
  "https://images.unsplash.com/photo-1522252234503-e356532cafd5?auto=format&fit=crop&w=1200&q=80",
]


def home(request):
    links = [
        ("Michael H. Moore", "https://www.michaelhmoore.life/"),
        ("World AI X Summit", "https://www.worldaixsummit.com/"),
        ("The Lion You Don’t See", "https://www.thelionyoudontsee.com/"),
        ("NeuroMed AI", "https://www.neuromedai.org/"),
        ("Malcolm Global Logistics", "https://www.malcolmgloballogistics.com/"),
        ("Ingrid Cruysberghs", "https://www.ingridcruysberghs.com/"),
        ("Erica Shoeline PH", "https://www.ericashoelineph.com/"),
        ("Beyond Logistics (demo)", "https://beyondlogistics-production.up.railway.app/"),
        ("I Rise Up Academy", "https://www.iriseupacademy.com/"),
        ("i-Patchwork", "https://www.i-patchwork.com/"),
        ("Carmela AI (i-Patchwork)", "https://www.i-patchwork.com/carmela-ai/"),
        ("I Rise Up AI", "https://www.iriseup.ai/"),
        ("I Rise Up Publishing", "https://www.iriseuppublishing.com/"),
        ("0K Foundation", "https://www.0kfoundation.org/"),
    ]
    projects = [
        {"title": t, "url": u, "image": PREVIEWS[i % len(PREVIEWS)]}
        for i, (t, u) in enumerate(links)
    ]
    return render(
        request,
        "portfolio/index.html",
        {
            "projects": projects,
            "hero_image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1920&q=80",
            "headshot_url": "https://res.cloudinary.com/dkjtfjnlf/image/upload/f_auto,q_auto/juliavictorio_asmi2l.jpg",
        },
    )


# myApp/views.py
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from .forms import ContactForm

def contact_submit(request):
    if request.method != "POST":
        return redirect(reverse("home") + "#contact")

    form = ContactForm(request.POST)
    if not form.is_valid():
        # Store errors briefly via messages (or you can re-render a template)
        messages.error(request, "Please check the form and try again.")
        for field, errs in form.errors.items():
            messages.error(request, f"{field.capitalize()}: {', '.join(errs)}")
        return redirect(reverse("home") + "#contact")

    cd = form.cleaned_data
    to_email = getattr(settings, "CONTACT_TO", "juliavictorio16@gmail.com")

    subject = f"New inquiry from {cd['name']} — {cd.get('project_type') or 'Project'}"
    body = (
        f"Name: {cd['name']}\n"
        f"Email: {cd['email']}\n"
        f"Project Type: {cd.get('project_type')}\n"
        f"Budget: {cd.get('budget')}\n\n"
        f"Message:\n{cd['message']}\n"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", to_email),
        to=[to_email],
        reply_to=[cd["email"]],
    )

    try:
        email.send(fail_silently=False)
        messages.success(request, "Thanks! I got your message and will reply within 1 business day.")
    except Exception as e:
        messages.error(request, "Sorry, something went wrong sending your message. You can email me directly at juliavictorio16@gmail.com.")
        # Optional: log the exception e

    return redirect(reverse("home") + "#contact")


# myApp/views.py
import os, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

try:
    # New-style SDK
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    def chat_completion(messages):
        resp = client.chat.completions.create(
            model="gpt-4o-mini", temperature=0.6, messages=messages
        )
        return resp.choices[0].message.content
except Exception:
    # Fallback if older SDK is installed
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    def chat_completion(messages):
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", temperature=0.6, messages=messages
        )
        return resp["choices"][0]["message"]["content"]

SYSTEM_PROMPT = (
    "You are Julia’s website AI assistant. Be warm, clear, and concise. "
    "Help visitors understand Julia’s services (websites, AI assistants, coaching), "
    "process (plan/blueprint/build/launch), pricing expectations, typical timelines (1–3 weeks), "
    "and next steps. Use plain English. If asked for quotes, give friendly rough ranges and invite them "
    "to the contact form. When relevant, propose a short, actionable next step. "
    "Never promise legal/medical/financial advice. Keep answers under 6–8 sentences unless asked for more."
)

@csrf_exempt
def ai_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_msg = (data.get("message") or "").strip()
        history = data.get("history") or []  # [{role:'user'|'assistant', content:'...'}]

        if not user_msg:
            return JsonResponse({"error": "Empty message"}, status=400)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # keep last few turns
        for m in history[-6:]:
            r, c = m.get("role"), m.get("content")
            if r in ("user", "assistant") and c:
                messages.append({"role": r, "content": c})
        messages.append({"role": "user", "content": user_msg})

        answer = chat_completion(messages)
        return JsonResponse({"answer": answer})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
