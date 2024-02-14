import numpy as np
import pandas as pd


def compute_total_asset(data, name):
    # Ceci est un placeholder, remplacez-le par votre logique de calcul
    total_assets = np.sum(data.loc[data['Name']==name, 'Position totale'])
    return round(total_assets)