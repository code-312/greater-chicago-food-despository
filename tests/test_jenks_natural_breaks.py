import os
import json
from breaks.jenks_natural_breaks import classify_zip_code_poverty, GeographicDivision, PovertyBins


def test_zip_code_poverty():
    with open(os.path.join(os.path.dirname(__file__), "resources", "test_zip_poverty.json")) as f:
        zip_data = json.loads(f.read()).get("zip")
        actual = classify_zip_code_poverty(zip_data, 4, GeographicDivision.ZIP_CODE)
        expected = PovertyBins(
            geographic_division=GeographicDivision.ZIP_CODE,
            child_poverty_population_bins=[0.0, 696.0, 2080.0, 4499.0, 12443.0],
            overall_poverty_population_bins=[0.0, 1497.0, 5064.0, 11505.0, 28488.0],
            overall_poverty_rate_bins=[0.0, 0.10506140968473754, 0.2268610668789809, 0.5408163265306123, 1.0]
        )
        assert actual == expected


def test_county_poverty():
    with open(os.path.join(os.path.dirname(__file__), "resources", "test_county_poverty.json")) as f:
        county_data = json.loads(f.read()).get("county")
        print(county_data)
        actual = classify_zip_code_poverty(county_data, 2, GeographicDivision.COUNTY)
        expected = PovertyBins(
            geographic_division=GeographicDivision.COUNTY,
            child_poverty_population_bins=[207.0, 618.0, 1206.0],
            overall_poverty_population_bins=[501.0, 1944.0, 3551.0],
            overall_poverty_rate_bins=[0.08811115019345761, 0.11030064696181657, 0.178576816696002]
        )
        assert actual == expected
