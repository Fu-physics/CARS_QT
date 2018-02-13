
# Setup our imports
import sys
import time
import numpy as np
import scipy
import scipy.signal
import matplotlib.pyplot as plt

from openpyxl import Workbook
from openpyxl import load_workbook
import als_methods as als
import pre as crikit

class CARS():
    def __init__(self):
        pass

    def nm2wavenumber(self, pump, antistokes):
        return 10**7*(1/np.array(antistokes) - 1/pump)
        
    def area(self, x):
        return np.sum(x)
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
    
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


    def loadData(self, fileName):
        ##  --------------------------------------               Import the xlsx file
        W = load_workbook(fileName)
        p = W.get_sheet_by_name(name = 'Sheet1')

        a=[]
        for row in p.iter_rows():
            for k in row:
                a.append(k.internal_value)

        dataNumer = 0
        for i in a:
            if  (not self.is_number(i)):
                dataNumer  = dataNumer + 1
            elif self.is_number(i):
                break
        print("dataNumer is: ", dataNumer)

        data = np.resize(a, [int(len(a)/dataNumer), dataNumer])
        del a
        dataNameList = data[0,:]
        print("The dictionary name list is:\n", dataNameList)

        ##   -------------------------           reshape the data to dictionary, and normalized the data which makes the area of each plot to unit 1;
        dic ={}
        for i in range(dataNumer):
            dic[dataNameList[i]] = data[1:,i].astype(np.float)

        dic_norm = {}  ## nornalized data dictionary, not included the 0 index which is the wavelength
        for i in dataNameList[1:]:
            #print(i)
            dic_norm[i] = dic[i]/self.area(dic[i])

        dic_norm["wavenumber"] = self.nm2wavenumber(1064, dic[dataNameList[0]])
        dic_norm[dataNameList[0]] = dic[dataNameList[0]]

        dic["wavenumber"] = dic_norm["wavenumber"]

        return  dic, dic_norm

    def plotPredata(self, Predata, preFigure):

        fig = preFigure

        WN = Predata["wavenumber"]
        averageIntensity =  0.0 * Predata["wavenumber"]
        
        plt.subplot(111)     ## plot background 
        
        numberOfData = 0; 
        for key, value in Predata.items():
            if (key != "wavenumber" and key != "wavelength") :
                print(key)
                print(Predata[key])
                averageIntensity += value
                numberOfData += 1
                plt.plot(WN, value, label = key)
                plt.legend()
                
        ## The average of background_list, which will be used as the background data.
        averageIntensity = averageIntensity / numberOfData     
        
        plt.plot(WN, averageIntensity, label = 'averageIntensity')

        plt.legend()
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        plt.ylabel('Spectrum (au)')
        plt.show()
    
class KK_ALS_Spectral():
    
    def __init__(self):
        self.I_CARS = dic_norm[matter]/dic_norm["background"]
        self.I_NRB = np.zeros(len(dic_norm[matter])) +1
        self.I_REF = np.zeros(len(dic_norm[matter])) +1(self, parameter_list):
                





if __name__ == '__main__':
    app = CARS()
    dicBackground, dicBackgroundNorm = app.loadData('spectra_background.xlsx')
    dicSignal, dicSignalNorm = app.loadData('spectra_signal.xlsx')

    fig = plt.figure(figsize=[12, 6])

    app.plotPredata(dicSignalNorm, fig)
    #app.plotPredata(dicBackgroundNorm, fig)
    #print("dic is:", dic)
    #print("dic_normal is:", dic_norm)
    print("the last step!")