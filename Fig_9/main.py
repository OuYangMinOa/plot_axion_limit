import pandas as pd
import os
import matplotlib
import time
import nptdms
import re

from urllib.request    import urlretrieve
from tqdm.auto         import tqdm
from datetime          import datetime, timedelta
from ou_Axion_limit    import analyse, Glimit
from matplotlib.pyplot import *
from glob              import glob
from numpy             import *
from scipy.signal      import savgol_filter
from scipy             import interpolate
import mplhep as hep
hep.style.use(hep.style.ROOT)

ALL_DATAS_FREQ = []
ALL_DATAS_SPEC = []
ALL_DATAS_NA   = []
ALL_DATAS_Q    = []
ALL_DATAS_beta = []
ALL_DATAS_MEAN = []
ALL_DATAS_DATE = []
ALL_DATAS_G    = []
RESONANCE_FREQ_ARR = []
fix_gain   = 0
do_Sg      = 2

#  71  > 377 
#  101 > 377
#  201 > 377
#  501 > 100 
#  251 > 100

# 3 189
# 4 241
# 4 201


order  = 4
window = 201
raw_floders  = os.listdir(f"raw/")
if (fix_gain):
    print("Using fitted gain")
    
if ("cavity 0" in raw_floders):
    raw_floders.remove("cavity 0")

for index in range(1):

    cavity_num = index+1
#     print(cavity_num,end=" ")
    saved_file = f"server_processed_data/server_window{window}_order{order}_do_sg_{do_Sg}/cavity_{cavity_num}.npy"

    temp_freq, temp_spec, temp_av, temp_mean,temp_date, G_arr, this_Q, this_beta, fr = load(
            saved_file,
            allow_pickle=True)
    ALL_DATAS_FREQ.append(temp_freq)
    ALL_DATAS_SPEC.append(temp_spec)
    ALL_DATAS_NA.append(  temp_av  )
    ALL_DATAS_MEAN.append(temp_mean)
    ALL_DATAS_DATE.append(temp_date)
    ALL_DATAS_G.append(G_arr)
    ALL_DATAS_Q.append([this_Q,])
    ALL_DATAS_beta.append(this_beta)
    RESONANCE_FREQ_ARR.append(fr)


ALL_DATAS_FREQ = array(ALL_DATAS_FREQ)
ALL_DATAS_SPEC = array(ALL_DATAS_SPEC)
ALL_DATAS_NA   = array(ALL_DATAS_NA)
ALL_DATAS_Q    = array(ALL_DATAS_Q) # 
ALL_DATAS_beta    = array(ALL_DATAS_beta) # 
RESONANCE_FREQ_ARR = array(RESONANCE_FREQ_ARR)


# font = {'size'   : 14,'figsize':(8,6)}
matplotlib.rcParams.update({'font.size': 15,'figure.figsize':(8,6)})

this_spec = ALL_DATAS_SPEC[0]
this_an = analyse(this_spec * 1e20)
figure()
hist(this_spec * 1e20,100,density=True)
legend(["fitted Gaussion",f"Total Entries {len(this_spec)}"])
title(r'$\mathrm{Histogram\ of\ step 1:}\ \mu=(%.1e\pm%.1e),\ \sigma=(%.1e\pm%.1e)$' %(
            this_an.mu,
            this_an.mu_error,
            this_an.sigma,
            this_an.sigma_error),size=15)
xlabel(r"power [$10^{-20}$w]")
ylabel("count",size=18)
tight_layout()
savefig("FIG_9.png")
show()