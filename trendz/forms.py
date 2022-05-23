from django import forms
from django.core.exceptions import ValidationError
import datetime
#form for login
class Loginform(forms.Form):
    username = forms.CharField(label="Username", required=True, max_length=15)
    password = forms.CharField (widget=forms.PasswordInput)


class Registerform(forms.Form):
    username = forms.CharField(label="Username", required=True, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput,label="Password", required=True, max_length=15)
    confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm PW", required=True, max_length=15)

class Inputform(forms.Form):
    fs = forms.IntegerField(label="FS", required=False, help_text=" *Fasting blood Sugar mg/dL", max_value=300, min_value=10, widget=forms.NumberInput(attrs= {"step": "1"}))
    pp = forms.IntegerField(label="PP", required=False, help_text=" *Postprandial glucose mg/dL", max_value=500, min_value=50, widget=forms.NumberInput(attrs= {"step": "1"}))
    hba1c = forms.FloatField(label="HbA1c", required=False, help_text=" *Average Blood sugar (~3 months) %",  max_value=15, min_value=3, widget=forms.NumberInput(attrs={"step":"0.1"}))
    hb = forms.FloatField(label="HB", required=False, help_text=" *Haemoglobin(Hb) gm/dL",  max_value=20, min_value=2, widget=forms.NumberInput(attrs={"step":"0.1"}))
    rbc = forms.FloatField(label="RBC", required=False, help_text=" *Red Blood Cells(Erythrocytes) million/cub.mm",  max_value=8, min_value=1, widget=forms.NumberInput(attrs={"step":"0.01"}))
    wbc = forms.IntegerField(label="WBC", required=False, help_text=" *White Blood Cells(Leucocytes) cells/cub.mm",  max_value=50000, min_value=2000, widget=forms.NumberInput(attrs={"step":"1"}))
    pl = forms.IntegerField(label="PL", required=False, help_text=" *Platelets thousands/microLit", max_value=900, min_value=50, widget=forms.NumberInput(attrs= {"step": "1"}))
    cr = forms.FloatField(label="CR", required=False, help_text=" *Creatinine mg/dL",  max_value=10, min_value=0, widget=forms.NumberInput(attrs={"step":"0.01"}))
    date = forms.DateField(label="Date", required=True,  widget=forms.SelectDateWidget(years=[x for x in range(2010,2031)]), initial=datetime.date.today) 