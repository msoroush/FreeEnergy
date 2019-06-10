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

numFile = 22 
compounds = ["C8OH", "H7F1", "H6F2", "H2F6", "H1F7", "F17O"]
fname = "Free_Energy_BOX_0_PRODUCTION_"
ext = ".dat"
NREP = 1
print("Correlated Data")
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
            files.append(file_path)
            
        #for TI estimator
        list_data = []
        for f in files:
            dHdl = extract_dHdl(f, T=temprature)
            list_data.append(dHdl)

        dHdl = pd.concat([ld for ld in list_data])
        ti = TI().fit(dHdl)
        sum_ti = ti.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        sum_ds_ti = ti.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        tis.append(sum_ti)


        #for MBAR estimator
        list_data = []
        for f in files:
            u_nkr = extract_u_nk(f, T=temprature)
            list_data.append(u_nkr)

        u_nk = pd.concat([ld for ld in list_data])
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
    print(" ")
    #print("Average  , %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f\n" % (com, np.average(tis), np.std(tis), np.average(mbars), np.std(mbars), np.average(bars), np.std(bars)))


print("Uncorrelated Data")
print("#Compound  TI-est(kcal/mol)  stdev  MBAR-est(kcal/mol)  stdev  BAR(kcal/mol)")
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
            files.append(file_path)

        list_data_TI = []
        list_data_BAR = []
        for f in files:
            dHdl = extract_dHdl(f, T=temprature)
            u_nkr = extract_u_nk(f, T=temprature)
            srs = dHdl['VDW'] + dHdl['Coulomb'] 
            list_data_TI.append(ss.statistical_inefficiency(dHdl, series=srs))
            list_data_BAR.append(ss.statistical_inefficiency(u_nkr, series=srs))


        #for TI estimator
        dhdl = pd.concat([ld for ld in list_data_TI])
        ti = TI().fit(dhdl)
        sum_ti = ti.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        sum_ds_ti = ti.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
        tis.append(sum_ti)


        #for MBAR estimator
        u_nk = pd.concat([ld for ld in list_data_BAR])
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
    print(" ")
    #print("Average  , %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f\n" % (com, np.average(tis), np.std(tis), np.average(mbars), np.std(mbars), np.average(bars), np.std(bars)))        
