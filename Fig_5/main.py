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

def expected_axion_power(freq_ ,beta , Q_=15_000 ,B_=8 , T_=3, g_gamma=10):
    output = []
    for each_f in freq_:
        g      = Glimit()
        g.B    = B_
        g.big_A= 77.6e6
        g.Q    = Q_
        g.T    = T_
        g.f    = each_f
        g.beta = beta
        g.calculate()
        output.append(g.shift *  ( g.ma * g.alpha / pi / (g.big_A**2) * g_gamma) **2)
    return array(output) 


df        = pd.read_table("fitted_param_posi.txt",sep=" ",header=None)
f_n , a_n = load(r"First_adding_noise.npy",allow_pickle=True)
freq = df.iloc[:,2].values * 1e9
Q01  = df.iloc[:,3].values
Q2   = df.iloc[:,4].values
DEG  = df.iloc[:,6].values
beta = df.iloc[:,3].values / df.iloc[:,4].values

get_b = lambda x:interpolate.interp1d(RESONANCE_FREQ_ARR, ALL_DATAS_beta, fill_value="extrapolate",assume_sorted = False)(x)
get_Q = lambda x:interpolate.interp1d(freq, Q01 / (1+get_b(x)), fill_value="extrapolate",assume_sorted = False)(x)
get_t = lambda x:interpolate.interp1d(f_n, a_n,fill_value="extrapolate", assume_sorted = False)(x)

dr_hien = pd.read_table("fitted_param_posi_faxion.txt",delimiter=" ",header=None)
RESONANCE_FREQ_ARR = dr_hien.iloc[:,2].values * 1e9
ALL_DATAS_beta = (dr_hien.iloc[:,3] / dr_hien.iloc[:,4]).values
ALL_DATAS_Q   = (1 / (1 / dr_hien.iloc[:,3] + 1/ dr_hien.iloc[:,4])).values.reshape(-1,1)


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

#                 ax.plot(1e-9 * ALL_DATAS_FREQ[spec_num],this_spec_for_stack + spec_num*8e-22)

#     savetxt(f"D:\\AXion\\CD102\\Temp_IQ\\step {spec_num+1}.txt",column_stack([ALL_DATAS_FREQ[spec_num],ALL_DATAS_SPEC[spec_num]]),delimiter=" ", fmt="%s %s")
#     savetxt(f"Y:\Analysis\Spectrum_wo_sg\\step {spec_num+1}.txt",column_stack([ALL_DATAS_FREQ[spec_num],ALL_DATAS_SPEC[spec_num]]),delimiter=" ", fmt="%s %s")
# legend(ncol=3)
legend(ncol=2,fontsize=9,loc="upper left")
ax.get_yaxis().set_visible(False)
grid()
xlabel("Frequency [GHz]")
tight_layout()
show()





















