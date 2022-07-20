import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt 
import os
import locale

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'axes.titlesize': 15})
rcParams.update({'axes.titleweight': 'bold'})
rcParams.update({'axes.labelweight': 'bold'})
rcParams.update({'axes.linewidth': 0.8})
rcParams.update({'axes.grid': False})

BLUE = '#3299e3'
BLACK= 'black'
RED = 'red'
PURPLE = '#be78e3'

SET_TITLES = True
DAYS = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
df = None

#######################
# AUXILIARY FUNCTIONS #
#######################

# auxiliary functions to determine the type of sensor for each entry
is_state = lambda x : pd.notna(x['state']) 
is_various = lambda x : pd.notna(x['temperature']) & pd.isna(x['description'])
is_door = lambda x : pd.notna(x['contact'])
is_movement = lambda x : pd.notna(x['illuminance'])
is_meteo = lambda x : pd.notna(x['windspeed'])
is_feedback = lambda x : pd.notna(x['feedback'])

def get_type(x):
    if is_state(x):
        return 'system'
    if is_meteo(x):
        return 'meteo'
    if is_various(x):
        return 'various'
    if is_door(x):
        return 'door'
    if is_movement(x):
        return 'movement'
    if is_feedback(x):
        return 'feedback'
    return 'other'


#########################
# READING FILES & SETUP #
#########################

def setup(datasetdir, title):
    global df, SET_TITLES
    SET_TITLES = title

    # list with files to consider
    files = ['sgh0201a8c87da4.csv', 'sgh0201a17a7a16.csv', 'sgh0201b9b7d045.csv', 'sgh0201e9248493.csv', 'sgh0201f6cb55ed.csv', 'sgh02015d5c61cc.csv', 'sgh02018fe9be2c.csv', 'sgh02019d93db3f.csv', 'sgh020102d29c86.csv', 'sgh020114a6a800.csv', 'sgh020125bce03a.csv', 'sgh020149c615c5.csv', 'sgh020177a7a91d.csv']

    # appending data from all files
    df_list = []
    for fi in files:
        file_path = os.path.join(datasetdir, fi)
        if not os.path.exists(file_path):
            raise FileNotFoundError("Path \'{0}\' does not contain the dataset files.".format(datasetdir))

        dff = pd.read_csv(file_path, parse_dates=['date'])
        dff['tenant'] = fi
        df_list.append(dff)
    df = pd.concat(df_list, verify_integrity=True, ignore_index=True)

    # transforming strings in JSON objects
    df['info'] = df['info'].apply(lambda x :json.loads(x))

    # removing column 'tenant' and place its values in the info JSON object
    t = df.pop('tenant')
    for i in range(len(df)):
        df['info'][i]['tenant']= t[i]

    # transforming JSON object into various columns
    df = pd.concat([df.drop(['info'], axis=1), pd.json_normalize(df['info'])], axis=1)

    # set index to date
    df.set_index('date', inplace=True)

    # only values after 3rd January 2019 were considered
    df = df[df.index > '2019-03-01']

    # adding a new column with the type of sensor for each entry
    df['sensor'] = df.apply(lambda x: get_type(x), axis=1)


################################################################
#                       CREATE CHARTS                          #
################################################################
# - relative_amount_data_by_month                              #
# - average_temperature_by_month                               #
# - average_humidity_by_month                                  #
# - average_temperature_by_week                                #
# - average_humidity_by_week                                   #
# - relative_occupancy_by_hour                                 #
# - relative_occupancy_by_hour_week                            #
# - average_temperature_by_hour (w/wo std)                     #    
# - average_temperature_by_hour_with_occupancy (w/wo std)      #                   
# - average_temperature_by_hour_week (w/wo std)                #         
# - average_temperature_by_hour_week_with_occupancy (w/wo std) #
################################################################

def relative_amount_data_by_month():
    # resample data by day, counting the number of entries
    data_count_day = df.resample('d', label='left')['sensor'].count()

    # get average of number of regists per day in each month
    avg_data_month = data_count_day.resample('m', label='right').mean()

    # get highest value
    max_avg_data_month = max(avg_data_month)

    # calculate data missing in relation to the highest value
    missing = 1 - avg_data_month/max_avg_data_month

    # create plot and assign labels
    ax = missing.plot.bar(
        label='relative amount of missing data', 
        xlabel='Months', 
        ylabel='Relative Data Missing', 
        title='Relative Data Missing by Month' if SET_TITLES else '', 
        linewidth=2, 
        width=0.7, 
        edgecolor='black', 
        color=BLUE
        )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    locale.setlocale(locale.LC_ALL, 'en_GB')
    x_labels = missing.index.strftime('%b %y')
    locale.resetlocale()    
    ax.set_xticklabels(x_labels)
    ax.set_axisbelow(True)
    ax.legend()
    plt.grid(True, which='both', axis='y', color='gray', linestyle='-.')
    return ax

def average_temperature_by_month():
    # resample data by month, averaging the temperature values
    res_month = df[is_various].resample('m', label='left')[['temperature']].mean()

    # plot the temperature values, calculating the mean for each month
    avg_month = res_month.groupby(res_month.index.month).mean()
    ax = avg_month['temperature'].plot( 
        xticks=avg_month.index, 
        label='temperature value', 
        ylabel='Temperature (ºC)', 
        xlabel='Months', 
        title='Average Temperature by Month' if SET_TITLES else '',
        marker='o', 
        markersize=7, 
        markeredgecolor=BLACK, 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=RED, 
        color='black', 
        linewidth=2 
    )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    x_labels = pd.to_datetime(avg_month.index, format='%m').month_name().str.slice(stop=3)
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax
    
def average_humidity_by_month():
    # resample data by month, averaging the humidity values
    res_month = df[is_various].resample('m', label='left')[['humidity']].mean()

    # plot the humidity values, calculating the mean for each month
    avg_month = res_month.groupby(res_month.index.month).mean()
    ax = avg_month['humidity'].plot(
        xticks=avg_month.index, 
        label='humidity value', 
        ylabel='Relative Humidity (%)', 
        xlabel='Months', 
        title='Average Humidity by Month' if SET_TITLES else '',
        marker='o', 
        markersize=7, 
        markeredgecolor=BLACK, 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=BLUE, 
        color='black', 
        linewidth=2
    )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    x_labels = pd.to_datetime(avg_month.index, format='%m').month_name().str.slice(stop=3)
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax

def average_temperature_by_week():
    # resample data by week, averaging the temperature values
    res_week = df[is_various].resample('w', label='left')[['temperature']].mean()

    # plot the temperature values, joining the weeks calculating their mean
    avg_week = res_week.groupby(pd.Index(res_week.index.isocalendar().week, dtype=np.int64)).mean()    
    ax = avg_week['temperature'].plot(
        label='temperature value', 
        xticks=avg_week.index[::5], 
        ylabel='Temperature (ºC)', 
        xlabel='Weeks', 
        title='Average Temperature by Week' if SET_TITLES else '',
        marker='o', 
        markersize=7, 
        markeredgecolor='black', 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=RED, 
        color=BLACK, 
        linewidth=2
    )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax

def average_humidity_by_week():
    # resample data by week, averaging the temperature and humidity values
    res_week = df[is_various].resample('w', label='left')[['humidity']].mean()

    # plot the humidity values, joining the weeks calculating their mean
    avg_week = res_week.groupby(pd.Index(res_week.index.isocalendar().week, dtype=np.int64)).mean()
    ax = avg_week['humidity'].plot(
        label='humidity value', 
        xticks=avg_week.index[::5], 
        ylabel='Relative Humidity (%)', 
        xlabel='Weeks', 
        title='Average Humidity by Week' if SET_TITLES else '',
        marker='o', 
        markersize=7, 
        markeredgecolor=BLACK, 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=BLUE, 
        color=BLACK, 
        linewidth=2
    )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax

def relative_occupancy_by_hour():
    # get all the entries with movement detected resampled per hour
    df_mov = df[df['occupancy'] == True].resample('h')

    # get number of different tenants where movement was detected per hour
    mov_sum = df_mov['tenant'].nunique()

    # sum those values per hour
    people_home_per_hour = mov_sum.groupby(mov_sum.index.hour).sum()

    # divide the obtained values by the maximum number found
    people_home_hour_perc = people_home_per_hour/max(people_home_per_hour)

    # create plot
    ax = people_home_hour_perc.plot(
        label='relative number of occupancy entries', 
        xticks=people_home_per_hour.index[::2],
        title='Relative Occupancy by Hour' if SET_TITLES else '', 
        ylabel='Relative Presence', 
        xlabel='Hours', 
        marker='o', 
        markersize=7, 
        markeredgecolor=BLACK, 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=PURPLE, 
        color=BLACK, 
        linewidth=2,
        figsize=(7,4)
    )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    x_labels = [ f'{h:02d}:00' for h in people_home_per_hour.index[::2] ]
    ax.set_xticklabels(x_labels)
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax

def relative_occupancy_by_hour_week():

    # get all the entries with movement detected resampled per hour
    df_mov = df[df['occupancy'] == True].resample('h') 

    # get number of different tenants where movement was detected per hour
    mov_sum = df_mov['tenant'].nunique()

    # group data by day of the week and hour in the respective day
    presenca_hour_week = mov_sum.groupby([mov_sum.index.dayofweek, mov_sum.index.hour] ).sum()

    # normalize values
    presenca_hour_week = presenca_hour_week/ max(presenca_hour_week)

    # plot the marks with the colour correspondent to the occupance/presence
    ax = presenca_hour_week.plot(
        label='relative number of occupancy entries', 
        ylabel='Relative Occupancy', 
        xlabel='Days of the Week, Hours', 
        marker='o', 
        xticks= range(len(presenca_hour_week.index)+1)[::12],
        markersize=5, 
        markeredgecolor=BLACK, 
        markeredgewidth=1, 
        linestyle='-', 
        markerfacecolor=PURPLE, 
        color=BLACK, 
        linewidth=2, 
        figsize=(9,4)
        )
    plt.title('Average Occupancy by Hours in a Week' if SET_TITLES else '')

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    xlabels = [ DAYS[wday][:3] +', \n' + f'{hour:02d}' + ':00' for (wday, hour) in presenca_hour_week.index[::12] ]
    xlabels.append( xlabels[0] )
    ax.xaxis.set_ticklabels( xlabels )
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    return ax

def average_temperature_by_hour(with_std=False):
    # resample data by hour, averaging the values
    df_var = df[is_various].resample('h').mean()

    # group values by their mean and standard deviation per hour
    df_var_group_by_hour_day = df_var.groupby(df_var.index.hour).agg(['mean', 'std'])

    # plot the temperature values
    temp_mean = df_var_group_by_hour_day['temperature']['mean']
    ax = temp_mean.plot(
        label='temperature value', 
        xticks=df_var_group_by_hour_day.index[::2], 
        ylabel='Temperature (ºC)', 
        xlabel='Hours',
        title= 'Average Temperature by Hour' if SET_TITLES else '',
        marker='o', 
        markersize=7, 
        markeredgecolor=BLACK, 
        markeredgewidth=2, 
        linestyle='--', 
        markerfacecolor=RED, 
        color=BLACK, 
        linewidth=2,
        figsize=(7,4)
        )

    # take care of axis labels and legend
    x_labels = [ f'{h:02d}:00' for h in df_var_group_by_hour_day.index[::2] ]
    ax.set_xticklabels(x_labels)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.legend()
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')

    if (not with_std):
        return ax

    # --- show the standard deviation range shadow ---
    # saving the averages and the standard deviation data
    temp_std = df_var_group_by_hour_day['temperature']['std']

    # add standar deviation range shadow and update legend and title
    ax.fill_between(
        label='standard deviation range',
        x=range(0,24), 
        y1=temp_mean-temp_std, 
        y2 = temp_mean+temp_std, 
        alpha=.15, 
        color=BLUE
    )
    plt.title('Average Temperature by Hour with Standard Deviation Range' if SET_TITLES else '', fontdict= {'fontsize': 11})
    ax.legend()
    return ax

def average_temperature_by_hour_with_occupancy(with_std=False):
    # ---- deal with occupance data ----
    # get all the entries with movement detected resampled per hour
    df_mov = df[df['occupancy'] == True].resample('h')

    # get number of different tenants where movement was detected per hour
    mov_sum = df_mov['tenant'].nunique()

    # sum those values per hour
    people_home_per_hour = mov_sum.groupby(mov_sum.index.hour).sum()

    # divide the obtained values by the maximum number found
    people_home_hour_perc = people_home_per_hour/max(people_home_per_hour)

    # create list with percentage values
    perc_values = people_home_hour_perc.values

    # ---- deal with temperature data ----
    # resample data by hour, averaging the values
    df_var = df[is_various].resample('h').mean()

    # group values by their mean and standard deviation per hour
    df_var_group_by_hour_day = df_var.groupby(df_var.index.hour).agg(['mean', 'std'])

    temp_means = df_var_group_by_hour_day['temperature']['mean']

    # plot the temperature values - only a line
    ax = temp_means.plot(
        xticks=df_var_group_by_hour_day.index[::2], 
        ylabel='Temperature (ºC)', 
        xlabel='Hours',
        linestyle='--', 
        color=BLACK, 
        linewidth=2, 
        zorder=1,
        figsize=(9,4)
        )

    # plot the marks with the colour correspondent to the occupance/presence
    ax1 = plt.scatter( 
        x = temp_means.index, 
        y=temp_means, 
        c = perc_values, 
        cmap='YlGnBu', 
        s=70, 
        marker='s', 
        edgecolors='black', 
        linewidths=1, 
        zorder=2
        )
    
    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    x_labels = [ f'{h:02d}:00' for h in df_var_group_by_hour_day.index[::2] ]
    ax.set_xticklabels(x_labels)
    legend_elements = [ 
        Line2D(
            [0], 
            [0], 
            label='temperature value with occupancy information', 
            lw=2, 
            color=BLACK, 
            marker='s', 
            markeredgecolor=BLACK, 
            markerfacecolor=BLUE, 
            markersize=8.3, 
            markeredgewidth=1
        ) ]
    ax.legend( handles=legend_elements)

    # take care of the colour legend for the presence
    plt.colorbar( ax1, ax=ax, label='Relative Presence Scale')

    plt.title('Average Temperature by Hour with Occupancy Information' if SET_TITLES else '', fontdict= {'fontsize': 11})
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')

    if not with_std:
        return ax

    # --- show the standard deviation range shadow ---
    # save standard deviation data
    temp_std = df_var_group_by_hour_day['temperature']['std']

    # add standard deviation range shadow and update legend and title
    plt.fill_between(x=range(0,24), y1=temp_means-temp_std, y2 = temp_means+temp_std, alpha=.1, color=BLUE)
    plt.title('Average Temperature by Hour with Occupancy Information and Standard Deviation Range' if SET_TITLES else '', fontdict= {'fontsize': 9})
    legend_elements += [ Patch(facecolor=BLUE, label='standard deviation range', alpha=.15)]
    ax.legend( handles = legend_elements )
    return ax
    
def average_temperature_by_hour_week(with_std=False):
    # resample data by hour, averaging the values
    df_var = df[is_various].resample('h').mean()

    # group data by week and hour of the day
    df_var_group = df_var.groupby([df_var.index.dayofweek, df_var.index.hour]).agg(['mean', 'std'])

    # plot the temperature values
    temp_mean = df_var_group['temperature']['mean']
    ax = temp_mean.plot(
        label='temperature value', 
        ylabel='Temperature (ºC)', 
        xlabel='Days of the Week, Hours', 
        marker='o', 
        markersize=5, 
        markeredgecolor=BLACK, 
        markeredgewidth=1, 
        linestyle='-', 
        markerfacecolor=RED, 
        color=BLACK, 
        linewidth=2,
        figsize=(9,4)
        )

    # take care of axis labels and legend
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    plt.title('Average Temperature by Hours in a Week')
    ax.set_xticks( range(len(df_var_group.index)+1)[::12] )
    xlabels  = [ DAYS[wday][:3] +', \n' + f'{hour:02d}:00' for (wday, hour) in df_var_group.index[::12] ]
    xlabels += [ xlabels[0] ]
    ax.set_xticklabels(xlabels)
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')
    ax.legend()

    if (not with_std):
        return ax

    # --- show the standard deviation range shadow ---
    # save standard deviation data
    temp_std = df_var_group['temperature']['std']

    # add standar deviation range shadow and update legend and title
    plt.fill_between(label='standard deviation range', x=range(len(temp_mean)), y1=temp_mean-temp_std, y2 = temp_mean+temp_std, alpha=.15, color=BLUE)
    plt.title('Average Temperature by Hours in a Week with Standard Deviation Range', fontdict= {'fontsize': 10})
    ax.legend()
    return ax

def average_temperature_by_hour_week_with_occupancy(with_std=False):
    # ---- deal with occupance data ----
    # get all the entries with movement detected resampled per hour
    df_mov = df[df['occupancy'] == True].resample('h')

    # get number of different tenants where movement was detected per hour
    mov_sum = df_mov['tenant'].nunique()
    
    # group data by day of the week and hour in the respective day and sum
    presenca_hour_week = mov_sum.groupby([mov_sum.index.dayofweek, mov_sum.index.hour] ).sum()

    # divide the obtained values by the maximum number found
    presenca_hour_week = presenca_hour_week/ max(presenca_hour_week)

    # create list with percentage values
    perc_values = presenca_hour_week.values

    # ---- deal with temperature data ----
    # resample data by hour, averaging the values
    df_var = df[is_various].resample('h').mean()

    # group values by their mean and standard deviation per hour
    df_var_group = df_var.groupby([df_var.index.dayofweek, df_var.index.hour] ).agg(['mean', 'std'])

    # save average temperature data
    temp_means = df_var_group['temperature']['mean']

    # plot the temperature values - only a line
    ax = temp_means.plot(
        ylabel='Temperature (ºC)', 
        xlabel='Days of the Week, Hours', 
        xticks= range(len(presenca_hour_week.index)+1)[::12],
        linestyle='--', 
        color=BLACK, 
        linewidth=2, 
        zorder=1,
        figsize=(10,4)
        )

    # plot the marks with the colour correspondent to the occupance/presence
    ax1 = plt.scatter( 
        x = range( len(temp_means) ), 
        y=temp_means, 
        c = perc_values, 
        cmap='YlGnBu', 
        s=70, 
        marker='s', 
        edgecolors=BLACK, 
        linewidths=1, 
        zorder=2
        )

    # take care of axis labels and legend
    xlabels = [ DAYS[wday][:3] +', \n' + f'{hour:02d}' + ':00' for (wday, hour) in presenca_hour_week.index[::12] ]
    xlabels.append( xlabels[0] )
    ax.xaxis.set_ticklabels( xlabels )
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    plt.title('Average Temperature by Hours in a Week with Occupancy Information' if SET_TITLES else '', fontdict= {'fontsize': 11})
    legend_elements = [ 
        Line2D(
            [0], 
            [0], 
            label='Temperature Value', 
            lw=2, 
            color=BLACK, 
            marker='s', 
            markeredgecolor=BLACK, 
            markerfacecolor=BLUE, 
            markersize=8.3, 
            markeredgewidth=1
        ) ]
    ax.legend( handles=legend_elements)

    # take care of the colour legend for the presence
    plt.colorbar( ax1, ax=ax, label='Relative Presence Scale')
    plt.grid(True, which='both', axis='both', color='gray', linestyle='-.')

    
    if not with_std:
        return ax

    # --- show the standard deviation range shadow ---
    # save standard deviation data
    temp_std = df_var_group['temperature']['std']

    # add standard deviation range shadow and update legend and title
    plt.fill_between(x=range(len(temp_means)), y1=temp_means-temp_std, y2 = temp_means+temp_std, alpha=.1)
    plt.title(
        'Average Temperature by Hours in a Week with Occupancy Information and Standard Deviation Range' if SET_TITLES else '', 
        fontdict= {'fontsize': 10}
    )
    legend_elements += [ Patch(facecolor=BLUE, label='Standard Deviation Range', alpha=.15)]
    ax.legend( handles = legend_elements )
    return ax
