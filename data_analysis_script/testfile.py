import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from oura import OuraClient, OuraOAuth2Client


def get_oura_sleep_data():
    ourac = OuraClient( 'XX','XX','XX')
    sleep_data = ourac.sleep_summary(start='2022-08-01', end='2022-11-01')
    processed_sleep_data = []
    for s in sleep_data['sleep']:
        temp = {}
        temp["sleep_duration"] = int(s['duration']) / 3600
        temp["heart_rate"] = s['hr_lowest']
        temp['efficiency'] = s['score_efficiency']
        temp['latency'] = s['score_latency']
        temp['rem_duration'] = s['rem'] / 3600
        temp['deep_duration'] = s['deep'] / 3600
        temp['light_duration'] = s['light'] / 3600
        temp['wake_up_count'] = s['wake_up_count']
        temp['sleep_quality_score'] = s['score']
        processed_sleep_data.append(temp)
    return processed_sleep_data

def get_applewatch_sleep_data():
    # create element tree object
    tree = ET.parse('export.xml')
    # for every health record, extract the attributes into a dictionary (columns). Then create a list (rows).
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    # create DataFrame from a list (rows) of dictionaries (columns)
    data = pd.DataFrame(record_list)
    # proper type to dates
    for col in ['creationDate', 'startDate', 'endDate']:
        data[col] = pd.to_datetime(data[col])
    # value is numeric, NaN if fails
    data['value'] = pd.to_numeric(data['value'], errors='coerce')
    # some records do not measure anything, just count occurences
    # filling with 1.0 (= one time) makes it easier to aggregate
    data['value'] = data['value'].fillna(1.0)
    # shorter observation names: use vectorized replace function
    data['type'] = data['type'].str.replace('HKQuantityTypeIdentifier', '')
    data['type'] = data['type'].str.replace('HKCategoryTypeIdentifier', '')
    # pivot and resample
    pivot_df = data.pivot_table(index='endDate', columns='type', values='value')
    df = pivot_df.resample('D').agg({'HeartRate': np.min,
                                     'OxygenSaturation': np.mean,
                                     'RespiratoryRate': np.mean,
                                     'StepCount': np.mean,
                                     'VO2Max': np.mean,
                                     'HKDataTypeSleepDurationGoal': np.mean,
                                     'HeartRateVariabilitySDNN': np.mean,
                                     }
                                    )
    df.loc[(df.index.month == 1) | (df.index.month == 2) | (df.index.month == 3) | (df.index.month == 4) | (
                df.index.month == 5) | (df.index.month == 6) | (df.index.month == 7) | (df.index.month == 8) | (
                       df.index.month == 9) | (df.index.month == 10) | (df.index.month == 12) | (
                       df.index.year == 2019) | (df.index.year == 2020) | (df.index.year == 2021), 'HeartRate'] = 0
    df.loc[(df.index.month == 1) | (df.index.month == 2) | (df.index.month == 3) | (df.index.month == 4) | (
                df.index.month == 5) | (df.index.month == 6) | (df.index.month == 7) | (df.index.month == 8) | (
                       df.index.month == 9) | (df.index.month == 10) | (df.index.month == 12) | (
                       df.index.year == 2019) | (df.index.year == 2020) | (
                       df.index.year == 2021), 'OxygenSaturation'] = 0
    df.loc[(df.index.month == 1) | (df.index.month == 2) | (df.index.month == 3) | (df.index.month == 4) | (
                df.index.month == 5) | (df.index.month == 6) | (df.index.month == 7) | (df.index.month == 8) | (
                       df.index.month == 9) | (df.index.month == 10) | (df.index.month == 12) | (
                       df.index.year == 2019) | (df.index.year == 2020) | (
                       df.index.year == 2021), 'RespiratoryRate'] = 0
    df.loc[(df.index.month == 1) | (df.index.month == 2) | (df.index.month == 3) | (df.index.month == 4) | (
                df.index.month == 5) | (df.index.month == 6) | (df.index.month == 7) | (df.index.month == 8) | (
                       df.index.month == 9) | (df.index.month == 10) | (df.index.month == 12) | (
                       df.index.year == 2019) | (df.index.year == 2020) | (
                       df.index.year == 2021), 'HKDataTypeSleepDurationGoal'] = 0
    df.loc[(df.index.month == 1) | (df.index.month == 2) | (df.index.month == 3) | (df.index.month == 4) | (
                df.index.month == 5) | (df.index.month == 6) | (df.index.month == 7) | (df.index.month == 8) | (
                       df.index.month == 9) | (df.index.month == 10) | (df.index.month == 12) | (
                       df.index.year == 2019) | (df.index.year == 2020) | (
                       df.index.year == 2021), 'HeartRateVariabilitySDNN'] = 0
    return df


def create_heatmap(df,image_name):
    cm = df.corr()
    # heatmap
    # fig = plt.figure(figsize=(8, 6))
    sns.set(rc={'figure.figsize': (10, 10)})
    snss = sns.heatmap(cm, annot=True, fmt=".2f", vmin=-1.0, vmax=+1.0, cmap='Spectral')
    fig = snss.get_figure()
    fig.savefig(image_name)


applewatch_sleepdata = get_applewatch_sleep_data()
ouraring_sleepdata = get_oura_sleep_data()
z = pd.DataFrame(ouraring_sleepdata)

create_heatmap(z,'testheatmap.png')
