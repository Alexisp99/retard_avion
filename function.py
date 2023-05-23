import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import fastparquet
from statsmodels.stats.outliers_influence import variance_inflation_factor



def count_nan(df):
    '''Pour chaques colonnes du dataframe donne le pourcentage de NaN'''
    nan_counts = df.isna().sum() # compte le nombre de NaN pour chaque colonne
    total_counts = len(df) # compte le nombre total de données dans le dataframe
    nan_percentages = (nan_counts / total_counts) * 100 # calcule le pourcentage de NaN pour chaque colonne
    
    return nan_percentages

def delete_nan(df, treshold):
    '''Ne prend pas en compte dans le df final  les colonnes qui posséde un pourcentage de NaN supperieure au treshold  '''
    nan_percentages = count_nan(df, treshold)
    nan_treshold = nan_percentages[nan_percentages.values < treshold]
    
    return df[nan_treshold.index]

def duplication(df):
    '''Donne le nombre de lignes dupliquées ainsi que le df des dupliqué'''
    nb = df.duplicated().sum()
    dupli = df[df.duplicated()]
    print(f'il y a {nb} lignes dupliquées')
    return dupli 

def boxplots(df, number):
    '''permet de ploter les differentes colonnes numerique en boxplot'''
    for col in number:
        sns.boxplot(x=df[col])
        plt.title(col)
        plt.show()

def outlier_identificator(df,colonne):
    '''Identification des outlier methode quantile'''
    q1=np.quantile(df[colonne],0.25)
    q3=np.quantile(df[colonne],0.75)
    out= (q3+1.5*(q3-q1)) 
    outlier=df.loc[df[colonne]> out]
    outlier = outlier.sort_values(by=colonne, ascending = False)
    return outlier

def univar_repartition(df, col):
    '''etude de la repartition des variables'''
    for i in col:
        fig = px.histogram(df, x=i)
        fig.update_layout(bargap=0.2)
        fig.show()

def histogram_plotly(df, x, *args, **kwargs ):
    '''pour utilisé le y et le hue il faut ecrire y= ou hue = '''
    y = kwargs.get('y', None)
    hue = kwargs.get('hue', None)
    if y!= None:
        fig = px.histogram(df, x= x, y = y, barmode='group')
    if hue!= None:
        fig = px.histogram(df, x= x, color = hue, barmode='group')
    if y!= None and hue!= None:
        fig = px.histogram(df, x= x, y=y, color = hue, barmode='group')

    fig.update_xaxes(type='category')
    fig.update_layout(bargap=0.2)
    fig.show()

def pourcent(df,list_colonne_groupby,colonne_cible): 
    data = df.groupby(list_colonne_groupby).agg({colonne_cible: 'sum'})
    data["%"] = data.apply(lambda x:  100*x / x.sum())
    data = data.reset_index()
    return data

def pourcent_fig(data,colonne ):
    fig = px.histogram(data,x=colonne, y='%', barmode='group')
    fig.update_xaxes(type='category')
    fig.update_layout(bargap=0.2,yaxis_title="%")
    fig.show()

def multicollinearity_check(X, thresh=5.0):
    data_type = X.dtypes
    # print(type(data_type))
    int_cols = \
    X.select_dtypes(include=['int', 'int16', 'int32', 'int64', 'float', 'float16', 'float32', 'float64']).shape[1]
    total_cols = X.shape[1]
    try:
        if int_cols != total_cols:
            raise Exception('All the columns should be integer or float, for multicollinearity test.')
        else:
            variables = list(range(X.shape[1]))
            dropped = True
            print('''\n\nThe VIF calculator will now iterate through the features and calculate their respective values.
            It shall continue dropping the highest VIF features until all the features have VIF less than the threshold of 5.\n\n''')
            while dropped:
                dropped = False
                vif = [variance_inflation_factor(X.iloc[:, variables].values, ix) for ix in variables]
                print('\n\nvif is: ', vif)
                maxloc = vif.index(max(vif))
                if max(vif) > thresh:
                    print('dropping \'' + X.iloc[:, variables].columns[maxloc] + '\' at index: ' + str(maxloc))
                    # del variables[maxloc]
                    X.drop(X.columns[variables[maxloc]], axis = 1, inplace=True)
                    variables = list(range(X.shape[1]))
                    dropped = True

            print('\n\nRemaining variables:\n')
            print(X.columns[variables])
            # return X.iloc[:,variables]
            return X
    except Exception as e:
        print('Error caught: ', e)