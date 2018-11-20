#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from addiction import view_progress, bar_value, self_merge

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

def members_with_time(data, start, end, column, rolling=30, method="mean"):
    """Caculate the member in the specific period
    Create a data to store the member amount in the specific period

    Parameters:
    ------------
    data: DataFrame
        Original data
    start: datetime
        Start date
    end: datetime
        End date
    column: label
        A label about the value caculated
    rolling: int
        The size of moving window
    method: string default mean
        The caculating method is used to caculate the moving statistic. Common 
        methods are mean or sum
    
    Returns:
    -----------
    result: 
        Store the caculate result
    """

    result = pd.DataFrame(columns=[column], 
        index=pd.DatetimeIndex(start=start, end=end, freq="d")
    )
    
    result[column].fillna(data, inplace=True)
    # moving caculation
    if method == "mean":
        result[column] = result[column].rolling(rolling).mean()
    elif method == "sum":
        result[column] = result[column].rolling(rolling).sum()
    

    return result

def merge_data(
    data1, data2, how="left",  portfolio_suffix=None, **kwargs
):
    """Merge the data
    According to whether the data is same, the data is merged by itself, or not.
    The data is the transript data and the portfolio data

    Self merge parameters example:
    merge_data(data1, data1, condition="condition", cond_value1="col_value1",
        cond_value2="col_value2", columns1=["val1", "val2"], on=["col1", "col2"],
        columns2=["val3", "val4", ...], portfolio=portfolio,
        suffixes=("_suff1", "_suff2"), portfolio_suffix=("_info", "_data"),
        **kwargs)
    None self merge parameters:
    merge_data(data1, data2, on="col", portfolio_suffix=("_feat1", "_feat2"))
    
    Not: If need merge the porfolio, pass the key value argument: 
        portfolio=portfolio

    Parameters:
    -----------
    data1, data2: DataFrame
        The original data. If the merge_more is True, merge the other data
    how: {"left", "right", "outer", "inner"} default "left"
        The merge method parameter how
    portfolio_suffix: tuple, suffixes information
        It is suffixes that is used in the portfolio merged

    Results:
    -----------
    result:
        Merged data
    
    Other Parameters:
    -----------------
    kwargs:
        Additional args
    """
    if "portfolio" in kwargs:
        portfolio = kwargs["portfolio"]
        del kwargs["portfolio"]

    if data1 is data2:
        result = self_merge(data1, **kwargs)
        if isinstance(portfolio_suffix, tuple):
            result = result.merge(
                portfolio, how="left", left_on="offer_id", right_on="id",
                suffixes=portfolio_suffix
            )
    else:
        result = pd.merge(data1, data2, how=how, suffixes=portfolio_suffix, **kwargs)
        # data1.merge(data1,  how=how, **kwargs)
    
    # delete the columns with all missing values
    result.dropna(how="all", axis=1, inplace=True)
    return result