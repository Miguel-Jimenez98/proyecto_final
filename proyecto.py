import pandas as pd
import math

# Datos simulados del usuario
usuario = {
    'zona': 'La Guajira',
    'consumo_diario_kWh': 12
}

# Cargar datos de zonas
zonas = pd.read_csv('zonas_no_interconectadas.csv')
zona_data = zonas[zonas['Zona'] == usuario['zona']].iloc[0]
irradiacion = zona_data['Irradiacion_solar']

# Cargar catálogo de equipos
catalogo = pd.read_csv('catalogo_equipos.csv')

# Supuestos para paneles y baterías
horas_sol = irradiacion
cap_panel = 400  # W
cap_bateria = 2400  # Wh
consumo = usuario['consumo_diario_kWh']

n_paneles = math.ceil((consumo * 1000 / horas_sol) / cap_panel)
n_baterias = math.ceil((consumo * 1000 * 2) / cap_bateria)  # backup 2 días

precio_panel = catalogo.loc[catalogo['Tipo'] == 'Panel Solar', 'Precio (USD)'].values[0]
precio_bateria = catalogo.loc[catalogo['Tipo'] == 'Batería', 'Precio (USD)'].values[0]
precio_inversor = catalogo.loc[catalogo['Tipo'] == 'Inversor', 'Precio (USD)'].values[0]

costo_total = (n_paneles * precio_panel) + (n_baterias * precio_bateria) + precio_inversor

cotizacion = {
    'Paneles necesarios': n_paneles,
    'Baterías necesarias': n_baterias,
    'Costo total estimado (USD)': costo_total
}

print("Recomendación y cotización:")
for k, v in cotizacion.items():
    print(f"{k}: {v}")