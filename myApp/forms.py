# myApp/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    project_type = forms.ChoiceField(choices=[
        ("Website", "Website"),
        ("AI Assistant", "AI Assistant"),
        ("Both", "Both (Website + AI)"),
        ("Other", "Other"),
    ], required=False)
    budget = forms.ChoiceField(choices=[
        ("Not sure yet", "Not sure yet"),
        ("Under ₱50k", "Under ₱50k"),
        ("₱50k–₱100k", "₱50k–₱100k"),
        ("₱100k+", "₱100k+"),
    ], required=False)
    message = forms.CharField(widget=forms.Textarea)
    hp = forms.CharField(required=False)  # honeypot

    def clean_hp(self):
        if self.cleaned_data.get("hp"):
            raise forms.ValidationError("Spam detected.")
        return ""
