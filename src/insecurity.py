import pandas as pd
from src import data
from src.file_to_json import files_to_dataframes  # noqa: E402


def get_food_insecurity_data(input_dir: str = 'data_folder') -> data.Wrapper:
    tables = files_to_dataframes(input_dir, blacklist=['Key'])

    combined_data = data.Wrapper()
    for pair in tables:
        df = reformat_dataframe(pair[1])
        combined_data.add(data.from_county_dataframe(df))
    return combined_data


def reformat_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    # Remove County Name column because it already exists elsewhere in the data
    new_df = df.drop(labels='County Name', axis=1)

    # Rename columns to stay consistent with our column names elsewhere
    new_df.columns = ['insecurity_2018',
                      'insecurity_2020_projected',
                      'insecurity_2018_child',
                      'insecurity_2020_child_projected']
    return new_df
