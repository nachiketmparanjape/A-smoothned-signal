import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import glob
import os

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
            plt.savefig(foldername + '/' + foldername +"_Sensor_"+str(i)+".tif",orientation='portrait',papertype='letter')
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
    
def file_list(file_search):
    l = glob.glob(str(file_search))
    return l
    
def main_IV():
    print "\nNow processing all the lvm files in the present folder"
    print "==================================================================================\n"
    
    
    file_search = raw_input("Please input a string for filename criteria - ")
    files = file_list(file_search)
    for fil in files:
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
            i += 1
            
def main_R():
    R = []
    file_search = raw_input("Please input a string for filename criteria - ")
    files = file_list(file_search)
    for fil in files:
        l = datareader(fil)
        
        for df in l:
            R_count(R,df)
        
    right = []
    for i in R:
        if i > 0 and i < 5:
            right.append(i)
    
    plt.hist(right,bins=100)
    return right