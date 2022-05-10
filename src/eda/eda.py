import pandas as pd
from functools import reduce
from tabulate import tabulate
#Função para descrever uma coluna
def variable_summary(series):
    variable = series.name
    dtype = series.dtype
    na = series.isna().sum()
    na_pct = str(round(100*na/series.shape[0],2))+"%"
    if('object' in str(dtype)):
        first_element = series.pipe(lambda x: x[x==x])
        if(first_element.shape[0] == 0):
            unique = series.nunique()
        else:
            element_type = str(type(first_element.iloc[0]))
            if((element_type == "<class 'numpy.ndarray'>") | (element_type == "<class 'list'>") | (element_type == "<class 'set'>") | (element_type == "<class 'dict'>")):
                unique = '-'
            else:
                unique = series.nunique()
    else:
        unique = series.nunique()
    
    #Verificando se a variavel é categorica ou string
    if( ('object' in str(dtype)) | ('category' in str(dtype)) ):
        minimum,mean,maximum,std,quat25,quat75,median,skew,kurt,mean_std = ("-","-","-","-","-","-","-","-","-","-")
    else:
        minimum = series.min()
        mean = series.mean()
        maximum = series.max()
        std = series.std()
        if('bool' in str(dtype)):
            quat25 = series.astype(float).quantile(0.25)
            quat75 = series.astype(float).quantile(0.75)
            median = series.astype(float).quantile(0.5)
        else:
            quat25 = series.quantile(0.25)
            quat75 = series.quantile(0.75)
            median = series.quantile(0.5)
        
        if( ('int' in str(dtype)) | ('float' in str(dtype)) ):
            skew = round(series.skew(),2) #skewness
            kurt = round(series.kurt(),2) #kurtosis
            if((all(series == 0)) or (std == 0)):
                mean_std = 0
            else:
                mean_std = round(mean/std,2)
        else:
            skew,kurt,mean_std = ("-","-","-")
        
        
    return(pd.DataFrame({'variable':[variable],
                        'type':[dtype],
                        'na':[na],
                        'na_pct':[na_pct],
                        'unique':[unique],
                        'min':[minimum],
                        'quat25':[quat25],
                        'median':[median],
                        'mean':[mean],
                        'quat75':[quat75],
                        'max':[maximum],
                        'std':[std],
                        'skewness':[skew],
                        'kurtosis':[kurt],
                        'media_desvio':[mean_std]}))

#Função para uma descrição geral dos dados
def describe(df):
    print("Quantidade de linhas:",df.shape[0])
    describe_dataset = reduce(lambda x,y: pd.concat((x,y)), [variable_summary(df[col]) for col in df.columns])
    return describe_dataset.reset_index(drop=True)


def print_df(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))