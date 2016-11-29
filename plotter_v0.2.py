# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:46:27 2016

@author: Nachiket
"""

#This file will use pandas module to collect data from a DPT file and then it will plot it using matplotlib

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

    
def data_loader(filename):
    """ Used to load the csv files into an appropriate dataframe"""
    #Importing data
    df = pd.read_csv(filename + '.csv')
    #Subsetting the dataframe
    df = df.ix[:162029][['Time (ms)','Channel','Sensor Resistance (kOhms)']]
    df['Time (ms)'] = pd.to_numeric(df['Time (ms)'], errors = coerce)
    df['Time (s)'] = df['Time (ms)']/1000
    df.drop('Time (ms)', axis=1, inplace=True)
    #Creating the pivot table and eliminating the unnecessary columns
    pivoted = df.pivot('Time (s)','Channel','Sensor Resistance (kOhms)')[[0,1,2,3,4,5,6,7,8,9]]
    return pivoted

def plotter(dataframe,filename):
    """ This is a plotting function. Crates a figure with two plots. Inputs - dataframe to be plotted and filename for the plots generated"""
    #Create a folder to save the files separetely
    folder_name = filename + "_Plots"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    
    for i in range(10):
        df_temp = dataframe[[i]].dropna()
        #Exponential Moving Average
        df_temp['EMV'] = df_temp.ewm(span=100,min_periods=0,adjust=True).mean()
        
        #Figures!
        #Fig 1 - initialization
        fig = plt.figure()
        #plt.plot()
        plot = df_temp.plot(figsize=(25,10))
        fig = plot.get_figure()
        
        #Saving the plots in a subfolder
        
        fig.savefig(folder_name +'/'+ filename +"_Channel_"+str(i)+".tif",orientation='portrait',papertype='letter')
        
    print "success"
    return df_temp
    

def filename_input():
    flag = True
    print " ### Welcome to the FTIR plotting tool (from DPT files) ###"
    while flag:
        try:
            name1 = raw_input("File"+" - Please enter the name of the data file you want to plot!!!")
            df = data_loader(name1)
            plotter(df,name1)
            flag = False
        except IOError:
            print "Looks like last file name was incorrect. Going back.\n"
            flag = False
          

def main():
    print "Welcome to the dataplotter!\n"
    
    
    choice = 0
    while choice<1 or choice>2:
        faith = True
        while faith:
            try:
                print "Options - \n1.Plot!\n2.Exit"
                choice = (int(raw_input("Choose an option - ")))
                faith = False
            except ValueError:
                faith = True
                print "Please enter a valid numerical option"
        
        if int(choice) == 1:
            filename_input()
            global option
            print "Going back to the main menu"
            choice = 0
    
        elif int(choice) == 2:
            break
            global option
            print "Going back to the main menu"
            
        else:
            print "Please enter a valid choice"
            
main()



        