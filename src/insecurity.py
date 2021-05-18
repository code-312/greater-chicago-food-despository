import pandas as pd
from typing import List, Tuple
from src import data
from src.file_to_json import files_to_dataframes  # noqa: E402


def get_food_insecurity_data(input_dir: str = 'data_folder') -> data.Wrapper:
    tables: List[Tuple[str, pd.DataFrame]] = files_to_dataframes(input_dir, blacklist=['Key'])

    combined_data = data.Wrapper()
    for pair in tables:
        df: pd.DataFrame = pair[1]
        wrapper: data.Wrapper = data.from_county_dataframe(reformat_dataframe(df))
        combined_data = data.combine(combined_data, wrapper)
    return combined_data


def reformat_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    # Remove County Name column because it already exists in merged_src
    new_df = df.drop(labels='County Name', axis=1, )

    # Rename columns to stay consistent with merged_src formatting
    new_df.columns = ['2018', '2020_projected',
                      '2018_child', '2020_child_projected']
    return new_df