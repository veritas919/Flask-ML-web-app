# given a csv, which should be produced from running data_gatherer.py, this module will create 3 lists, which are:
# service_range_for_each_cat, max_cost_for_each_cat and max_performance_for_each_cat
# These lists hold, respectively, the range of service numbers, the maximum cost, and the maxmimum performance corresponding to each category
# additionally, this module will produce service_dict, a dictionary that holds the 4 metrics for each service 
# this module also calculates the number of service categories 

import pandas as pd

class MyPreprocessor:

    def __init__(self):
        self.num_cats = 0
        self.service_range_for_each_cat = []
        self.max_cost_for_each_cat = []
        self.max_performance_for_each_cat = []
        self.service_dict = {} 

    def preprocess(self, file_as_csv): 

        data = pd.read_csv(file_as_csv, sep = ",")

        index = data.index
        num_rows = len(index)


        # determine the smallest and largest category numbers
        smallest_service_cat_num = data.loc[0]['Service']
        smallest_service_cat_num = smallest_service_cat_num[1]

        largest_service_cat_num = data.loc[num_rows-1]['Service']
        largest_service_cat_num = largest_service_cat_num[1]

        # determine the number of categories we have 
        self.num_cats = int(largest_service_cat_num) - int(smallest_service_cat_num) + 1

        # create lists to hold the maximum cost or maximum performance for each category.
        # i.e. if max_costs_for_each_cat was [58, 67, 12] that means that the max cost for a cat1 service is 58, for cat2 service is 67, for cat3 service is 12


        for i in range(int(largest_service_cat_num)):
            val = i+1
            string_pattern = "S" + str(val)
            cat_data = data[data['Service'].str.contains(string_pattern)]

            column_cost = cat_data["Cost ($)"]
            max_val_cost = column_cost.max()
            self.max_cost_for_each_cat.append(max_val_cost)

            column_perf = cat_data["Time (s)"]  
            max_val_perf = column_perf.max()
            self.max_performance_for_each_cat.append(max_val_perf)


        #create a dictionary to hold the metrics for each possible service option 

        for index, row in data.iterrows():
            service_num = row["Service"]
            self.service_dict[service_num + "cost"] = row["Cost ($)"]
            self.service_dict[service_num + "reliability"] = row["Reliability(%)"] / 100
            self.service_dict[service_num + "time"] = row["Time (s)"]
            self.service_dict[service_num + "availability"] = row["Availability(%)"] / 100


        # generate a list to hold the tuples containing the range of service numbers for each category
        # ie. if we have s11 thru s14 and s21 thru s29, then this list will be [(1,4) , (1,9)]

        #service_range_for_each_cat = []

        for i in range(int(largest_service_cat_num)):
            val = i+1
            string_pattern = "S" + str(val)
            cat_data = data[data['Service'].str.contains(string_pattern)]

            cat_service_max = cat_data["Service"].iloc[-1]
            cat_service_max = int(cat_service_max[2]) 

            range_arr = [1, cat_service_max]

            self.service_range_for_each_cat.append(range_arr) 
