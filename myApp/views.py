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


import json, os
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape

import stripe

# --- Stripe keys ---
stripe.api_key = settings.STRIPE_SECRET_KEY

def _usd_cents(amount_str: str) -> int:
    """Sanitize to positive USD cents."""
    try:
        amt = Decimal(amount_str or "0").quantize(Decimal("0.01"))
        if amt <= 0:
            return 0
        return int(amt * 100)
    except Exception:
        return 0

# ========== Widget page ==========
def widget(request):
    """
    Render the iframe-friendly donation form.
    URL: /donate/widget?org=solutions-for-change
    """
    org = request.GET.get("org", "solutions-for-change")
    context = {"org": org, "publishable_key": settings.STRIPE_PUBLISHABLE_KEY}
    return render(request, "solutions_for_change.html", context)

# ========== Create Checkout Session ==========
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        custom_amount = data.get("amount")
        recurring_amount = data.get("recurring")

        donor = {
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "email": data.get("email", ""),
            "mobile": data.get("mobile", ""),
            "address": data.get("address", ""),
            "city": data.get("city", ""),
            "state": data.get("state", ""),
            "country": data.get("country", ""),
            "postal_code": data.get("postal_code", ""),
            "message": data.get("message", ""),
            "org": data.get("org", "solutions-for-change"),
        }

        def usd_cents(s):
            from decimal import Decimal
            try:
                val = Decimal(s or "0").quantize(Decimal("0.01"))
                return int(val * 100) if val > 0 else 0
            except Exception:
                return 0

        # ➜ MONTHLY (no pre-created Product needed)
        if recurring_amount:
            unit_amount = usd_cents(recurring_amount)
            if unit_amount <= 0:
                return HttpResponseBadRequest("Invalid monthly amount")

            try:
                session = stripe.checkout.Session.create(
                    mode="subscription",
                    payment_method_types=["card"],
                   
                    line_items=[{
                        "quantity": 1,
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": unit_amount,
                            "recurring": {"interval": "month"},
                            "product_data": {"name": "Monthly Donation"},
                        },
                    }],
                    success_url=f"{settings.DOMAIN}/donate/success",
                    cancel_url=f"{settings.DOMAIN}/donate/cancel",
                    metadata=donor,
                    subscription_data={"metadata": donor},
                )
                return redirect(session.url, code=303)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

        # ➜ ONE-TIME (unchanged – also no product needed)
        amount = usd_cents(custom_amount)
        if amount <= 0:
            return HttpResponseBadRequest("Invalid amount")
        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                customer_creation="if_required",
                line_items=[{
                    "quantity": 1,
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": amount,
                        "product_data": {"name": "Donation"},
                    }
                }],
                success_url=f"{settings.DOMAIN}/donate/success",
                cancel_url=f"{settings.DOMAIN}/donate/cancel",
                metadata=donor,
                payment_intent_data={"metadata": donor},
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# ========== Webhook ==========
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")

    # Handle a few key events
    if event["type"] == "checkout.session.completed":
        # For one-time payments, you can read event.data.object.payment_intent
        # For subscriptions, event.data.object.subscription will be set
        session = event["data"]["object"]
        # TODO: record to DB / send internal email if needed
        # metadata = session.get("metadata", {})
    elif event["type"] in ("invoice.paid", "customer.subscription.created"):
        pass
    elif event["type"] in ("invoice.payment_failed", "customer.subscription.deleted"):
        pass

    return HttpResponse(status=200)
