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

def create(path):
    if (os.path.isdir(path)):
        return True
    try:
        print(f"      - creating '{path}' success")
        os.makedirs(path)
    except Exception as e:
        print(e)
        return False

ALL_DATAS_FREQ = []
ALL_DATAS_SPEC = []
ALL_DATAS_NA   = []
ALL_DATAS_Q    = []
ALL_DATAS_beta = []
ALL_DATAS_MEAN = []
ALL_DATAS_DATE = []
ALL_DATAS_G    = []
RESONANCE_FREQ_ARR = []
use_f_gain = 1
do_Sg      = 0

order  = 4
window = 201
raw_floders  = os.listdir(f"faxion_1120_raw/")

if ("cavity 0" in raw_floders):
    raw_floders.remove("cavity 0")

for index in range(len(raw_floders)):
    cavity_num = index+1
    print(cavity_num,end=" ")
    saved_file = f"server_processed_faxion_1120/server_window{window}_order{order}_do_sg_{do_Sg}/cavity_{cavity_num}.npy"
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

sort_index = argsort(ALL_DATAS_FREQ[:,800])[::-1]

RESONANCE_FREQ_ARR = RESONANCE_FREQ_ARR[sort_index]
ALL_DATAS_FREQ     = ALL_DATAS_FREQ[sort_index]
ALL_DATAS_SPEC     = ALL_DATAS_SPEC[sort_index]
ALL_DATAS_NA       = ALL_DATAS_NA[sort_index]
ALL_DATAS_Q        = ALL_DATAS_Q[sort_index]
ALL_DATAS_beta     = ALL_DATAS_beta[sort_index]



ALL_DATAS_FREQ     = array(ALL_DATAS_FREQ)
ALL_DATAS_SPEC     = array(ALL_DATAS_SPEC)
ALL_DATAS_NA       = array(ALL_DATAS_NA)
ALL_DATAS_Q        = array(ALL_DATAS_Q) # 
ALL_DATAS_beta     = array(ALL_DATAS_beta) # 
RESONANCE_FREQ_ARR = array(RESONANCE_FREQ_ARR)


matplotlib.rcParams.update({'font.size': 18})
fig = figure(figsize=(8,6))
ax = fig.add_subplot()
title("spectrum in each step")
for spec_num in range(ALL_DATAS_FREQ.shape[0]):
    this_spec_for_stack =  ALL_DATAS_SPEC[spec_num] - mean( ALL_DATAS_SPEC[spec_num])
    ax.plot(1e-9 * ALL_DATAS_FREQ[spec_num],this_spec_for_stack - spec_num*6.2e-22,"-",
            label= f"step = {spec_num+1}" )#if (abs(spec_num-ALL_DATAS_FREQ.shape[0]) <10) else None)

legend(ncol=2,fontsize=9,loc="upper left")
ax.get_yaxis().set_visible(False)
grid()
xlabel("Frequency [GHz]")
tight_layout()
savefig("FIG_5.png")
show()





















