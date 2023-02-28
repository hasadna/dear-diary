from django import forms


class FetchSingleItemForm(forms.Form):
    resource_id = forms.UUIDField()
    website = forms.CharField(initial="https://www.odata.org.il")
    force = forms.BooleanField()

STATUSES = [
    '',
    'Exception',
    'Success',
    'Skipped',
]

class DownloadReportSearchForm(forms.Form):
    resource_id = forms.UUIDField(required=False)
    status = forms.ChoiceField(choices = zip(STATUSES, STATUSES), required=False)
