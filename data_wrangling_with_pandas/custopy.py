# Creating a Module for Our Customer Call Project

# Define a function
def tweak_customer_call_data(df, labels, column_names):
    """
    Clean and format customer call data.

    This function takes a DataFrame as input, performs various data cleaning and
    formatting operations on it, and returns the cleaned DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing customer call data.

    Returns:
    pandas.DataFrame: A cleaned and formatted DataFrame with the following
    modifications:
    - Cleaned last names in the 'last_name' column.
    - Transformed 'paying_customer' and 'do_not_contact' columns.
    - Cleaned and formatted 'phone_number' column.
    - Split 'address' column into 'Street Address', 'State', and 'Zip Code'.
    - Dropped unwanted columns 'not_useful_column' and 'address'.
    - Filtered rows where 'do_not_contact' is not 'Yes' or is not NaN and 'phone_number' is not NaN.
    - Renamed the 'customerid' column to 'customer_id'.
    - Reset the DataFrame index.

    Notes:
    - The 'clean_last_name_revised' function is used to clean the 'last_name' column.
    - The 'clean_phone_number' function is used to clean and format phone numbers.
    - The 'clean_address' function is used to split the 'address' column into 'Street Address', 'State', and 'Zip Code'.

    Example:
    df = tweak_customer_call_data(customer_raw)
    """
    # Include required libraries
    import re
    import numpy as np
    import pandas as pd
    from janitor import clean_names

    # Define a function to clean and format phone numbers
    def clean_phone_number(phone):
        # Convert the value to a string, and then remove non-alphanumeric characters
        phone = re.sub(r'\D', '', str(phone))

        # Check if the phone number has 10 digits
        if len(phone) == 10:
            # Format the phone number as xxx-xxx-xxxx
            phone = f'{phone[:3]}-{phone[3:6]}-{phone[6:]}'
        else:
            # Handle other formats or invalid phone numbers
            phone = np.nan

        return phone

    # Define a function to clean last names
    def clean_last_name_revised(name):
        if pd.isna(name):
            return ''
        # Remove non-alphabetic characters but keep spaces, single quotes, and hyphens
        name = re.sub(r"[^A-Za-z\-\s']", '', name).strip()
        name = re.sub(r"\s+", " ", name)
        return name

    # Define a function to clean and transform the address column
    def clean_address(df):
        df[['street_address', 'state', 'zip_code']] = df['address'].str.split(',', n=2, expand=True)
        return df

    # Clean and transform the data
    # ----------------------------
    return (
        df
        # Clean and transform column values
        .assign(
            last_name=lambda x: x['last_name'].apply(clean_last_name_revised),
            paying_customer=lambda x: x['paying_customer'].str.lower().replace(labels),
            do_not_contact=lambda x: x['do_not_contact'].str.lower().replace(labels),
            phone_number=lambda x: x['phone_number'].apply(clean_phone_number)
        )
        # Split address column into: Street Address, State, and Zip Code
        .pipe(clean_address)
        # Delete unwanted columns
        .drop(columns=['not_useful_column', 'address'])
        .query('~(do_not_contact == "yes" | do_not_contact.isna() | phone_number.isna())')
        .rename(columns=column_names)
        .reset_index(drop=True)
    )
