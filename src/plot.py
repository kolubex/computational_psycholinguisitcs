#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# plot.py

import os
import warnings
from math import ceil, floor
from pathlib import Path

import matplotlib.pyplot as plt
plt.ioff() # Don't show plots in pop-up window
import matplotlib.cbook as cbook
warnings.filterwarnings('ignore', category=cbook.mplDeprecation)
import numpy as np
import pandas as pd
from mycolorpy import colorlist as mcp

import analyze
import constants


if __name__ == '__main__':
	# Define directory and file paths
	HOME_DIR = Path(__name__).resolve().parents[1]
	PROJECT_DIR = os.path.join(HOME_DIR, 'project')
	DATA_DIR = os.path.join(PROJECT_DIR, 'data')
	RESULTS_PATH = os.path.join(DATA_DIR, 'dataMM.txt')
	FIGURES_DIR = os.path.join(PROJECT_DIR, 'figures')
	if not os.path.exists(FIGURES_DIR):
		os.mkdir(FIGURES_DIR)

	# Create dataframe
	df = pd.read_csv(RESULTS_PATH, sep='\t')	
	df_common = analyze.get_subset(df, 'category', 'common')
	df_rare = analyze.get_subset(df, 'category', 'rare')

	# Adverb surprisal vs. Adverb RT (by category)
	fig_path = os.path.join(FIGURES_DIR, 'surprisal_vs_adv_RT.png')
	plt.scatter(df_common['surprisal'], df_common['adv_RT'], color='blueviolet', label='Common')
	plt.scatter(df_rare['surprisal'], df_rare['adv_RT'], color='gold', label='Rare')
	plt.title('Adverb Surprisal vs. Adverb RT')
	plt.xlabel('Surprisal (bits)')
	plt.ylabel('Reading Time (sec)')
	plt.xlim(10, 65, 5)
	plt.ylim(0, ceil(np.max(df['adv_RT']))+1)
	plt.legend(loc='best')
	plt.savefig(fig_path)
	plt.clf()

	# Adverb surprisal vs. Adverb RT (by category)
	fig_path = os.path.join(FIGURES_DIR, 'surprisal_vs_adv_RT.png')
	plt.scatter(df_common['surprisal'], df_common['adv_RT'], color='blueviolet', label='Common')
	plt.scatter(df_rare['surprisal'], df_rare['adv_RT'], color='gold', label='Rare')
	plt.title('Adverb Surprisal vs. Adverb RT')
	plt.xlabel('Surprisal (bits)')
	plt.ylabel('Reading Time (sec)')
	plt.xlim(10, 65, 5)
	plt.ylim(0, ceil(np.max(df['adv_RT']))+1)
	plt.legend(loc='best')
	plt.savefig(fig_path)
	plt.clf()

	# Adverb surprisal vs. Adverb RT (Common)
	fig_path = os.path.join(FIGURES_DIR, 'surprisal_vs_adv_RT_common.png')
	df_common_sorted = df_common.sort_values(by=['surprisal'])
	x = df_common_sorted['surprisal']
	x_unique = sorted(list(set(x)))
	y_adv = df_common_sorted['adv_RT']
	colors = mcp.gen_color(cmap='tab20', n=len(x_unique))
	cmap = {surprisal: color for surprisal, color in zip(x_unique, colors)}
	for xe, ye in zip(x, y_adv):
		color = cmap.get(xe)
		plt.scatter([xe] * 1, ye, c=color)
	plt.title('Adverb Surprisal vs. Adverb RT (Common)')
	plt.xlabel('Surprisal (bits)')
	plt.ylabel('Reading Time (sec)')
	plt.xlim(floor(np.min(x)), ceil(np.max(x)), 0.5)
	plt.ylim(0, ceil(np.max(df['adv_RT'])))
	plt.savefig(fig_path)
	plt.clf()

	# Adverb surprisal vs. Adverb RT (Rare)
	fig_path = os.path.join(FIGURES_DIR, 'surprisal_vs_adv_RT_rare.png')
	df_rare_sorted = df_rare.sort_values(by=['surprisal'])
	x = df_rare_sorted['surprisal']
	x_unique = sorted(list(set(x)))
	y_adv = df_rare_sorted['adv_RT']
	colors = mcp.gen_color(cmap='tab20', n=len(x_unique))
	cmap = {surprisal: color for surprisal, color in zip(x_unique, colors)}
	for xe, ye in zip(x, y_adv):
		color = cmap.get(xe)
		plt.scatter([xe] * 1, ye, c=color)
	plt.title('Adverb Surprisal vs. Adverb RT (Rare)')
	plt.xlabel('Surprisal (bits)')
	plt.ylabel('Reading Time (sec)')
	plt.xlim(floor(np.min(x))-1, ceil(np.max(x))+3)
	plt.ylim(0, ceil(np.max(df['adv_RT'])))
	plt.savefig(fig_path)
	plt.clf()

	# Adverb surprisal vs. Sentence RT
	fig_path = os.path.join(FIGURES_DIR, 'surprisal_vs_sent_RT.png')
	plt.scatter(df_common['surprisal'], df_common['sentence_RT'], color='blueviolet', label='Common')
	plt.scatter(df_rare['surprisal'], df_rare['sentence_RT'], color='gold', label='Rare')
	plt.title('Adverb Surprisal vs. Sentence RT')
	plt.xlabel('Surprisal (bits)')
	plt.ylabel('Reading Time (sec)')
	plt.xlim(10, 65, 5)
	plt.ylim(0, ceil(np.max(df['sentence_RT']))+5)
	plt.legend(loc='best')
	plt.savefig(fig_path)
	plt.clf()

	# Mean Adverb RT by Adverb Length (characters)
	df_rt_word_len_common = analyze.calc_rt_by_category(df_common, 'word_length')
	df_rt_word_len_rare = analyze.calc_rt_by_category(df_rare, 'word_length')
	x_len_common = df_rt_word_len_common['word_length']
	x_len_rare = df_rt_word_len_rare['word_length']
	y_adv_common = df_rt_word_len_common['adv_RT_mean'].to_dict()
	y_adv_rare = df_rt_word_len_rare['adv_RT_mean'].to_dict()
	x = list(set(df['word_length']))
	x_axis = np.arange(min(x), max(x)+1)
	y_common = analyze.assemble(x, y_adv_common)
	y_rare = analyze.assemble(x, y_adv_rare)

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_word_len.png')
	plt.bar(x_axis - 0.2, y_common, 0.4, color='blueviolet', label='Common')
	plt.bar(x_axis + 0.2, y_rare, 0.4, color='gold', label='Rare')
	plt.axhline(np.mean(list(y_adv_common.values())), c='blueviolet', linestyle='--')
	plt.axhline(np.mean(list(y_adv_rare.values())), c='gold', linestyle='--')
	plt.xticks(x_axis, x)
	plt.legend(loc='best')
	plt.title('Mean Adverb RTs by Adverb Length')
	plt.xlabel('Length (Characters)')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()
	print(f'Mean adverb RT for common')

	# Mean Adverb RT by Participant
	df_rt_id_common = analyze.calc_rt_by_category(df_common, 'id')
	df_rt_id_rare = analyze.calc_rt_by_category(df_rare, 'id')
	y_adv_common = df_rt_id_common['adv_RT_mean']
	y_adv_rare = df_rt_id_rare['adv_RT_mean']
	x = df_rt_id_rare['id']
	x_axis = np.arange(len(x))

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_participant.png')
	plt.bar(x_axis - 0.2, y_adv_common, 0.4, color='blueviolet', label='Common')
	plt.bar(x_axis + 0.2, y_adv_rare, 0.4, color='gold', label='Rare')
	plt.axhline(np.mean(y_adv_common), c='blueviolet', linestyle='--')
	plt.axhline(np.mean(y_adv_rare), c='gold', linestyle='--')
	plt.xticks(x_axis, x)
	plt.ylim(0, ceil(np.max(y_adv_rare)))
	plt.legend(loc='best')
	plt.title('Mean Adverb RTs by Participant')
	plt.xlabel('Participant ID')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()

	# Mean Adverb RT by Adverb (Common)
	adv_common = [adv_tuple[0] for adv_tuple in constants.ADV_TUPLE]
	df_rt_common = analyze.calc_rt_by_category(df_common, 'adv').sort_values(by=['adv'], key=lambda x: adv_common)
	y_adv = df_rt_common['adv_RT_mean']
	y_adv_mean = np.mean(y_adv)

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_adv_common.png')
	plt.figure(figsize=(10,6))
	plt.bar(adv_common, y_adv, yerr=np.std(y_adv), color='blueviolet', alpha=0.5, ecolor='black', capsize=5)
	plt.axhline(y_adv_mean, c='blueviolet', linestyle='--')
	plt.tick_params(axis='x', labelrotation=25)
	plt.ylim(0, 4.5) # Match scale of rare adverb plot
	plt.title('Mean Adverb RTs by Adverb (Common)')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()
	print(f'Mean adverb RT for common: {y_adv_mean}')

	# Mean Adverb RT by Adverb (Rare)
	adv_rare = [adv_tuple[1] for adv_tuple in constants.ADV_TUPLE]
	df_rt_rare = analyze.calc_rt_by_category(df_rare, 'adv').sort_values(by=['adv'], key=lambda x: adv_rare)
	y_adv = df_rt_rare['adv_RT_mean']
	y_adv_mean = np.mean(y_adv)

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_adv_rare.png')
	plt.figure(figsize=(10,6))
	plt.bar(adv_rare, y_adv, yerr=np.std(y_adv), color='gold', alpha=0.5, ecolor='black', capsize=5)
	plt.axhline(y_adv_mean, c='gold', linestyle='--')
	plt.tick_params(axis='x', labelrotation=25)
	plt.ylim(0, ceil(np.max(y_adv))+0.5)
	plt.title('Mean Adverb RTs by Adverb (Rare)')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()
	print(f'Mean adverb RT for rare: {y_adv_mean}')

	# Mean Sentence RT by Adverb (Common)
	adv_common = [adv_tuple[0] for adv_tuple in constants.ADV_TUPLE]
	df_rt_common = analyze.calc_rt_by_category(df_common, 'adv').sort_values(by=['adv'], key=lambda x: adv_common)
	y_adv = df_rt_common['sent_RT_mean']
	y_adv_mean = np.mean(y_adv)

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_sent_common.png')
	plt.figure(figsize=(10,6))
	plt.bar(adv_common, y_adv, yerr=np.std(y_adv), color='blueviolet', alpha=0.5, ecolor='black', capsize=5)
	plt.axhline(y_adv_mean, c='blueviolet', linestyle='--')
	plt.tick_params(axis='x', labelrotation=25)
	plt.ylim(0, 16) # Match scale of rare adverb plot
	plt.title('Mean Sentence RTs by Adverb (Common)')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()
	print(f'Mean sentence RT for common: {y_adv_mean}')

	# Mean Sentence RT by Adverb (Rare)
	adv_rare = [adv_tuple[1] for adv_tuple in constants.ADV_TUPLE]
	df_rt_rare = analyze.calc_rt_by_category(df_rare, 'adv').sort_values(by=['adv'], key=lambda x: adv_rare)
	y_adv = df_rt_rare['sent_RT_mean']
	y_adv_mean = np.mean(y_adv)

	fig_path = os.path.join(FIGURES_DIR, 'mean_RT_sent_rare.png')
	plt.figure(figsize=(10,6))
	plt.bar(adv_rare, y_adv, yerr=np.std(y_adv), color='gold', alpha=0.5, ecolor='black', capsize=5)
	plt.axhline(y_adv_mean, c='gold', linestyle='--')
	plt.tick_params(axis='x', labelrotation=25)
	plt.ylim(0, 16)
	plt.title('Mean Sentence RTs by Adverb (Rare)')
	plt.ylabel('Reading Time (sec)')
	plt.savefig(fig_path)
	plt.clf()
	print(f'Mean sentence RT for rare: {y_adv_mean}')