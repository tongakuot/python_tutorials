import pandas as pd
import datetime as dt

df = pd.read_csv('data.csv')

df['date'] = df['Month']+' '+df['Year'].astype(str)

dates_df = pd.DataFrame([d.strftime('%b %Y') for d in pd.date_range('Jan 2022','Jan 2023',freq='M')],columns=['date'])

new_df = pd.pivot_table(df, values='Amount', index=['Variable'],
                    columns=['date'], aggfunc=sum, fill_value=0).T\
                        .merge(dates_df,on='date',how='right').T\
                           .fillna(0).rename(index={'date':'Variable'}).T.set_index('Variable')\
                            .T.assign(YearTotal = lambda x: x.sum(axis=1).astype(int))\
                                .reindex(['Salary','Bonus', 'Taxes']).astype('int32')

new_df.loc['TotalBrutto'] = new_df.sum()      
new_df
