```python
import numpy as np
from scipy.stats import f_oneway

g1 = [1, 4, 7, 77]
g2 = [1, 4, 7, 77]
g3 = [1, 4, 7, 77]

all_data =  np.array(g1 + g2 + g3)
mean_global = np.mean(all_data)
ss_total = np.sum((all_data - mean_global)**2)

ss_between = (sum(len(g)  * (np.mean(g) - mean_global)**2) for g in [g1, g2, g3])

etat_carre = ss_between / ss_total

```