import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
distance_matrix = df.copy()

    
    distance_dict = {}

    
    for index, row in df.iterrows():
        start_toll = row['start_toll']
        end_toll = row['end_toll']
        distance = row['distance']

        
        if (start_toll, end_toll) in distance_dict:
            distance_dict[(start_toll, end_toll)] += distance
        elif (end_toll, start_toll) in distance_dict:
            distance_dict[(end_toll, start_toll)] += distance
        else:
           
            distance_dict[(start_toll, end_toll)] = distance

    
    for index, row in distance_matrix.iterrows():
        start_toll = row['start_toll']
        end_toll = row['end_toll']

        
        if (start_toll, end_toll) in distance_dict:
            distance_matrix.at[index, 'distance'] = distance_dict[(start_toll, end_toll)]
        elif (end_toll, start_toll) in distance_dict:
            distance_matrix.at[index, 'distance'] = distance_dict[(end_toll, start_toll)]

    distance_matrix = distance_matrix.pivot(index='start_toll', columns='end_toll', values='distance')

    
    distance_matrix = distance_matrix.fillna(0)
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    return distance_matrix



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
    for id_start in df.index:
        for id_end in df.columns:
            distance = df.loc[id_start, id_end]
            unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)
    return unrolled_df



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
reference_df = df[df['id_start'] == reference_id]
    reference_avg_distance = reference_df['distance'].mean()

    # Calculate the lower and upper bounds based on the 10% threshold
    lower_bound = reference_avg_distance - 0.1 * reference_avg_distance
    upper_bound = reference_avg_distance + 0.1 * reference_avg_distance

    
    result_df = df[(df['id_start'] != reference_id) & (df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    
    result_df = result_df.sort_values(by='id_start')
    return result_df



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
df_with_rates = df.copy()

    
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = vehicle_type
        df_with_rates[column_name] = df_with_rates['distance'] * rate_coefficient
     return df_with_rates



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    
    df_with_time_rates = df.copy()

    
    weekday_time_ranges = [
        (time(0, 0, 0), time(10, 0, 0)),
        (time(10, 0, 0), time(18, 0, 0)),
        (time(18, 0, 0), time(23, 59, 59))
    ]

    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))

    
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    
    start_days = []
    start_times = []
    end_days = []
    end_times = []

    
    for index, row in df_with_time_rates.iterrows():
        
        start_time = row['start_time']
        end_time = row['end_time']

        
        if start_time.weekday() < 5:  
            
            discount_factor = 1.0 
            for i, time_range in enumerate(weekday_time_ranges):
                if time_range[0] <= start_time <= time_range[1]:
                    discount_factor = weekday_discount_factors[i]
                    break
        else:  
            discount_factor = weekend_discount_factor

        
        vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
        for column in vehicle_columns:
            df_with_time_rates.at[index, column] *= discount_factor

        
        start_days.append(start_time.strftime('%A'))  
        start_times.append(start_time)
        end_days.append(end_time.strftime('%A')) 
        end_times.append(end_time)

    
    df_with_time_rates['start_day'] = start_days
    df_with_time_rates['start_time'] = start_times
    df_with_time_rates['end_day'] = end_days
    df_with_time_rates['end_time'] = end_times

    return df_with_time_rates


