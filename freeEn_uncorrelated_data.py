from alchemlyb.parsing.gomc import  extract_dHdl,  extract_u_nk
from alchemlyb.estimators import MBAR, BAR, TI 
import alchemlyb.preprocessing.subsampling as ss
import pandas as pd
import numpy as np
import os

bd = os.path.dirname(os.path.realpath(__file__))

temprature = 298           #temperature (K)
k_b = 1.9872036E-3         #kcal/mol/K
k_b_T = temprature * k_b

def get_delta(est):
    """ Return the change in free energy and standard deviation for TI and MBAR estimators.
    
    """
    delta = est.delta_f_.iloc[0, -1] * k_b_T
    d_delta = est.d_delta_f_.iloc[0, -1] * k_b_T
    return delta, d_delta


def get_delta2(est):
    """ Return the change in free energy and standard deviation for BAR estimator.
    
    """
    ee = 0.0

    for i in range(len(est.d_delta_f_) - 1):
        ee += est.d_delta_f_.values[i][i+1]**2
    
    delta = est.delta_f_.iloc[0, -1] * k_b_T
    d_delta = k_b_T * ee**0.5
    return delta, d_delta

##################################################

numFile = 22
compounds = ["F3O", "F5O", "F7O", "F9O", "F11O", "F13O", "F15O", "F17O"]
fname = "Free_Energy_BOX_0_PRODUCTION_"
ext = ".dat"
NREP = 5

print("%16s, %16s, %16s, %16s, %16s, %16s, %16s" % ("#Compound","TI(kcal/mol)","stdev","MBAR(kcal/mol)","stdev","BAR(kcal/mol)","stdev"))

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
            print("%4s: Reading File: %s " % (com, freeEn_file))
            files.append(file_path)
                    
        # Read the data for TI estimator and BAR or MBAR estimators.
        list_data_TI = []
        list_data_BAR = []
        for f in files:
            dHdl = extract_dHdl(f, T=temprature)
            u_nkr = extract_u_nk(f, T=temprature)
            #Detect uncorrelated samples using VDW+Coulomb term in derivative 
            # of energy time series (calculated for TI)
            srs = dHdl['VDW'] + dHdl['Coulomb'] 
            list_data_TI.append(ss.statistical_inefficiency(dHdl, series=srs, conservative=False))
            list_data_BAR.append(ss.statistical_inefficiency(u_nkr, series=srs, conservative=False))


        #for TI estimator
        #print("Working on TI method ...")
        dhdl = pd.concat([ld for ld in list_data_TI])
        ti = TI().fit(dhdl)
        sum_ti, sum_ds_ti = get_delta(ti)
        tis.append(sum_ti)


        #for MBAR estimator
        #print("Working on MBAR method ...")
        u_nk = pd.concat([ld for ld in list_data_BAR])
        mbar = MBAR().fit(u_nk)
        sum_mbar, sum_ds_mbar = get_delta(mbar)
        mbars.append(sum_mbar)

        #for BAR estimator
        #print("Working on BAR method ...")
        u_nk = pd.concat([ld for ld in list_data_BAR])
        bar = BAR().fit(u_nk)
        sum_bar, sum_ds_bar = get_delta2(bar)
        bars.append(sum_bar)
    
        print("Replica-%d, %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f" % (nr, com, sum_ti, sum_ds_ti, sum_mbar, sum_ds_mbar, sum_bar, sum_ds_bar))

        
    tis = np.array(tis)
    mbars = np.array(mbars)
    bars = np.array(bars)
    print("Average, %4s,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f,  %7.4f" % (com, np.average(tis), np.std(tis), np.average(mbars), np.std(mbars), np.average(bars), np.std(bars)))        
