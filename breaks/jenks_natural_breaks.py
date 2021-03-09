import enum
from dataclasses import dataclass
from typing import List, Tuple, Dict
import jenkspy


def classify_data(input: List[float], class_number: int) -> Tuple[float]:
    return jenkspy.jenks_breaks(input, nb_class=class_number)


class GeographicDivision(enum.Enum):
    COUNTY = 1
    ZIP_CODE = 2


@dataclass
class PovertyBins:
    geographic_division: GeographicDivision
    child_poverty_population_bins: List[float]
    overall_poverty_population_bins: List[float]
    overall_poverty_rate_bins: List[float]


def classify_zip_code_poverty(zip_data: Dict, class_number: int, geo_div: GeographicDivision) -> PovertyBins:
    child_poverty_count = []
    overall_poverty_count = []
    overall_poverty_rate = []
    for k, v in zip_data.items():
        poverty_metrics = v.get('poverty_metrics')
        population_poverty = poverty_metrics.get('poverty_population_poverty')

        child_poverty_count.append(poverty_metrics.get('poverty_population_poverty_child'))
        overall_poverty_count.append(population_poverty)
        try:
            rate = population_poverty / poverty_metrics.get('poverty_population_total')
            overall_poverty_rate.append(rate)
        except ZeroDivisionError:
            # Exclude 0 poverty population records from the rate calculation.
            # These values would greatly affect the natural breaks.
            pass

    child_count_bins = list(classify_data(child_poverty_count, class_number))
    overall_count_bins = list(classify_data(overall_poverty_count, class_number))
    overall_rate_bins = list(classify_data(overall_poverty_rate, class_number))

    return PovertyBins(geographic_division=geo_div, child_poverty_population_bins=child_count_bins,
                       overall_poverty_population_bins=overall_count_bins, overall_poverty_rate_bins=overall_rate_bins)
