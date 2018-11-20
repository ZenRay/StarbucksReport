#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Purpose:
---------
    The module contains additional functions that deal with the specific function
"""
import numpy as np
import pandas as pd
from progressbar import Bar, ProgressBar, Timer, ETA, FileTransferSpeed, Percentage
import matplotlib.pyplot as plt
import matplotlib as mtl

def view_progress(iterdata, dictdata, length, target):
    """Show the progress percentage

    Show the progress about the data dealing

    Parameters:
    ------------
    iterdata: DataFrame or Series
        The data is used with the iterrows method, so that loop  the value.
    dictdata: dict
        The data is store the information in the key, and the values is the 
        original data index
    length: int
        It is same as the iterdata rows
    target: Series
        Update the result into the target
    
    Results:
    -----------
    target: Series
        Return the result updated
    """
    # create the progress bar
    widgets = [
        "Pregress:", Percentage(), " ", Bar("█"), " ", Timer(), " ", ETA(), " ",
        FileTransferSpeed()
    ]

    bar = ProgressBar(widgets=widgets, maxval=length).start()

    for row in iterdata.iterrows():
        bar.update(row[0] + 1)
        
        try:
            # assign the first on interval time with 0
            time_interval = [0]
            time_interval.extend(row[1]["time"])

            # maybe there is no offer_id
            current_index = (row[1]["person"], row[1]["offer_id"])
        except KeyError:
            current_index = row[1]["person"]

        
        # update the target value
        target.loc[dictdata[current_index]] = time_interval
        # for index, value in zip(dictdata[current_index], time_interval):
        #     target.loc[index] = value
    bar.finish()


    return target

def bar_value(data, xpad, ypad, **fontdict):
    """Plot the bar value

    Add the text about the bar plot

    Parametes:
    -----------
    data: default Series
        Original data to plot the text
    xpad ypad: float
        The offset of the text from the bar top
    
    Other Parameters:
    ----------
    **fontdict: Text properties
        It is fontdict property
    """
    for index, value in enumerate(data):
        plt.text(x=index+xpad, y=value+ypad, s="%s" % value, **fontdict)

def self_merge(
    data, condition, cond_value1, cond_value2, columns1, columns2, how="left",
    **kwargs,
):
    """The DataFrame Merged with itself
    
    Merge the DataFrame itself with different condition, besides need specific 
    the columns that the values are needed

    Parameters:
    -----------
    data: DataFrame
        Original values
    condition: column label
        The specific column label is used to filter the data
    cond_value1, cond_value2: string
        It is the condition column value
    columns1, columns2: column labels
        The specific column labels are used to get the values

    Results:
    ----------
    result: 
        The data merged

    Other Parameters:
    -----------------
    kwargs: additional parametes
        They are the merge method parameters
    """
    data1 = data.loc[data[condition] == cond_value1, columns1]
    data2 = data.loc[data[condition] == cond_value2, columns2]

    result = pd.merge(data1, data2, how=how, **kwargs)

    return result

def info_filter(x, filter1="time_received", filter2="time_viewed"):
    """Check the validate x
    The function is used to the apply method, the value x is a iterable object 
    that is the axis x value. The condition is that the total time between the 
    received time and the duration time is equal or less than the current 
    transaction time

    Note:
    --------------
    It is used to filter the informational type value

    Kernel example:
    ---------------
    df.apply(lambda x: x['col1'] > x['col2'], axis=1)

    Example:
    --------------
    df.apply(info_filter, axis=1)
    """

    if pd.notnull(x[filter1]) and (x[filter2] + x["duration"] <= x["time"]):
        result = True
    else:
        result = False
    
    return result