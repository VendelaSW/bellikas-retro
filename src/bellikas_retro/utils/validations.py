from __future__ import annotations
from typing import Iterable

# Checks that age is an integer within the allowed range.
def validate_age(age: int, min_age: int = 17, max_age: int = 60) -> int:
    if not isinstance(age, int):
        raise ValueError('Age must be an integer')
    
    if not (min_age <= age <= max_age):
        raise ValueError(f'Age must be between {min_age} and {max_age}')
    return age

# Ensures the selected region exists in the region mapping.
def validate_region(region: str, region_map: dict[str, str]) -> str:
    if region not in region_map:
        allowed = ', '.join(region_map.keys())
        raise ValueError(f'Region must be one of: {allowed}')
    return region

# Validates region and returns the corresponding sales column name.
def get_sales_column(region: str, region_map: dict[str, str]) -> str:
    validate_region(region, region_map)
    return region_map[region]

# Ensures the dataset contains at least one valid year.
def validate_years(years: Iterable) -> list:
    years_list = list(years)
    if len(years_list) == 0:
        raise ValueError('No years available in dataset (Year column empty or missing).')
    return years_list

# Checks that the selected year is available in the dataset.
def validate_selected_year(selected_year, years: list):
    if selected_year not in years:
        raise ValueError('Selected year in not in available year options.')
    return selected_year

# Ensures minimum sales is a non-negative number.
def validate_min_sales(minimun: float) -> float:
    if not isinstance(minimun, (int, float)):
        raise ValueError('Minimun sales must be a number')
    if minimun < 0:
        raise ValueError('Minimun sales must be >= 0')
    return float(minimun)