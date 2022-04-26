def tweak_ss_census_data(df):
    return(df
          [cols]
          .rename(columns = cols_names)
          .query('~age_cat.isna()')
          .assign(gender = lambda x:x['gender'].str.split('\s+').str[1],
                 age_cat = lambda x:x['age_cat'].replace(new_age_cats),
                 population = lambda x:x['population'].astype('int')
          )
          .query('gender != "Total" & age_cat != "Total"'
          .groupby(['state', 'gender', 'age_cat'])['population']
          .sum()
          .reset_index()
       )
