import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    return df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
car_matrix.values[[range(len(car_matrix))]*2] = 0
    
    return car_matrix



def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    
    type_counts = df['car_type'].value_counts().to_dict()

    
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

    return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus = df['bus'].mean()
    return df[df['bus'] > 2 * mean_bus].index.tolist()

    return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck_per_route = df.groupby('route')['truck'].mean()
    return avg_truck_per_route[avg_truck_per_route > 7].index.tolist()

    return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
modified_matrix = matrix.copy()

    
    modified_matrix[matrix > 20] *= 0.75
    modified_matrix[matrix <= 20] *= 1.25

   
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    
    df['duration'] = df['end_datetime'] - df['start_datetime']

    
    result_series = df.groupby(['id', 'id_2']).apply(lambda group: (
        group['duration'].sum() == pd.Timedelta(days=7) and
        group['start_datetime'].min().time() == pd.Timestamp('00:00:00').time() and
        group['end_datetime'].max().time() == pd.Timestamp('23:59:59').time()
    ))
    return pd.Series()
