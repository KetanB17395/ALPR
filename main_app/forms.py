from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms


from .models import RTSPUrlModel
__all__ = ['RTSPURLForm']


class RTSPURLForm(forms.ModelForm):
    # rtsp_url = forms.CharField(label="RTSP Url",max_length=255)

    class Meta:
        model = RTSPUrlModel
        fields = ['url']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Submit'))

    