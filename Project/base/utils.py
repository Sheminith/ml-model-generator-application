import pandas as pd

def remove_duplicated_cols(dataset):
    """
    01)
    Remove duplicated columns.
    """
    # .loc - selects data by labels
    # .loc - first argument(':' <- select all rows) second argument(select columns)
    # '~' sign flip the boolean value (ex: [False, False, True] -> [True, True, False])
    df = dataset.loc[:, ~dataset.columns.duplicated()]

    return df

def remove_empty_or_constant_cols(dataset):
    """
    02)
    Remove columns with 'all empty' values or 'same value' in every row.
    """
    # Remove columns with all NaN values
    df = dataset.dropna(axis=1, how='all')

    # Keep columns that has no same values for all the rows
    df = dataset.loc[:, dataset.nunique() > 1]

    return df

def remove_sensitive_cols(dataset, threshold=0.7):
    """
    03)
    Automatically detect columns with sensitive personal information such as:
        - Phone numbers
        - Emails
        - Postal/Zip codes
        - Names/Mostly text
        - Addresses
    """
    df = dataset.copy()
    cols_to_drop = []

    # Keywords for column names
    phone_keywords = ['phone', 'mobile', 'cell']
    email_keywords = ['email', 'mail', 'gmail']
    postal_keywords = ['zip', 'postal', 'postcode']
    name_keywords = ['name', 'fullname', 'first', 'last', 'sirname', 'nickname']
    address_keywords_cols = ['address', 'addr', 'street', 'location', 'home', 'billing', 'mailing']
    address_keywords_pattern = r"(?:St|Ave|Rd|Lane|Blvd|Drive|Court|Way|Pl|Sq|Circle|Terrace|Parkway)"

    # Patterns for content detection
    phone_pattern = r'^\+?\d{10,15}$' # 0752345679 or +94752345679
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    postal_pattern = r'^[A-Z]{0,2}\s?\d{5}(-\d{4})?$'
    address_pattern = rf".*\d+.*{address_keywords_pattern}.*"

    for col in df.columns:
        # Convert the entire column to strings
        series = df[col].astype(str)

        col_lower = col.lower()

        # Column name checks
        phone_name_flag = any(k in col_lower for k in phone_keywords) # any() Returns 'True' if atleast one element in any iterable is truthy
        email_name_flag = any(k in col_lower for k in email_keywords)
        postal_name_flag = any(k in col_lower for k in postal_keywords)
        name_name_flag = any(k in col_lower for k in name_keywords)
        address_name_flag = any(k in col_lower for k in address_keywords_cols)

        # Content checks
        phone_ratio = series.str.match(phone_pattern).mean()
        email_ratio = series.str.match(email_pattern).mean()
        postal_ratio = series.str.match(postal_pattern).mean()
        address_ratio = series.str.match(address_pattern).mean()
        text_ratio = (~series.str.replace(r'\s','').str.isnumeric()).mean() # Remove all spaces -> Check if string contains all numeric -> Invert to get the non-numeric -> Take mean

        # Rules to decide whether the column has to be dropped
        if phone_ratio >= threshold or phone_name_flag:
            cols_to_drop.append(col)
        elif email_ratio >= threshold or email_name_flag:
            cols_to_drop.append(col)
        elif postal_ratio >= threshold or postal_name_flag:
            cols_to_drop.append(col)
        elif address_ratio >= 0.1 or address_name_flag: # small fraction of content matches or column name matches to address keywords
            cols_to_drop.append(col)
        elif text_ratio >= 0.8 and name_name_flag: # most fraction of content matches and column name matches to name keywords
            cols_to_drop.append(col)

    # Remove duplicated
    cols_to_drop = list(set(cols_to_drop))

    # Drop columns
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    
    return df

def fix_data_types(datasets): # continue from here... I stopped here...
    """
    04)
    Fix data types of columns where columns contain string with numerical data. (e.g. '12345')
    """
    pass

def handle_missing_values(dataset):
    """
    03)
    Remove columns with some values according to most preffered thresholds.

    Dataset > 50,000 - Remove if 70-80% missing
    Dataset < 5000 - Remove if 20-30% missing

    If not,
    if the column is numeric, fill empty cells with the mean.
    if the column is categorical, handle accordingly.
    """
    pass