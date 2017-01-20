import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

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

def IV_Curve(dataframe):
    dataframe.plot(x='Voltage',y='Current',legend=False)
    plt.xlabel('Voltage')
    plt.ylabel('Current')
    plt.save()

def R_count(df):
    #IV_Curve(dataframe)
    df['Resistance'] = df['Voltage']/df['Current']
    if round(df['Resistance'].mean()*0.001,4) < 5:
        R.append(round(df['Resistance'].mean()*0.001,4))
    else:
        R_waste.append(round(df['Resistance'].mean()*0.001,4))
    #print ("Resistance = " + str(round(dataframe['Resistance'].mean()*0.001,3)) + " kOhm")
    #print R
    #plt.boxplot(R)
    
def main():
    print "Now processing all the csv files in the present folder\n\n"
    print "=================================================================================="
    
    for files in glob.glob("*.lvm"):
        l = datareader(files)
        #global R
        #global R_waste
        #R = []
        #R_waste = []
        for df in l:
            #IV_Curve(df)
            R_count(df)