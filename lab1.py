import argparse
import pandas as pd
import math

# parser = argparse.ArgumentParser()

# parser.add_argument('--input_path', '-i', help='input path for proprecessing')
# parser.add_argument('--output_path', '-o', help='output path for proprecessing')
# #parser.add_argument('--task', '-t', required='True', choices=['remove', 'equalSizeDiscretize'], help='task that need to be done')
# parser.add_argument('--bin', type=int, default=3, help='depth of bin')
# parser.add_argument('propList', type=str, nargs='+', help='property for proprecessing')

# args = parser.parse_args()
data_Frame = pd.read_csv("bikes.csv")
#data_Frame = pd.read_csv(args.input_path)
data = data_Frame.to_dict('list')

# Min-max normalization
new_max = 1.0
new_min = 0.0

def min_max_normalization(data, new_max, new_min):
    """Min-max normalization performs a linear transformation on specified list of attributes"""
    new_data = {}
    for key, values in data.items():
        if key in ["Christophe-Colomb"]:#args.propList:
            new_data[key] = []
            for value in values:
                new_value = ((value-min(values))/(max(values) - min(values)))*(new_max - new_min) + new_min
                new_data[key].append(new_value)
    return new_data


# z-score normalization
def count_number_of_values_nonNaN(values):
    """Count the number of values non NaN"""
    count = 0
    for value in values:
        if math.isnan(value):
            continue
        count += 1
    return count

def mean_of_set_values(list_values):
    """Calculate mean of a set of values"""
    sum_values = 0
    for value in list_values:
        if math.isnan(value):
            continue
        sum_values += value
    return sum_values/count_number_of_values_nonNaN(list_values)

def standard_deviation_of_data(list_values):
    """Find standard deviation of the data"""
    sum_square = 0
    for value in list_values:
        if math.isnan(value):
            continue
        sum_square += value**2
    mean = mean_of_set_values(list_values)
    variance = 1/count_number_of_values_nonNaN(list_values) * sum_square - mean**2
    return math.sqrt(variance)

def z_score_normalization(data):
    """z-score normalization performs a linear transformation on specified list of attributes"""
    new_data = {}
    for key, values in data.items():
        if key in args.propList:
            new_data[key] = []
            mean  = mean_of_set_values(values)
            standard_deviation = standard_deviation_of_data(values)
            for value in values:
                if math.isnan(value):
                    continue
                new_value = (value - mean)/standard_deviation
                new_data[key].append(new_value)
    return new_data

# Discretization by Binning
def equal_frequency_bining(data, depth_of_bin):
    """Partition specified list of observation attributes into n bin by equal-frequency partitioning methods"""
    new_data = {}
    for key, values in data.items():
        if key in args.propList:
            length = count_number_of_values_nonNaN(values)
            i = 0
            while i < length:
                binn = bin
                new_value = mean_of_set_values()
                new_data[key].append()

print(min_max_normalization(data, new_max, new_min))