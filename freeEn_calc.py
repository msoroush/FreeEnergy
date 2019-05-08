from alchemlyb.parsing.gomc import  extract_dHdl
from alchemlyb.parsing.gomc import  extract_u_nk
from alchemlyb.estimators import MBAR
from alchemlyb.estimators import TI
import pandas as pd
import os

bd = os.path.dirname(os.path.realpath(__file__))

temprature = 298 #temperature (k)
k_b = 8.3144621E-3 #kJ/mol
k_b_T = temprature * k_b

numFile = 27
compounds = ["F3O", "F5O", "F7O", "F9O", "F11O", "F13O", "F15O", "F17O"]
fname = "Free_Energy_BOX_0_PRODUCTION_"
ext = ".dat"

#loop through all compounds
for com in compounds:
    #read the free energy files 
    data_loc = bd + "/" + com +"/TI/state_"
    files = []
    for i in range(numFile + 1):
        freeEn_file = fname + str(i) + ext
        file_path = data_loc + str(i) + "/" + freeEn_file
        print("%4s: Reading File: %s " % (com, freeEn_file))
        files.append(file_path)

    #for TI estimator
    print("Working on TI method ...")
    dHdl = pd.concat([extract_dHdl(f, T=temprature) for f in files])
    ti = TI().fit(dHdl)
    #print(ti.delta_f_ * k_b_T)   #printing free energy difference for all lambda states
    #print(ti.d_delta_f_ * k_b_T) #printing error in free energy difference for all lambda states
    sum = ti.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
    sum_ds = ti.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
    print("Free Energy of %4s from TI: %3.4f +/- %3.4f (kJ/mol) \n" % (com, sum, sum_ds))


    #for MBAR estimator
    print("Working on MBAR method ...")
    u_nk = pd.concat([extract_u_nk(f, T=temprature) for f in files])
    mbar = MBAR().fit(u_nk)
    #print(mbar.delta_f_ * k_b_T)  #printing free energy difference for all lambda states
    #print(mbar.d_delta_f_ * k_b_T)  #printing error in free energy difference for all lambda state
    sum = mbar.delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
    sum_ds = mbar.d_delta_f_.loc[[(0.0, 0.0)], [(1.0, 1.0)]].values[0][0] * k_b_T
    print("Free Energy of %4s from MBAR: %3.4f +/- %3.4f (kJ/mol) \n" % (com, sum, sum_ds))


