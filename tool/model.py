#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Purpose:
---------
    The script contains model built functions
"""
from IPython.display import display_html
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import MinMaxScaler, minmax_scale
from sklearn.feature_selection import SelectPercentile, f_regression, mutual_info_regression, SelectFwe
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, make_scorer

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def model_built(
    pipeline, param_grid, X, y, report=False, model_name=None, 
    test_X=None, test_y=None, **kwargs
):
    """Build the model

    Use the pipeline method and the gridsearch to build model

    Parameters:
    ------------
    pipeline: Pipeline object
        The Pipeline object
    param_grid: params dict
        It is GridSearchCV parameter
    X, y: 
        Train data
    report: boolean
        If it true, display the model, result
    model_name: string default None
    test_x, test_y:
        Test data
    """
    cv = GridSearchCV(pipeline, param_grid=param_grid, cv=3, n_jobs=2, **kwargs)

    # train model
    cv.fit(X, y=y)

    if report:
        display_html(
            '<h1>The {0} model result:</h1> \
            <ul style="font:italic 25px Fira San, Serif;"> \
                <li>The mean squared value of the test data is: {1:.4f}</li> \
                <li>The R^2 score of the test data is: {2:.4f}</li> \
                <li>The R^2 score of the train data is: {3:.4f}</li> \
            </ul>'.format(
                model_name, mean_squared_error(test_y, cv.predict(test_X)), 
                r2_score(test_y, cv.predict(test_X)),
                r2_score(y, cv.predict(X))
            ), raw=True
        )
    
    return cv

def plot_feature(cv, index, model_index=1, ascending=False):
    """Plot the feature importance

    Plot the model importance

    Parameters:
    -----------
    cv: estimator
        The estimater is trained by tunning the parameters
    index:
        The train data columns
    model_index: int indice 
        Specific the cv model indice
    """
    value = cv.best_estimator_.steps[model_index][1].feature_importances_
    new_index = index[cv.best_estimator_.steps[0][1].get_support()]

    data = pd.DataFrame(value, index=new_index)
    data = data.reset_index().sort_values(0, ascending=False)

    with sns.axes_style("dark"), sns.plotting_context("paper", font_scale=1.5):
        plt.figure(figsize=(7, 7))
        ax = plt.subplot()
        sns.barplot(
            y="index", x=0, data= data, orient="h", palette=["#8c8c91"], ax=ax
        )
        plt.xlabel("")
        plt.ylabel("")

    return ax