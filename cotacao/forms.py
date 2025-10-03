# cotacao/forms.py

from django import forms
from .models import CadCliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = CadCliente
        # Defina quais campos do seu modelo você quer que apareçam no formulário.
        
        fields = [
            'razaoSocial', 'cnpj', 'inscEstadual', 'inscMunicipal', 
            'logradouro', 'numeroLogradouro', 'bairro', 'cidade', 
            'estado', 'sgEstado', 'pais', 'cep', 'telefone', 'email', 
            'situacao'
        ]
        
        # Opcional: Adicionar classes CSS do Bootstrap
        widgets = {
            'razaoSocial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão Social Completa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numeroLogradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'sgEstado': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 2,'placeholder':'Apenas 2 Caracteres EX: "PR"'}),
            'pais': forms.TextInput(attrs={'class':'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números', 'maxlength': 8}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Você deve continuar para todos os campos...
        }