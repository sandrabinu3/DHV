# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:44:56 2023

@author: bc975789
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def readFile(filename, yr):
    """ function to read and clean a World Bank files

    Args:
        filename (string): filepath to the World Bank file
        yr (list): list of years to be dropped from the dataframe

    Returns:
        final_df (dataframe): clean dataframe with selected years
    """
    df = pd.read_csv(filename, skiprows=2, header=1)  # read the data
    # dropping the unwanted columns
    ref_df = df.drop(df.columns[1:4], axis=1)
    ref_df = ref_df.drop(df.columns[-1:], axis=1)
    # filtering the years
    final_df = ref_df.drop(columns=yr)
    # reseting the index
    final_df = final_df.reset_index(drop=True)
    return final_df


def Infographic(country, text, name):
    """ Function to create the infographics

    Args:
        country (string): the country being analysed
        text (string): analysed report
        name (string): name and id
    """
    #defining colours list
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12',
          '#9b59b6', '#1abc9c', '#e74c3c', '#2ecc71']
    #initializing the figure
    fig = plt.figure(figsize=(18, 18), facecolor='#F0F0F0')
    plt.suptitle('CO2 Emission, Sources and Energy Analysis in China',
                 fontsize=28, y=0.94, fontweight='bold')

    co2_china = co2[co2['Country Name'] == country]
    co2_china_yr = co2_china.iloc[:, 1:]
    co2_china_series = co2_china_yr.squeeze()

    # barchart
    plt.subplot(3, 2, 1)
    plt.bar(list(co2_china_yr.columns),
            co2_china_yr.unstack().values.tolist(), color=colors[5])
    plt.plot(co2_china_series, marker='o', color='r', linewidth=2)
    first_value = co2_china_yr.unstack().values.tolist()[0]
    last_value = co2_china_yr.unstack().values.tolist()[-1]
    plt.text(co2_china_yr.columns[0], first_value,
             f'{first_value:.2f}', ha='center', va='bottom', color='black', fontsize=12)
    plt.text(co2_china_yr.columns[-1], last_value,
             f'{last_value:.2f}', ha='center', va='bottom', color='black', fontsize=12)
    plt.title('CO2 emission in China (2011-2020)',
              fontweight='bold', fontsize=16)
    plt.ylabel('CO2 emissions(kt)', fontsize=13)
    plt.xlabel('Year', fontsize=13)
    plt.ylim(9000000, 11080000)
    plt.legend()

    #filtering the desired country from dfs
    build_df = build[(build['Country Name'] == country)]
    manuf_df = manuf[(manuf['Country Name'] == country)]
    oth_sectors_df = oth_sectors[(oth_sectors['Country Name'] == country)]
    transport_df = transport[(transport['Country Name'] == country)]
    ele_heat_df = ele_heat[(ele_heat['Country Name'] == country)]
    renew_df = renew_cons[(renew_cons['Country Name'] == country)]
    dfs = [build_df, manuf_df, oth_sectors_df, transport_df, ele_heat_df]
    china_data = [df.loc[df['Country Name'] == country, '2014'].values[0]
                  for df in dfs]
    sources1 = ['Residential buildings and\nCommercial and Public services',
                'Manufacturing industries\nand Construction',
                'Other Sectors', 'Transport', 'Electricity and\nHeat production']

    # Pieplot1
    plt.subplot(3, 2, 2)
    plt.pie(china_data, autopct='%1.1f%%',
            pctdistance=0.8, startangle=90, explode=(0, 0, 0, 0, 0.03), 
            colors=colors[3:], wedgeprops=dict(width=0.5))
    plt.title('China\'s CO2 Emission sources Distribution (2014)',
              fontweight='bold', fontsize=16)
    plt.legend(labels=sources1, loc='best', bbox_to_anchor=(
        0.8, 0.2, 0.9, 0.7), borderpad=1.5, labelspacing=1.5)

    # pieplot2
    pie_dfs = [hydro, renew, ogc, nucl]
    china_pie = [df.loc[df['Country Name'] == 'China', '2014'].values[0]
                 for df in pie_dfs]
    sources = ['Hydro', 'Renewable Sources', 'Oil, Gas & Coal', 'Nuclear']
    plt.subplot(3, 2, 3)
    plt.pie(china_pie, autopct='%1.1f%%', startangle=180,
            pctdistance=0.8, explode=(0.05, 0.1, 0, 0), colors=colors[3:], 
            wedgeprops=dict(width=0.5))
    plt.title('Electricity Production Distribution in China (2014)',
              fontweight='bold', fontsize=16)
    plt.legend(labels=sources, loc='best', bbox_to_anchor=(
        0, 0, 0, 0.7), borderpad=1.5, labelspacing=1.5)

    renew_df.set_index('Country Name', inplace=True)

    # linechart
    plt.subplot(3, 2, 4)
    plt.grid(color=colors[5])
    for country in renew_df.index:
        plt.plot(renew_df.columns,
                 renew_df.loc[country], label=country, marker='o', color='r')
        for i, (year, value) in enumerate(zip(renew_df.columns, renew_df.loc[country])):
            if i == 0 or i == len(renew_df.columns) - 1:
                plt.text(year, value + 0.1, f'{value:.2f}%', ha='center',
                         va='bottom', color='black', fontsize=12, fontweight='bold')
            else:
                plt.text(year, value + 0.1, f'{value:.2f}%',
                         ha='center', va='bottom', color='black', fontsize=10)
    plt.title('Renewable energy consumption\n(% of total final energy consumption)',
              fontweight='bold', fontsize=16)
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Renewable Enegry Consumption(%)', fontsize=13)
    plt.ylim(11, 15.5, 0.5)
    plt.legend(loc='upper center')

    # horizontal barchart
    selected_data = renew_prod[(renew_prod['Entity'] == country) & (
        renew_prod['Year'] == 2022)]
    bar_data = selected_data[['Electricity from wind - TWh',
                              'Electricity from hydro - TWh',
                              'Electricity from solar - TWh',
                              'Other renewables including bioenergy - TWh']]
    # bar_data = bar_data.transpose()
    bar_values = bar_data.unstack().values.tolist()
    # colors=['blue', 'green', 'yellow', 'orange']
    renew_sources = ['Wind', 'Hydro', 'Solar',
                     'Other Sources\nincluding Bioenergy']
    plt.subplot(3, 2, 5)
    bars = plt.barh(renew_sources, bar_values, color=colors[3:])
    # bar_data.plot(kind='barh', legend=False)
    plt.title('Renewable Energy Sources in China 2022',
              fontweight='bold', fontsize=16)
    plt.xlabel('Electricity (TWh)', fontsize=13)
    plt.ylabel('Energy Sources', fontsize=13)
    plt.xlim(0, 1500)
    for bar, value in zip(bars, bar_values):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.2f}',
                 va='center', ha='left', fontsize=12, fontweight='bold')

    plt.text(0.73, 0.24, text, ha='center', va='center',
             transform=plt.gcf().transFigure, fontsize=14,
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.text(0.73, 0.113, name, ha='center', va='center',
             transform=plt.gcf().transFigure, fontsize=14,
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.savefig('22029960.png', dpi=300, bbox_inches='tight')
    


co2_file = 'Data/co2.csv'
ele_heat = 'Data/ele_heat.csv'
manuf = 'Data/manuf.csv'
oth_sectors = 'Data/oth_sectors.csv'
transport = 'Data/transport.csv'
building = 'Data/building.csv'
renew_cons = 'Data/renew_cons.csv'
hydro = 'Data/hydro_electric.csv'
ogc = 'Data/oil_gas_coal.csv'
renew = 'Data/renew.csv'
nucl = 'Data/nuclear.csv'
renew_prod = pd.read_csv('Data/modern-renewable-prod.csv')


cntry = 'China'
yr_co2 = [str(year) for year in range(1960, 2011)] + [str(year)
                                                      for year in range(2021, 2023)]
yr_pie = [str(year) for year in range(1960, 2014)] + [str(year)
                                                      for year in range(2015, 2023)]
yr_null = []

co2 = readFile(co2_file, yr_co2)
ele_heat = readFile(ele_heat, yr_pie)
manuf = readFile(manuf, yr_pie)
oth_sectors = readFile(oth_sectors, yr_pie)
transport = readFile(transport, yr_pie)
build = readFile(building, yr_pie)
hydro = readFile(hydro, yr_co2)
ogc = readFile(ogc, yr_co2)
renew = readFile(renew, yr_co2)
nucl = readFile(nucl, yr_co2)
renew_cons = readFile(renew_cons, yr_co2)





text = """ 
This infographic examines CO2 emissions over a number of years and their 
primary sources in China, the nation with the largest CO2 emissions. China's
CO2 emissions increased sharply from 9 million kilotons to around 11 million 
kilotons, as shown in the first plot(2011-2020). When analyzing the primary 
sources of CO2 emissions, data from 2014 indicates that the production of 
electricity and heat accounts for more than half (i.e., 52.3%) of emissions.
The second pie chart shows that in 2014,coal, oil, and gas accounted for 75% 
of China's power generation, which raises CO2 emissions.
However, it also demonstrates how China is approaching this problem by 
utilizing renewable energy sources, such as hydroelectricity, which accounts 
for 18.6% of the country's energy production and 4.1% from other renewable 
sources. China's renewable energy consumption increased from 11.34% to 14.81% 
of total energy consumption between 2011 and 2020, demonstrating a sustained 
trend but at a slower pace. And according to 2022, hydroelectricity and wind 
energy are China's two main sources of renewable energy which uphold China's 
step towards sustainable development."""

name = """ Name : Sandra Binu
      Student ID : 22029960 """

Infographic('China', text, name)
