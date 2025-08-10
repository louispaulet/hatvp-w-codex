"""Utility functions for personal information extraction."""

from __future__ import annotations

import pandas as pd


AGE_BANDS = [0, 30, 40, 50, 60, 70, 80, 90, 200]
AGE_LABELS = ["<30", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"]


def compute_age_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute age related features from a personal information dataframe.

    Parameters
    ----------
    df:
        DataFrame containing at least ``dateDepot`` and ``dateNaissance``
        columns formatted as ``"%d/%m/%Y %H:%M:%S"`` and ``"%d/%m/%Y"``
        respectively.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with new ``age`` and ``age_band`` columns.
    """

    data = df.copy()
    deposit = pd.to_datetime(
        data["dateDepot"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    )
    birth = pd.to_datetime(
        data["dateNaissance"], format="%d/%m/%Y", errors="coerce"
    )
    valid = deposit.notna() & birth.notna()
    age = pd.Series(pd.NA, index=data.index, dtype="Int64")
    year_diff = deposit.dt.year - birth.dt.year
    before_birthday = (
        (deposit.dt.month < birth.dt.month)
        | ((deposit.dt.month == birth.dt.month) & (deposit.dt.day < birth.dt.day))
    )
    year_diff = year_diff - before_birthday.astype(int)
    age[valid] = year_diff[valid]
    data["age"] = age
    data["age_band"] = pd.cut(
        data["age"], bins=AGE_BANDS, labels=AGE_LABELS, right=False
    )
    return data
