from typing import Callable
import pandas as pd

def filter_rows(dataframe: pd.DataFrame, condition: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame:
    """
    Filters rows in the DataFrame based on a condition function.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        condition (Callable[[pd.DataFrame], pd.Series]): A function that takes a DataFrame and returns a boolean Series.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where the condition is True.
    """
    return dataframe[condition(dataframe)]