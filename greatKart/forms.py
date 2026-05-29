from django import forms
from store . models import Person, State, LGA

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'state', 'lga']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_state'
            }),
            'lga': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_lga'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially set LGA as empty
        self.fields['lga'].queryset = LGA.objects.none()
        
        # If state is selected, load corresponding LGAs
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['lga'].queryset = LGA.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input, keep empty
        elif self.instance.pk:
            # If editing existing person, load their state's LGAs
            self.fields['lga'].queryset = self.instance.state.lgas.order_by('name')