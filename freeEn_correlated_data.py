from alchemlyb.parsing.gomc import  extract_dHdl
from alchemlyb.parsing.gomc import  extract_u_nk
import alchemlyb.preprocessing.subsampling as ss
from alchemlyb.estimators import MBAR, BAR
from alchemlyb.estimators import TI
import pandas as pd
import numpy as np
import os

bd = os.path.dirname(os.path.realpath(__file__))

temprature = 298 #temperature (K)
k_b = 1.9872036E-3 #kcal/mol/K
k_b_T = temprature * k_b

numFile = 27
compounds = ["F3O", "F5O", "F7O", "F9O", "F11O", "F13O", "F15O", "F17O"]
fname = "Free_Energy_BOX_0_PRODUCTION_"
ext = ".dat"
NREP = 5
print("#Compound  TI-est(kcal/mol)  stdev  MBAR-est(kcal/mol)  stdev  BAR-est(kcal/mol) ")

#loop through all compounds
for com in compounds:
    tis = []
    mbars = []
    bars = []
    for nr in range(NREP):
        #read the free energy files 
        data_loc = bd + "/" + com +"/TI_"+str(nr+1)+"/state_"
        files = []
        for i in range(numFile + 1):
            freeEn_file = fname + str(i) + ext
            file_path = data_loc + str(i) + "/" + freeEn_file
            #print("%4s: Reading File: %s " % (com, file_path))
            files.append(file_path)
            
        #for TI estimator
        #print("Working on TI method ...")]
        dHdl = pd.concat([extract_dHdl(f, T=temprature) for f in files])
        ti = TI().fit(dHdl)
        sum_ti = ti.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        sum_ds_ti = ti.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        tis.append(sum_ti)


        #for MBAR estimator
        #print("Working on MBAR method ...")
        u_nk = pd.concat([extract_u_nk(f, T=temprature) for f in files])
        mbar = MBAR().fit(u_nk)
        sum_mbar = mbar.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        sum_ds_mbar = mbar.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        mbars.append(sum_mbar)
        
        
        bar = BAR().fit(u_nk)
        sum_bar = bar.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        bars.append(sum_bar)
    
        print("Replica-%d, %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f" % (nr, com, sum_ti, sum_ds_ti, sum_mbar, sum_ds_mbar, sum_bar))

        
    tis = np.array(tis)
    mbars = np.array(mbars)
    bars = np.array(bars)
    print("Average, %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f" % (com, np.average(tis), np.std(tis), np.average(mbars), np.std(mbars), np.average(bars), np.std(bars)))
