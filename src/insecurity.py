import pandas as pd
from src import data
from src.file_to_json import files_to_dataframes  # noqa: E402


column_names = ['insecurity_2018',
                'insecurity_2020_projected',
                'insecurity_2018_child',
                'insecurity_2020_child_projected']

def get_food_insecurity_data(input_dir: str = 'data_folder/insecurity') -> data.Wrapper:  # noqa E501
    tables = files_to_dataframes(input_dir, blacklist=['Key'])

    combined_data = data.Wrapper()
    for pair in tables:
        df = reformat_dataframe(pair[1])
        combined_data.add(data.from_county_dataframe(df))
        combined_data.meta.data_bins['natural_breaks'] = data.calculate_natural_breaks_bins(df, column_names)  # noqa E501
        combined_data.meta.data_bins['quantiles'] = data.calculate_quantiles_bins(df, column_names)  # noqa E501
    return combined_data


def reformat_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    # Remove County Name column because it already exists elsewhere in the data
    new_df = df.drop(labels='County Name', axis=1)

    # Rename columns to stay consistent with our column names elsewhere
    new_df.columns = column_names
    return new_df
