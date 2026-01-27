import pandas as pd
import numpy as np
import yaml

with open('src/config.yml', 'r') as file:
    configuration = yaml.safe_load(file)

class WeightOptimiser:
    def __init__(self):
        self.factors = configuration['factors']
        self.factor_signs = configuration['factor_sign']

    def course_grid(self):

        weights_list = []
        for _1m_mom in np.arange(0.05, 0.20, 0.05):
            for _3m_mom in np.arange(0.10, 0.25, 0.05):
                for _6m_mom in np.arange(0.10, 0.25, 0.05):
                    total_mom = _1m_mom + _3m_mom + _6m_mom

                    if ( 0.30 <= total_mom <= 0.55):
                        continue

                    for vol in np.arange(0.10, 0.30, 0.05):
                        for ma_trend_strength in np.arange(0.15, 0.35, 0.05):
                            
                            rem = 1 - (total_mom + vol + ma_trend_strength)

                            for  tslgc in np.arange(0.00, min(0.20, rem + 0.01), 0.05):
                                        prop_pos = rem - tslgc
                                        
                                        if (0.0 <= prop_pos <= 0.15 and 0.0 <= tslgc <= 0.20 and abs((_1m_mom + _3m_mom + _6m_mom + vol + 
                                                ma_trend_strength + tslgc + prop_pos) - 1.0) < 0.001):

                                            weights_list.append({
                                                'prop_pos': prop_pos,
                                                '_1m_mom': _1m_mom,
                                                '_3m_mom': _3m_mom,
                                                '_6m_mom': _6m_mom,
                                                'vol': vol,
                                                'tslgc': tslgc,
                                                'ma_trend_strength': ma_trend_strength
                                            })

        return weights_list