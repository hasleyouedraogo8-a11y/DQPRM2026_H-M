import pandas as pd
import numpy as np

# Chargement des données
df = pd.read_csv('./data/Table.csv', delimiter='\t', index_col=0)

# Calcul de la masse
rho_g_per_cm3 = 1.03
df['Masse [g]'] = df['Volume [cm3]'] * rho_g_per_cm3

# Extraction de la masse pour le lobe droit
m_foie_lobe_d = df.loc['lobe_droit', 'Masse [g]']

# Calcul de l'activité
delta_Mev_per_Bq_s = 0.9336
T_y90_s = 64.065 * 3600
dose_foie_limite_Gy = 120

act_1 = (dose_foie_limite_Gy * np.log(2) * (m_foie_lobe_d) / 1000) / (T_y90_s * delta_Mev_per_Bq_s * 1e9 * 1.6e-13)
print(f"L'activité à injecter est de {act_1:.2f} GBq pour atteindre {dose_foie_limite_Gy} Gy au lobe droit.")

# Rapport des concentrations
ratio_tum_lobe = df.loc['tum_dome_SPECT', 'Moyenne'] / df.loc['lobe_droit', 'Moyenne']
print(f"Le rapport des concentrations est estimé à {ratio_tum_lobe:.2f}")

# Calcul des activités dans le foie et la tumeur
m_tum = df.loc['tum_dome_CT', 'Masse [g]']
A_n = act_1 / (1 + ratio_tum_lobe * (m_tum / m_foie_lobe_d))
A_t = ratio_tum_lobe * A_n * (m_tum / m_foie_lobe_d)

print(f"Les activités dans le foie perfusé et la tumeur sont {A_n*1000:.2f} et {A_t*1000:.2f} MBq respectivement.")

# Calcul de la dose à la tumeur
dose_t = (A_t * T_y90_s * delta_Mev_per_Bq_s * 1e9 * 1.6e-13) / np.log(2) * (m_tum)
print(f"La dose à la tumeur est {dose_t:.2f} Gy")