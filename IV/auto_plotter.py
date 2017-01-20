# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 10:19:39 2016

@author: Nachiket Madhav Paranjape

This code plots for all the files present in a particular folder

"""

import os
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import glob
from bokeh.plotting import figure, output_file, save

def data_loader(filename):
    """ Used to load the csv files into an appropriate dataframe"""
    #Importing data
    df = pd.read_csv(filename)
    print "\nData Loaded.\n"
    print ".......Starting the process.......\n"
    print "=================================================================================="
    #Subsetting the dataframe
    df = df[['Time (ms)','Channel','Sensor Resistance (kOhms)']]
    df['Time (ms)'] = pd.to_numeric(df['Time (ms)'], errors = coerce)
    df['Time (s)'] = df['Time (ms)']/1000
    df.drop('Time (ms)', axis=1, inplace=True)
    df = df[:-8]
    #Creating the pivot table and eliminating the unnecessary columns
    pivoted = df.pivot('Time (s)','Channel','Sensor Resistance (kOhms)')
    return pivoted

def plotter(dataframe,filename):
    """ This is a plotting function. Crates a figure with two plots. Inputs - dataframe to be plotted and filename for the plots generated"""
    #Create a folder to save the files separetely
    folder_name = filename + "_Plots"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    print "\nSmoothing and Plotting"
    for i in range(10):
        print "\n Channel "+ str(i+1)
        df_temp = dataframe[i]
        #Exponential Moving Average
        df_temp['EMV'] = df_temp.ewm(span=100,min_periods=0,adjust=True).mean()
        #print "Smoothened"
        
        #Figures!
        #Fig 1 - initialization
        #plot = plt.figure()
        #plt.plot()
        plot = df_temp.plot(figsize=(25,10))
        fig = plot.get_figure()
        #print "Plotted"
        
        #Saving the plots in a subfolder
        
        fig.savefig(folder_name +'/'+ filename +"_Channel_"+str(i)+".tif",orientation='portrait',papertype='letter')
    print
    print "Plotting Successfull!"
    print 
    print "=================================================================================="
    return df_temp
    
def bokeh_plotter(dataframe,filename):
    """ This is a dynamic plotting function. Crates html with two plots. Inputs - dataframe to be plotted and filename for the plots generated"""
    #Create a folder to save the files separetely
    folder_name = filename + "_Plots"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    print "\nSmoothing and Plotting"
    for i in range(10):
        print "\n Channel "+ str(i+1)
        df_temp = dataframe[[i]].dropna()
        #Exponential Moving Average
        y1 = df_temp.ewm(span=100,min_periods=0,adjust=True).mean()
        #print "Smoothened"
        x = list(df_temp.index)
        y2 = df_temp[i]

        
        #Create a new plot with title and axis labels
        p = figure(title= "Channel "+str(i), x_axis_label ='Time (s)', y_axis_label = 'Resistance (kiloohms)')
        
        # add a line renderer with legend and line thickness
        p.scatter(x, y2, legend="Temp.",line_width=0.5,line_color='yellow')
        p.line(x, y1, legend="Temp.", line_width=1,line_color='blue')
        
        #Output to static html file
        output_file(folder_name +'/'+ filename +"_Channel_"+str(i)+".html")
        save(p)

    print "Plotting Successfull!"
    print 
    print "=================================================================================="
    

def main():
    print "Now processing all the csv files in the present folder\n\n"
    print "=================================================================================="
    
    for files in glob.glob("*.csv"):
        df = data_loader(files)
        bokeh_plotter(df,files)
        
main()
        

