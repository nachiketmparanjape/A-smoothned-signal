import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
    """ Plots IV Curve for the sensor data in the dataframe. Stores images in a separate subfolder (foldername)"""
        
    try:
        dataframe['Resistance'] = dataframe['Voltage']/dataframe['Current']
        dataframe.plot(x='Voltage',y='Current',legend=False)
        plt.xlabel('Voltage')
        plt.ylabel('Current')
        plt.title(str(i)+ ") Mean Resistance = " + str(round(dataframe['Resistance'].mean()*0.001,4)) + " kOhm")
        plt.savefig(foldername + '/' + foldername +"_Sensor_"+str(i)+".jpeg",orientation='portrait',papertype='letter')
        plt.close()
    except TypeError:
        pass
    

def Resistances(df):
    """ Calculates R1 (Ohmic) and R2 (Shocky Barrier) for every IV data. Returns R1, R2.
    Also, populates the input lists for compilation purposes"""
    
    #Ohmic Region
    try:
        V1high = float(df[df['Voltage'] > 0.84][df['Voltage'] < 0.86]['Voltage'])
    except TypeError:
        V1high = np.nan
        
    try:
        V1low = float(df[df['Voltage'] > 0.74][df['Voltage'] < 0.76]['Voltage'])
    except TypeError:
        V1low = np.nan
        
    try:    
        I1high = float(df[df['Voltage'] > 0.84][df['Voltage'] < 0.86]['Current'])
    except TypeError:
        I1high = np.nan
        
    try:
        I1low = float(df[df['Voltage'] > 0.74][df['Voltage'] < 0.76]['Current'])
    except TypeError:
        I1low = np.nan
        
    R1 = (V1high - V1low) * 0.001 / (I1high - I1low)
    
    #Shocky Region
    try:
        V2high = float(df[df['Voltage'] > 0.24][df['Voltage'] < 0.26]['Voltage'])
    except TypeError:
        V2high = np.nan
    
    try:
        V2low = float(df[df['Voltage'] > 0.05][df['Voltage'] < 0.07]['Voltage'])
    except TypeError:
        V2low = np.nan
    
    try:
        I2high = float(df[df['Voltage'] > 0.24][df['Voltage'] < 0.26]['Current'])
    except TypeError:
        I2high = np.nan
        
    try:
        I2low = float(df[df['Voltage'] > 0.05][df['Voltage'] < 0.07]['Current'])
    except TypeError:
        I2low = np.nan
    
    R2 = (V2high - V2low) * 0.001 / (I2high - I2low)
    
    return R1, R2
    

def file_list(file_search='*.lvm'):
    """ Searches for files of specific types or names and compiles their names in a list.
    
    file_search requires a phrase (string). Default = '*.lvm'"""
    l = glob.glob(str(file_search))
    return l

    
def main_IV():
    
    """This plots the IV data for a list of files. Takes string input from user as a search term"""
    
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
    
    """Searches for files in a folder for a specific phrase (default = '*.lvm') and enlists resistances"""
    
    R1list = []
    R2list = []
    #file_search = raw_input("Please input a string for filename criteria - ")
    files = file_list(file_search)
    for fil in files:
        l = datareader(fil)
        
        for df in l:
            R1, R2 = Resistances(df)
            R1list.append(R1)
            R2list.append(R2)
        
    return R1list,R2list
    
def R_df(file_search = '*.lvm'):
    
    Rdf = pd.DataFrame(columns = ['Sensor','ROhmic','RShocky'])
    R1list = []
    R2list = []
    sensorlist = []
    files = file_list(file_search)
    j = 1
    for fil in files:
        l = datareader(fil)
        i = 1
        print ("\n\n............Processing file " + str(j) + "............")
        j += 1
        
        for df in l:
            print ("\n............ Calculating Resistances for Dataset " + str(i) + "............")
            R1, R2 = Resistances(df)
            R1list.append(R1)
            R2list.append(R2)
            i += 1
            sensor = str(fil) + "_" + str(i)
            sensorlist.append(sensor)
            
            
    Rdf['Sensor'] = sensorlist
    Rdf['ROhmic'] = R1list
    Rdf['RShocky'] = R2list

    return Rdf
            
def yield_printer(List,lowerlimit = 10,higherlimit = 30):
    select = []
    for i in List:
        if i >= lowerlimit and i <= higherlimit:
            select.append(i)
    try: #to handle zerodivision error
        print ("\nLower Limit = " + str(lowerlimit) + " kOhm\tHigher Limit = " + str(higherlimit) + " kOhm")
        print ("Overall Yield =\t" + str(round(float(len(select))*100/len(List),4)) + " %\t(" + str(len(select)) + "/" + str(len(List)) + ")")
    except ZeroDivisionError:
        pass
    
def write_to_excel(df):
    name = raw_input("Enter the name for the file - ")
    writer = pd.ExcelWriter(name)
    df.to_excel(writer,'Sheet1')
    writer.save()
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

    

    
