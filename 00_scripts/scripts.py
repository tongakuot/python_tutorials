def tweak_ss_census(df):
    return(df
          [cols]
          .rename(columns = cols_names)
          .query('~age_cat.isna() & gender != "Total" & age_cat != "Total"')
          .assign(gender = lambda df_: df_['gender'].str.split('\s+').str[1],
                 age_cat = lambda df_: df_['age_cat'].replace(new_age_cats),
                 population = lambda df_: df_['population'].astype('int')
          )
          # .query('gender != "Total" & age_cat != "Total"'
          .groupby(['state', 'gender', 'age_cat'])['population']
          .sum()
          .reset_index()
       )
