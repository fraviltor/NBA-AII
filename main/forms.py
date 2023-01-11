from django import forms

class PlayerBusquedaForm(forms.Form):
    player_name = forms.CharField(label="Nombre de Jugador", widget=forms.TextInput, required=True)
