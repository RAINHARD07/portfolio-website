from django import forms

from .models import ContactSubmission


class ContactSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ("name", "email", "subject", "message_body")

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_message_body(self):
        return self.cleaned_data["message_body"].strip()
