def filter_on_channels(dataframe, channel_a, channel_b, max_diff=5, max_pct_diff=0.61):
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


