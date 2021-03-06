import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import glob
import os
#import sys
#import platform
#from datetime import datetime

def datareader(filename):
    """Data Import and Cleaning
    
    Returns a list of 8 dataframes for further processing"""
    
    df1 = pd.read_csv(filename,sep="\t",skiprows = 22, usecols=[1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    df2 = pd.read_csv(filename,sep='\t',skiprows = 133, usecols = [1,2], names = ['Voltage','Current'],nrows=101, dtype='float')
    df3 = pd.read_csv(filename,sep='\t',skiprows = 244, usecols = [1,2], names = ['Voltage','Current'],nrows=101, dtype='float')
    df4 = pd.read_csv(filename,sep='\t',skiprows = 355, usecols = [1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    df5 = pd.read_csv(filename,sep='\t',skiprows = 466, usecols = [1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    df6 = pd.read_csv(filename,sep='\t',skiprows = 577, usecols = [1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    df7 = pd.read_csv(filename,sep='\t',skiprows = 688, usecols = [1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    df8 = pd.read_csv(filename,sep='\t',skiprows = 799, usecols = [1,2], names = ['Voltage','Current'],nrows=101,dtype='float')
    
    return [df1, df2, df3, df4, df5, df6, df7, df8]

def IV_Curve(dataframe,foldername,i):
        
        try:
            dataframe['Resistance'] = dataframe['Voltage']/dataframe['Current']
            dataframe.plot(x='Voltage',y='Current',legend=False)
            plt.xlabel('Voltage')
            plt.ylabel('Current')
            plt.title(str(i)+ ") Resistance = " + str(round(dataframe['Resistance'].mean()*0.001,4)) + " kOhm")
            plt.savefig(foldername + '/' + foldername +"_Sensor_"+str(i)+".jpeg",orientation='portrait',papertype='letter')
            plt.close()
        except TypeError:
            pass
        
            
def R_count(R,df):
    #IV_Curve(dataframe)
    df['Resistance'] = df['Voltage']/df['Current']
    R.append(round(df['Resistance'].mean()*0.001,4))
#    if round(df['Resistance'].mean()*0.001,4) < 5:
#        R.append(round(df['Resistance'].mean()*0.001,4))
#    else:
#        R_waste.append(round(df['Resistance'].mean()*0.001,4))
    #print ("Resistance = " + str(round(dataframe['Resistance'].mean()*0.001,3)) + " kOhm")
    #print R
    #plt.boxplot(R)
    
def R_count2(R,df):
    #IV_Curve(dataframe)
    df['Resistance'] = df['Voltage']/df['Current']
    R.append(round((df['Resistance'][1]+df['Resistance'][-1])/2*0.001,4))
#    if round(df['Resistance'].mean()*0.001,4) < 5:
#        R.append(round(df['Resistance'].mean()*0.001,4))
#    else:
#        R_waste.append(round(df['Resistance'].mean()*0.001,4))
    #print ("Resistance = " + str(round(dataframe['Resistance'].mean()*0.001,3)) + " kOhm")
    #print R
    #plt.boxplot(R)
    
def file_list(file_search='*.lvm'):
    l = glob.glob(str(file_search))
    return l
    
def main_IV():
    print "\nNow processing all the lvm files in the present folder"
    print "==================================================================================\n"
    
    
    file_search = raw_input("Please input a string for filename criteria - ")
    files = file_list(file_search)
    n = 1 #Printing File no
    for fil in files:
        
        print ("\n...........  File    " + str(n) + ".......\n")
        n += 1 #Increment the counter
        folder_name = fil + "_Plots"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        l = datareader(fil)
        #global R
        #global R_waste
        #R = []
        #R_waste = []
        i = 1
        for df in l:
            IV_Curve(df,folder_name,i)
            print ("Plotting .....   " + str(i)+ "   .....")
            i += 1
            
            
def R_list(file_search='*.lvm'):
    R = []
    #file_search = raw_input("Please input a string for filename criteria - ")
    files = file_list(file_search)
    for fil in files:
        l = datareader(fil)
        
        for df in l:
            R_count(R,df)
        
    right = []
    for i in R:
        if i > 10 and i < 30:
            right.append(i)
            
    #plt.hist(right,bins=100)
    #plt.axis([2.2, 3.6, 0, 5])
    #y = float(len(right))/len(R)
    return right, R
    
def yield_printer():
    """ Prints out overall as well as recipe specific yield """
    
    R, Rtotal = R_list()
    R = float(len(R))
    Rtotal = float(len(Rtotal))
    try: #to handle zerodivision error
        print ("\nOverall Yield -\t" + str(round(R/Rtotal,4)) + "\t(" + str(R) + "/" + str(Rtotal) + ")")
    except ZeroDivisionError:
        pass
    
    R, Rtotal = R_list("10*.lvm")
    R = float(len(R))
    Rtotal = float(len(Rtotal))
    try:
        print ("10s Yield -\t" + str(round(R/Rtotal,4)) + "\t(" + str(R) + "/" + str(Rtotal) + ")")
    except ZeroDivisionError:
        pass
    
    R, Rtotal = R_list("20*.lvm")
    R = float(len(R))
    Rtotal = float(len(Rtotal))
    try:
        print ("20s Yield -\t" + str(round(R/Rtotal,4)) + "\t(" + str(R) + "/" + str(Rtotal) + ")")
    except ZeroDivisionError:
        pass
    
    R, Rtotal = R_list("30*.lvm")
    R = float(len(R))
    Rtotal = float(len(Rtotal))
    try:
        print ("30s Yield -\t" + str(round(R/Rtotal,4)) + "\t(" + str(R) + "/" + str(Rtotal) + ")")
    except ZeroDivisionError:
        pass
#main_R()
            
    



""" This is a template used to print histogram for the resistances with a hue given to the different deposition times"""

#
#import numpy
#bins = numpy.linspace(0, 10, 400)        
#plt.figure(figsize=(8,5))
#plt.hist(right1,bins,alpha=0.5)
#plt.hist(right2,bins,alpha=0.5)
#plt.hist(right3,bins,alpha=0.5)
#plt.legend(["10s","20s","30s"])
#plt.xlabel("Resistance - kOhm")
#plt.axis([0, 6,0,3.5])
#plt.show()

""" Plotting one historgram"""

#import numpy
#bins = numpy.linspace(0, 100, 10)        
#plt.figure(figsize=(8,5))
##plt.hist(right1,bins,alpha=0.5)
#plt.hist(right2,bins,alpha=0.5)
#plt.hist(right3,bins,alpha=0.5)
#plt.legend(["20s"])
#plt.xlabel("Resistance - kOhm")
#plt.axis([0, 6,0,3.5])
#plt.show()
