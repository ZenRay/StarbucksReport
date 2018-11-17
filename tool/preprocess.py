#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from addiction import view_progress

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

def parse_time_value(data, target_column, option="offer_id"):
    """Parse the time interval and transaction time

    Get the the transaction time interval, since the user finish the last 
    transaction time.

    Parameters:
    -----------
    data: DataFrame
        Original data
    target_column: string
        The label string. If it exists, update the column value; otherwise, 
        create the target_column
    option: string default offer_id
        It is additional option to group. It is used, when offer_id is validate
        value; otherwise, it is deprecated, when offer_id is missing value
    
    Results:
    ----------
    result: DataFrame or Series
        Store the information from parse the time
    columns: list labels
        Store the new labels
    """
    if target_column not in data:
        result = pd.DataFrame(index=data.index)
        result[target_column] = np.nan
    else:
        result = data[[target_column]]

    person_with_offer = data.groupby(["person", option])["time"]
    person_without_offer = \
        data.loc[data[option].isnull()].groupby(["person"])["time"]
    
    # parse the time information about the validate offer_id value
    person_offer_items = person_with_offer.apply(
        lambda x: np.diff(sorted(x))
    ).reset_index()
    person_offer_groups = person_with_offer.groups

    result["time_interval"] = view_progress(
        person_offer_items, person_offer_groups, person_offer_items.shape[0],
        result["time_interval"]
    )
    
    # parse the time information about the invalidate offer_id value
    person_without_offer_items = person_without_offer.apply(
        lambda x: np.diff(sorted(x))
    ).reset_index()
    person_without_offer_groups = person_without_offer.groups

    result["time_interval"] = view_progress(
        person_without_offer_items, person_without_offer_groups,
        person_without_offer_items.shape[0], result["time_interval"]
    )

    # get the labels
    columns = result.columns

    return result, columns

def group_size(data, by, label="count", **kwargs):
    """Caculate the size and transform
    
    Caculate the data groups size and transform as DataFrame

    Parameters:
    -----------
    data: DataFrame
        Original data
    by: label or list of labels
        Used to determine the groups for tht groupby.
    label: label
        Used to rename the new DataFrame label
    
    Returns:
    ---------
    result: DataFrame
        Store the data that is transformed the groups data into DataFrame
    """
    group_data = data.groupby(by=by, **kwargs).size()

    result = group_data.reset_index()

    result.rename({0: label}, inplace=True, axis=1)

    return result