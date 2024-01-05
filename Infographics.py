# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:44:56 2023

@author: bc975789
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def readFile(filename,yr):
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

co2_file='Data/co2.csv'
ele_heat='Data/ele_heat.csv'
manuf='Data/manuf.csv'
oth_sectors='Data/oth_sectors.csv'
transport='Data/transport.csv'
building='Data/building.csv'
renew_cons='Data/renew_cons.csv'
forest='Data/forest_land.csv'
hydro='Data/hydro_electric.csv'
ogc='Data/oil_gas_coal.csv'
renew='Data/renew.csv'
nucl='Data/nuclear.csv'
renew_prod=pd.read_csv('Data/modern-renewable-prod.csv')


cntry_list=['China']
yr_co2 = [str(year) for year in range(1960, 2011)] + [str(year)
                                                  for year in range(2021, 2023)]
yr_pie=[str(year) for year in range(1960, 2014)] + [str(year)
                                                  for year in range(2015, 2023)]
yr_null=[]

co2=readFile(co2_file,yr_co2)
ele_heat=readFile(ele_heat,yr_pie)
manuf=readFile(manuf,yr_pie)
oth_sectors=readFile(oth_sectors,yr_pie)
transport=readFile(transport,yr_pie)
build=readFile(building,yr_pie)
forest=readFile(forest, yr_co2)
hydro=readFile(hydro, yr_co2)
ogc=readFile(ogc, yr_co2)
renew=readFile(renew, yr_co2)
nucl=readFile(nucl, yr_co2)
renew_cons=readFile(renew_cons, yr_co2)


build_df=build[(build['Country Name'].isin(cntry_list))]
manuf_df=manuf[(manuf['Country Name'].isin(cntry_list))]
oth_sectors_df=oth_sectors[(oth_sectors['Country Name'].isin(cntry_list))]
transport_df=transport[(transport['Country Name'].isin(cntry_list))]
ele_heat_df=ele_heat[(ele_heat['Country Name'].isin(cntry_list))]
renew_df=renew_cons[(renew_cons['Country Name'].isin(cntry_list))]

colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e74c3c', '#2ecc71']



fig=plt.figure(figsize=(18, 18),facecolor='#F0F0F0')
plt.suptitle('CO2 Emission, Sources and Energy Analysis in China',fontsize=28,y=0.94,fontweight='bold')


co2_china=co2[co2['Country Name']=='China']
co2_china_yr=co2_china.iloc[:,1:]
co2_china_series=co2_china_yr.squeeze()

plt.subplot(3,2,1)
plt.bar(list(co2_china_yr.columns),co2_china_yr.unstack().values.tolist(),color=colors[5])
plt.plot(co2_china_series,marker='o',color='r',linewidth=2)
first_value = co2_china_yr.unstack().values.tolist()[0]
last_value = co2_china_yr.unstack().values.tolist()[-1]
plt.text(co2_china_yr.columns[0], first_value, f'{first_value:.2f}', ha='center', va='bottom', color='black', fontsize=12)
plt.text(co2_china_yr.columns[-1], last_value, f'{last_value:.2f}', ha='center', va='bottom', color='black', fontsize=12)
plt.title('CO2 emission in the China (2011-2020)',fontweight='bold',fontsize=16)
plt.ylabel('CO2 emissions(kt)',fontsize=13)
plt.xlabel('Year',fontsize=13)
plt.ylim(9000000,11080000)
plt.legend()


dfs = [build_df,manuf_df, oth_sectors_df, transport_df, ele_heat_df]
china_data = [df.loc[df['Country Name'] == 'China', '2014'].values[0] 
              for df in dfs]
sources1 = ['residential buildings and\ncommercial and public services', 
            'manufacturing industries\nand construction', 
            'Other Sectors', 'Transport', 'Electricity and\nHeat production']
plt.subplot(3,2,2)
plt.pie(china_data, autopct='%1.1f%%', 
        pctdistance=0.8,startangle=90, explode=(0,0,0,0,0.05),colors=colors[3:],wedgeprops=dict(width=0.5))
plt.title('China\'s CO2 Emission sources Distribution (2014)',fontweight='bold',fontsize=16)
plt.legend(labels=sources1,loc='best',bbox_to_anchor=(0.8, 0.2, 0.9, 0.7))


pie_dfs=[hydro,renew,ogc,nucl]
china_pie=[df.loc[df['Country Name'] == 'China', '2014'].values[0] for df in pie_dfs]
sources=['Hydro','Renewable Sources','Oil, Gas & Coal','Nuclear']
plt.subplot(3,2,3)
plt.pie(china_pie, autopct='%1.1f%%', startangle=180,
        pctdistance=0.8,explode=(0.05,0.1,0,0),colors=colors[3:],wedgeprops=dict(width=0.5))
plt.title('Electricity Production Distribution in China (2014)',fontweight='bold',fontsize=16)
plt.legend(labels=sources,loc='best', bbox_to_anchor=(0, 0, 0, 0.5))


renew_df.set_index('Country Name', inplace=True)
plt.subplot(3,2,4)
plt.grid()
for country in renew_df.index:
    plt.plot(renew_df.columns, renew_df.loc[country], label=country, marker='o',color='r')
    for i, (year, value) in enumerate(zip(renew_df.columns, renew_df.loc[country])):
        if i == 0 or i == len(renew_df.columns) - 1:
            plt.text(year, value + 0.1, f'{value:.2f}%', ha='center', va='bottom', color='black', fontsize=12, fontweight='bold')
        else:
            plt.text(year, value +0.1, f'{value:.2f}%', ha='center', va='bottom', color='black', fontsize=10)
plt.title('Renewable energy consumption (% of total final energy consumption)',
          fontweight='bold',fontsize=15)
plt.xlabel('Year',fontsize=13)
plt.ylabel('Renewable Enegry Consumption(%)',fontsize=13)
plt.ylim(11,15.5,0.5)
plt.legend(loc='upper center')



selected_data = renew_prod[(renew_prod['Entity'] == 'China') & (renew_prod['Year'] == 2022)]
bar_data = selected_data[['Electricity from wind - TWh', 
                         'Electricity from hydro - TWh', 
                          'Electricity from solar - TWh', 
                          'Other renewables including bioenergy - TWh']]
#bar_data = bar_data.transpose()
bar_values=bar_data.unstack().values.tolist()
#colors=['blue', 'green', 'yellow', 'orange']
renew_sources=['Wind','Hydro','Solar','Other Sources\nincluding Bioenergy']
plt.subplot(3,2,5)
bars=plt.barh(renew_sources,bar_values,color=colors[3:])
#bar_data.plot(kind='barh', legend=False)
plt.title('Renewable Energy Sources in China 2022',fontweight='bold',fontsize=16)
plt.xlabel('Electricity (TWh)',fontsize=13)
plt.ylabel('Energy Sources',fontsize=13)
plt.xlim(0,1500)
for bar, value in zip(bars, bar_values):
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.2f}', 
             va='center', ha='left', fontsize=12,fontweight='bold')


text=""" 
This infographics explores the CO2 emission and its major sources in the highest
Co2 emitting country China, over several years. The first plot shows the drastic 
increase in China’s co2 emission from the numeric of 9 million kilotons to nearly 
11 million kilotons. Looking into the major sources of co2 emission, 2014 data 
shows that more than half (ie., 52.3%) of the emission is from the electricity 
and heat production and the second pie chart show its reason because 75% of the 
electricity in China (2014) is produced from oil, gas and coal which contributes 
to the high emission of co2. But it also shows how China looks into tackling this 
issue by adopting renewable energy sources including hydroelectricity which 
contributes to 4.1% and 18.6% of energy production respectively. Thus, China shows
a sustainable move although at a slower rate in increasing the renewable energy 
consumption from 11.34% to 14.81% of the total energy consumption from 2011 to 
2020 and according to 2022 the major renewable energy sources used by China are 
Hydroelectricity followed by wind energy."""

name=""" Name : Sandra Binu
      Student ID : 22029960 """
    
plt.text(0.73, 0.25, text, ha='center', va='center', 
         transform=plt.gcf().transFigure, fontsize=14, 
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.text(0.73, 0.125, name , ha='center', va='center', 
         transform=plt.gcf().transFigure, fontsize=14, 
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
plt.savefig('22029960.png', dpi=300, bbox_inches='tight')
#plt.tight_layout()
#fig.set_facecolor('#F0F0F0')
plt.show()


