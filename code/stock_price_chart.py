# 
# Stock Price Chart
# by Georgios Ouzounis, June 2021
#
# This code is asssembled from the the article posted in Medium.com
# original code source: https://medium.com/analytics-vidhya/visualizing-historical-stock-price-and-volume-from-scratch-46029b2c5ef9
# by Trifunovic Uros, Mar. 23, 2021

import requests
import pandas as pd
import matplotlib.pyplot as plt

colors = {'red': '#ff207c', 'grey': '#42535b', 'blue': '#207cff', 'orange': '#ffa320', 'green': '#00ec8b'}
config_ticks = {'size': 14, 'color': colors['grey'], 'labelcolor': colors['grey']}
config_title = {'size': 18, 'color': colors['grey'], 'ha': 'left', 'va': 'baseline'}

def format_borders(plot):
	plot.spines['top'].set_visible(False)
	plot.spines['left'].set_visible(False)
	plot.spines['left'].set_color(colors['grey'])
	plot.spines['bottom'].set_color(colors['grey'])

def get_prev_day_info(plot, stock_df):
	previous_close='$' + str("{:,}".format(stock_df['Open'][0])) 
	previous_volume=str("{:,}".format(stock_df['Volume'][0]))
	previous_date=str(stock_df['Date'][0].date())    
	plot.set_title(
		'Closing price on ' + previous_date + ': ' + 
		previous_close  + '\nShares traded on ' + previous_date +
		': ' + previous_volume, fontdict=config_title, loc='left'
	)

def plot_ma(plot, x, y):
	mov_avg = {
		'MA (50)': {'Range': 50, 'Color': colors['orange']}, 
		'MA (100)': {'Range': 100, 'Color': colors['green']}, 
		'MA (200)': {'Range': 200, 'Color': colors['red']}
	}
    
	for ma, ma_info in mov_avg.items():
		plot.plot(
			x, y.rolling(ma_info['Range']).mean(), 
			color=ma_info['Color'], label=ma, linewidth=2, ls='--'
		)

def format_legend(plot):
	plot_legend = plot.legend(loc='upper left', 
	bbox_to_anchor= (-0.005, 0.95), fontsize=16)    
	for text in plot_legend.get_texts():
		text.set_color(colors['grey'])

def get_charts(stock_data):

	date = stock_data['Date']
	vol = stock_data['Volume']
	value = stock_data['Close']

	plt.rc('figure', figsize=(15, 10))
    
	fig, axes = plt.subplots(2, 1, 
		gridspec_kw={'height_ratios': [3, 1]})
	fig.tight_layout(pad=3)
    
    
	plot_price = axes[0]
	plot_price.plot(date, value, color=colors['blue'], linewidth=2, label='Price')
	plot_price.yaxis.tick_right()
	plot_price.tick_params(axis='both', **config_ticks)
	plot_price.set_ylabel('Price (in USD)', fontsize=14)
	plot_price.yaxis.set_label_position("right")
	plot_price.yaxis.label.set_color(colors['grey'])
	plot_price.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.5)
	plot_price.set_axisbelow(True)
	plot_vol = axes[1]
	plot_vol.bar(date, vol, width=15, color='darkgrey')

	format_borders(plot_price)
	format_borders(plot_vol)

	get_prev_day_info(plot_price, stock_data)

	plot_ma(plot_price, date, value)
    
	format_legend(plot_price)

