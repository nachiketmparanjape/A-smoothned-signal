import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import glob
import os
#import sys
#import platform
#from datetime import datetime

class IV():

    def datareader(self,filename):
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
    
    
    def IV_Curve(self,dataframe,foldername,i):
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
        
    
    def Resistances(self,df):
        """ Calculates R1 (Ohmic) and R2 (Shocky Barrier) for every IV data. Returns R1, R2.
        Also, populates the input lists for compilation purposes"""
        
        #Ohmic Region
        V1high = float(df[df['Voltage'] > 0.94][df['Voltage'] < 0.96]['Voltage'])
        V1low = float(df[df['Voltage'] > 0.74][df['Voltage'] < 0.76]['Voltage'])
        I1high = float(df[df['Voltage'] > 0.94][df['Voltage'] < 0.96]['Current'])
        I1low = float(df[df['Voltage'] > 0.74][df['Voltage'] < 0.76]['Current'])
        R1 = (V1high - V1low) * 0.001 / (I1high - I1low)
        
        #Shocky Region
        V2high = float(df[df['Voltage'] > 0.24][df['Voltage'] < 0.26]['Voltage'])
        V2low = float(df[df['Voltage'] < -0.24][df['Voltage'] > -0.26]['Voltage'])
        I2high = float(df[df['Voltage'] > 0.24][df['Voltage'] < 0.26]['Current'])
        I2low = float(df[df['Voltage'] < -0.24][df['Voltage'] > -0.26]['Current'])
        R2 = (V2high - V2low) * 0.001 / (I2high - I2low)
        
        return R1, R2
        
    
    def file_list(self,file_search='*.lvm'):
        """ Searches for files of specific types or names and compiles their names in a list.
        
        file_search requires a phrase (string). Default = '*.lvm'"""
        l = glob.glob(str(file_search))
        return l
    
        
    def main_IV(self):
        
        """This plots the IV data for a list of files. Takes string input from user as a search term"""
        
        print "\nNow processing all the lvm files in the present folder"
        print "==================================================================================\n"
        
        
        file_search = raw_input("Please input a string for filename criteria - ")
        from IVData import IV
        files = IV.file_list(file_search)
        n = 1 #Printing File no
        for fil in files:
            
            print ("\n...........  File    " + str(n) + ".......\n")
            n += 1 #Increment the counter
            folder_name = fil + "_Plots"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            l = IV.datareader(fil)
            #global R
            #global R_waste
            #R = []
            #R_waste = []
            i = 1
            for df in l:
                IV.IV_Curve(df,folder_name,i)
                print ("Plotting .....   " + str(i)+ "   .....")
                i += 1
                
    
    def R_list(self,file_search='*.lvm'):
        
        """Searches for files in a folder for a specific phrase (default = '*.lvm') and enlists resistances"""
        
        from IVData import IV
        R1list = []
        R2list = []
        #file_search = raw_input("Please input a string for filename criteria - ")
        files = IV.file_list(file_search)
        for fil in files:
            l = IV.datareader(fil)
            
            for df in l:
                R1, R2 = IV.Resistances(df)
                R1list.append(R1)
                R2list.append(R2)
            
        return R1list,R2list
        
    def R_df(self,file_search = '*.lvm'):
        
        Rdf = pd.DataFrame(columns = ['Sensor','ROhmic','RShocky'])
        R1list = []
        R2list = []
        sensorlist = []
        files = IV.file_list(file_search)
        for fil in files:
            l = IV.datareader(fil)
            i = 0
            
            for df in l:
                R1, R2 = IV.Resistances(df)
                R1list.append(R1)
                R2list.append(R2)
                i += 1
                sensor = str(fil) + "_" + str(i)
                sensorlist.append(sensor)
                
        Rdf['Sensor'] = sensorlist
        Rdf['ROhmic'] = R1list
        Rdf['RShocky'] = R2list
    
        return Rdf
                
    def yield_printer(self,List,lowerlimit = 10,higherlimit = 30):
        select = []
        for i in List:
            if i >= lowerlimit and i <= higherlimit:
                select.append(i)
        try: #to handle zerodivision error
            print ("\nLower Limit = " + str(lowerlimit) + " kOhm\tHigher Limit = " + str(higherlimit) + " kOhm")
            print ("Overall Yield =\t" + str(round(float(len(select))*100/len(List),4)) + " %\t(" + str(len(select)) + "/" + str(len(List)) + ")")
        except ZeroDivisionError:
            pass
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
#    
    

    
