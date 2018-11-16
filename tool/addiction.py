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