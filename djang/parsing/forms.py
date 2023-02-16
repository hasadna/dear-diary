from django import forms


class FetchSingleItemForm(forms.Form):
    resource_id = forms.UUIDField()
    website = forms.CharField(initial="https://www.odata.org.il")
