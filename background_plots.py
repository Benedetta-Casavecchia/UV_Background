import os, os.path
import math
import numpy as np
from vtk import vtkStructuredPointsReader
from vtk.util import numpy_support as VN
import vtk
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.colors import LogNorm

def read_file(file_name, first_line, condition_columns, column_wavelegth, column_lum):
    f = open(file_name,"r")
    lines = f.readlines()
    #print(lines[0])
    #print(len(lines))

    wavelength = []
    luminosity = []
    i = 0
    for x in lines:
        if i >= first_line:
            try:
                wavelength.append(float(x.split(condition_columns)[column_wavelegth]))
                luminosity.append(float(x.split(condition_columns)[column_lum]))
                #print(wavelength)
                #print(i)
            except ValueError as ve: #this condition is for the .out file, vecause there are parenthesis e.g. (5, 9)
                wavelength.append(float(x.split(condition_columns)[column_wavelegth].replace("(", " ")))
                luminosity.append(float(x.split(condition_columns)[column_lum].replace(")", " ")))
        i += 1
    f.close()
    #print(len(wavelength))
    #print(len(luminosity))
    
    return wavelength, luminosity
    
read_file("S99UV_background.dat", 3, "       ", 0, 4)
read_file("haardt_madau_galaxy.dat", 15, "\t", 0, 1)
read_file("haardt_madau_quasar.dat", 15, "\t", 0, 1)
read_file("z_0.0000e+00.out", 3, " ", 1, 2)

def makeSED():
    
    w_l1, lum1 = np.array(read_file("S99UV_background.dat", 3, "       ", 0, 4))
    w_l2, lum2 = np.array(read_file("haardt_madau_galaxy.dat", 15, "\t", 0, 1))
    w_l3, lum3 = np.array(read_file("haardt_madau_quasar.dat", 15, "\t", 0, 1))
    w_l4, lum4 = np.array(read_file("z_0.0000e+00.out", 3, " ", 1, 2))
    
    #lum1 = (lum1*1e8*500**2)/(2*math.pi*3.086e18*(150**2))**2
    w_l4 = 6.6260755e-27*3e10*1e8/(w_l4*2.179874099e-11)
    #print(w_l4)
    #print(lum2)
    
    plt.figure(figsize = (11,9)) 
    plt.plot(np.log10(w_l1), lum1, label = 'S99_background_4Myr')
    plt.plot(np.log10(w_l2), np.log10(lum2), label = 'H&M_galaxy_Cloudy13')
    plt.plot(np.log10(w_l3), np.log10(lum3), label = 'H&M_quasar_Cloudy13')
    plt.plot(np.log10(w_l4), lum4,label = 'HM12_UVB_cooling_tools')
    plt.xticks(fontsize = 18)
    plt.yticks(fontsize = 18)
    plt.xlabel(r'$\log_{10}(\lambda \ [A])$', fontsize = 18)
    plt.ylabel(r'$\log_{10}(I \ [erg \ cm^{-2} \ s^{-1} \ Hz^{-1} \ sr^{-1}])$', fontsize = 18)
    plt.legend(loc=2, prop={'size': 14})
    
    plt.show()
    
makeSED()
