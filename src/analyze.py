#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# analyze.py

"""Analyze data from reading experiments."""

from typing import Dict, List, Union

import numpy as np
import pandas as pd


def get_subset(df: pd.DataFrame, column_name: str, value: Union[float, int, str]) -> pd.DataFrame:
	"""Get subset of dataframe corresponding to particular column value."""
	return df.loc[df[column_name] == value]


def calc_rt_metrics_subset(
	df: pd.DataFrame,
	column_name: str,
	value: Union[float, int, str]
) -> List[Union[float, int]]:
	"""Calculate mean and median RTs (adverb and sentence) corresponding to particular column value."""
	df_subset = get_subset(df, column_name, value)
	return [
		value,
		np.mean(df_subset['adv_RT']), np.median(df_subset['adv_RT']),
		np.mean(df_subset['sentence_RT']), np.median(df_subset['sentence_RT'])
	]


def calc_rt_by_category(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
	"""Calculate mean and median RTs (adverb and sentence) corresponding to each value in particular column."""
	column_values = set(df[column_name])
	subset_dict = {value: calc_rt_metrics_subset(df, column_name, value) for value in column_values}
	columns = [column_name, 'adv_RT_mean', 'adv_RT_median', 'sent_RT_mean', 'sent_RT_median']
	return pd.DataFrame(subset_dict, index=columns, dtype=object).transpose()


def assemble(
	idx: List[int],
	value_dict: Dict[int, Union[float, int, str]],
	default_val: Union[float, int, str]=0
) -> List[Union[float, int, str]]:
	"""Collect values corresponding to a specific index, given a list of indices."""
	assembled = [value_dict.get(i, default_val) for i in idx]
	return assembled