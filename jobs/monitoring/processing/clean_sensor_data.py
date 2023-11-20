import pandas as pd

def filter_on_channels(dataframe, channel_a, channel_b, max_diff=5, max_pct_diff=0.61) -> pd.DataFrame:
    '''
    Filters rows in the DataFrame based on the absolute and percentage difference 
    between two specified columns representing sensor channels A and B.

    Args:
        dataframe (pd.DataFrame): A pandas DataFrame with air pollution data.
        channel_a (str): The name of the first channel (e.g., 'pm1.0_atm_a').
        channel_b (str): The name of the second channel (e.g., 'pm1.0_atm_b').
        max_diff (float, optional): The maximum acceptable absolute difference 
                                    in μg between the two channels. Default is 5.
        max_pct_diff (float, optional): The maximum acceptable percentage difference 
                                        between the two channels, expressed as a fraction 
                                        (e.g., 0.61 for 61%). Default is 0.61.
    
    Returns:
        pd.DataFrame: A DataFrame filtered based on the specified criteria.
    '''
    # Abs difference
    absolute_difference = abs(dataframe[channel_a] - dataframe[channel_b])
    # Pc difference, where the denominator is not zero to avoid division by zero
    percentage_difference = abs((dataframe[channel_a] - dataframe[channel_b]) / dataframe[channel_b].replace(0, float('nan')))
    
    condition = (absolute_difference <= max_diff) & (percentage_difference <= max_pct_diff)
    return dataframe[condition].copy()



def convert_to_dataframe(response_dictionary) -> pd.DataFrame:
    """
    Convert a dictionary of sensor data into a pandas DataFrame.

    The input dictionary should have sensor IDs as keys and lists of measurement dictionaries as values.
    Each measurement dictionary in the input will be flattened, with the sensor ID added to it.

    Parameters:
    - response_dictionary (dict): A dictionary with sensor IDs as keys and lists of measurement
                                  dictionaries as values.

    Returns:
    - pandas.DataFrame: A DataFrame containing the flattened sensor data, showing only the first
                        few rows.
    """
    flattened_data = []

    for sensor_id, readings in response_dictionary.items():
        for reading in readings[0]: 
            reading['sensor_id'] = sensor_id
            flattened_data.append(reading)

    return pd.DataFrame(flattened_data)
