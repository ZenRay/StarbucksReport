#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np


def parse_offer_id(x, option=["offer_id", "offer id"]):
    """Parse the offer id value
    The two types are same information in the transript value,
    so we use the another way to parse the information
    
    Parameters:
    -----------
    x: dict
        It is the value store in the transcript value
    option: list
        It is a list that contains the same value
    
    Results:
    ----------
    result:
        If it exists, return the value, otherwise return the nan
    """
    for i in option:
        if i in x:
            result = x[i]
            break
    else:
        result = np.nan
    
    return result