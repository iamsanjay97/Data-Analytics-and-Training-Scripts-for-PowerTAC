import os
import sys
import pandas as pd
from os import walk
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams["figure.figsize"] = (16,8)
color_book = {'VidyutVanika': 'slateblue', 'VV20': 'slateblue', 'VidyutVanika18': 'yellowgreen', \
              'VV18': 'yellowgreen', 'Sample': 'orchid', 'AgentUDE': 'slategray', 'SPOT': 'orangered', \
              'TUC_TAC': 'gold'}

data_path = '/mnt/d/PowerTAC/PowerTAC2021/experiments/basic/'

dirs  = []

for (dirpath1, dirnames1, filenames1) in walk(data_path):
    dirs.extend(dirnames1)

print(dirs)

for dir in dirs:

    try:
        folder = dir
        data_path_test = data_path + folder + '/'
        storage_path = '/mnt/d/PowerTAC/PowerTAC2021/experiments/basic/results/' + folder + '/'

        if not os.path.isdir(storage_path):
            os.makedirs(storage_path)

        accounting_info_dict = dict()

        files  = []

        for (dirpath, dirnames, filenames) in walk(data_path_test):
            files.extend(filenames)
            
        for file in files:
            
            broker = file[len(file) - file[::-1].index('_'):-4]
            accounting_info_dict.update({broker: pd.read_csv(data_path_test+file, 
                                        names=['Boot', 'Timeslot', 'Income_to_Cost', 'Avg_Market_ShareC', 'Avg_Market_ShareP', 'Tariff_Revenue', 'Wholesale_Cost', 
                                                'Balancing_Cost', 'Distribution_Cost', 'Capacity_Transaction', 'Profit', 'Cash_Position'])})
            print("{} :: \nGames: {}\n".format(broker, accounting_info_dict.get(broker)['Boot'].unique()))

        aggregate_accounting_info_dict = dict()

        for broker in accounting_info_dict.keys():
            
            df = accounting_info_dict.get(broker)
            games = df['Boot'].unique()

            df = df.groupby('Boot')
            avg_income_to_cost = df['Income_to_Cost'].mean()
            avg_marke_shareC = df['Avg_Market_ShareC'].mean()
            avg_marke_shareP = df['Avg_Market_ShareP'].mean()
            total_tariff = df['Tariff_Revenue'].sum()
            total_wholesale = df['Wholesale_Cost'].sum()
            total_balancing = df['Balancing_Cost'].sum()
            total_distribution = df['Distribution_Cost'].sum()
            total_capacity_trans = df['Capacity_Transaction'].sum()
            total_profit = df['Profit'].sum()
            final_cash = df.nth([-1])['Cash_Position']

            aggregate_df = pd.DataFrame(columns = ['Boot', 'Avg_Income_to_Cost', 'Avg_Market_ShareC','Avg_Market_ShareP', 'Total_Tariff_Revenue', 'Total_Wholesale_Cost', 
                                                    'Total_Balancing_Cost', 'Total_Distribution_Cost', 'Total_Capacity_Transaction', 'Total_Profit', 'Final_Cash'])


            for game in games:
                aggregate_df = aggregate_df.append({'Boot': game, 'Avg_Income_to_Cost': avg_income_to_cost[game], 'Avg_Market_ShareC': avg_marke_shareC[game], 
                                                    'Avg_Market_ShareP': avg_marke_shareP[game], 'Total_Tariff_Revenue': total_tariff[game], 
                                                    'Total_Wholesale_Cost': total_wholesale[game], 'Total_Balancing_Cost': total_balancing[game], 
                                                    'Total_Distribution_Cost': total_distribution[game], 'Total_Capacity_Transaction': total_capacity_trans[game],     
                                                    'Total_Profit': total_profit[game], 'Final_Cash': final_cash[game]}, ignore_index = True)
                
            aggregate_accounting_info_dict.update({broker: aggregate_df})

        X = ['Tariff','Wholesale','Balancing','Distribution','Capacity','Profit', 'Final Cash']
        
        X_axis = np.arange(len(X))
        index = 0

        if len(aggregate_accounting_info_dict.keys()) == 2:
            shift = [-0.2, 0.2]
            width = 0.4
        elif len(aggregate_accounting_info_dict.keys()) == 3:
            shift = [-0.2, 0.0, 0.2]
            width = 0.2
        elif len(aggregate_accounting_info_dict.keys()) == 4:
            shift = [-0.3, -0.1, 0.1, 0.3]
            width = 0.2
        elif len(aggregate_accounting_info_dict.keys()) == 6:
            shift = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2]
            width = 0.1

        for broker in aggregate_accounting_info_dict.keys():

            data = np.array([aggregate_accounting_info_dict.get(broker)['Total_Tariff_Revenue'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Total_Wholesale_Cost'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Total_Wholesale_Cost'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Total_Balancing_Cost'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Total_Capacity_Transaction'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Total_Profit'].mean(),
                    aggregate_accounting_info_dict.get(broker)['Final_Cash'].mean()])
                    
            data[np.isnan(data)] = 0.0
            plt.bar(X_axis+shift[index], data, width, label = broker, color = color_book[broker])
            index += 1
            
        plt.xticks(X_axis, X)
        plt.xlabel('Category')
        plt.ylabel('Money (($)')
        plt.title(folder)
        plt.legend()
        plt.savefig(storage_path + 'Accounting1.jpg')
        plt.close()  

        X = ['Consumption', 'Production']
        
        X_axis = np.arange(len(X))
        index = 0

        for broker in aggregate_accounting_info_dict.keys():
            
            df = aggregate_accounting_info_dict.get(broker)

            data = np.array([df[df.Avg_Market_ShareC > 0.0].Avg_Market_ShareC.mean(),
                    df[df.Avg_Market_ShareP > 0.0].Avg_Market_ShareP.mean()])
            
            data[np.isnan(data)] = 0.0  
            plt.bar(X_axis+shift[index], data, width, label = broker, color = color_book[broker])
            index += 1
            
        plt.xticks(X_axis, X)
        plt.xlabel('Market Share')
        plt.ylabel('Percentage')
        plt.title(folder)
        plt.legend()
        plt.savefig(storage_path + 'Accounting2.jpg')
        plt.close()

    except:
        print("Error in ", dir)





