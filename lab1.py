import argparse
import pandas as pd
import math
import numpy as np
import csv

parser = argparse.ArgumentParser()

parser.add_argument('--input_path', '-i', required='True', help='input path for proprecessing')
parser.add_argument('--output_path', '-o', required='True', help='output path for proprecessing')
parser.add_argument('--task', '-t', required='True', choices=['minMaxNormalization', 'zScoreNormalization', 
'equalWidthDiscretize', 'equalFrequencyDiscretize', 'fillInMissingInstance','removeMissingInstance'], help='task that need to be done')
parser.add_argument('--bin', type=int, default=3, help='depth of bin')
parser.add_argument('--new_min', type=float, default=0.0, help='new min of min-max normalization')
parser.add_argument('--new_max', type=float, default=1.0, help='new max of min-max normalization')
parser.add_argument('propList', type=str, nargs='+', help='property for proprecessing')

args = parser.parse_args()


def writing_csvfile(csv_file_name, data):
    """"""
    with open(csv_file_name, mode='w', newline='') as csv_file:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        i = 0
        num_record = len(data[fieldnames[0]])
        record = []
        while i < num_record:
            one_record = {}
            for field in fieldnames:
                one_record[field] = data[field][i]
            i += 1
            record.append(one_record)

        writer.writerows(record)
    
# min-max normalization
def min_max_normalization(data, prop_list, new_min, new_max):
    """Min-max normalization performs a linear transformation on specified list of attributes"""
    new_data = {}
    for key, values in data.items():
        if key in prop_list:
            new_data[key] = []
            for value in values:
                new_value = ((value-min(values))/(max(values) - min(values)))*(new_max - new_min) + new_min
                new_data[key].append(new_value)
        else:
            new_data[key] = values
    return new_data

# z-score normalization
def count_number_of_values_nonNaN(values):
    """Count the number of values non NaN"""
    count = 0
    for isnan in pd.isna(values):
        if isnan == True:
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

def mode_of_set_values(list_values):
    """Find mode of a set of values that its type is nominal"""
    independent_values = []
    i = 0
    for value in list_values:
        check = pd.isna(list_values)[i]
        i += 1
        if (value not in independent_values) and (check == False):
            independent_values.append(value)
    
    count_list = np.zeros(len(independent_values))

    for value in list_values:
        if value in independent_values:
            count_list[independent_values.index(value)] += 1

    return independent_values[np.where(count_list == max(count_list))[0][0]]

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

def z_score_normalization(data, prop_list):
    """z-score normalization performs a linear transformation on specified list of attributes"""
    new_data = {}
    for key, values in data.items():
        if key in prop_list:
            new_data[key] = []
            mean  = mean_of_set_values(values)
            standard_deviation = standard_deviation_of_data(values)
            for value in values:
                new_value = (value - mean)/standard_deviation
                new_data[key].append(new_value)
        else:
            new_data[key] = values
    return new_data

# Discretization by Binning
def equal_frequency_binning(data, prop_list, num_bins):
    """Partition specified list of observation attributes into n bin by equal-frequency partitioning methods"""
    new_data = {}
    for key, values in data.items():
        if key in prop_list:
            length = len(values)        # can consist nan value
            new_data[key] = [''] * length

            depth_of_bin = length//num_bins
            sorted_data = sorted(values)

            lower_boundary = sorted_data[0] - 999999    #-inf
            upper_boundary = (sorted_data[depth_of_bin] + sorted_data[depth_of_bin - 1])/2

            i = 0
            order_bin = 1
            while i < length:
                check = pd.isna(values)[i]
                if check == True:
                    i += 1
                    new_data[key].append(np.nan)
                    continue
                if sorted_data[i] >= lower_boundary and sorted_data[i] <= upper_boundary:
                    if upper_boundary >= sorted_data[length - 1]:
                        new_data[key][values.index(sorted_data[i])] = '(' + str(lower_boundary) + '-inf)'
                    elif lower_boundary <= sorted_data[0]:
                        new_data[key][values.index(sorted_data[i])] = '(-inf-' + str(upper_boundary) + ']'
                    else:
                        new_data[key][values.index(sorted_data[i])] = '(' + str(lower_boundary) + '-' + str(upper_boundary) + ']'
                    i += 1
                else:
                    lower_boundary = upper_boundary
                    order_bin += 1
                    if depth_of_bin + i + 1 >= length:    
                        upper_boundary = sorted_data[length - 1 ] + 999999
                    elif num_bins - order_bin <= length%num_bins:
                        upper_boundary = (sorted_data[depth_of_bin  + 1 + i] + sorted_data[depth_of_bin + 1 + i - 1])/2
                    else:
                        upper_boundary = (sorted_data[depth_of_bin + i] + sorted_data[depth_of_bin + i - 1])/2
                
        else:
            new_data[key] = values
    return new_data
            
def equal_width_binning(data, prop_list, num_bins):
    """Partition specified list of observation attributes into n bin by equal-width partitioning methods"""
    new_data = {}
    for key, values in data.items():
        if key in prop_list:
            length = len(values)        # can consist nan value
            new_data[key] = [''] * length
            width = (max(values) - min(values))/num_bins

            sorted_data = sorted(values)
            
            lower_boundary = sorted_data[0] - 999999    #-inf
            upper_boundary = sorted_data[0] + width

            i = 0
            while i < length:
                check = pd.isna(values)[i]
                if check == True:
                    i += 1
                    new_data[key].append(np.nan)
                    continue
                if sorted_data[i] >= lower_boundary and sorted_data[i] <= upper_boundary:
                    if upper_boundary >= sorted_data[length - 1]:
                        new_data[key][values.index(sorted_data[i])] = '(' + str(lower_boundary) + '-inf)'
                    elif lower_boundary <= sorted_data[0]:
                        new_data[key][values.index(sorted_data[i])] = '(-inf-' + str(upper_boundary) + ']'
                    else:
                        new_data[key][values.index(sorted_data[i])] = '(' + str(lower_boundary) + '-' + str(upper_boundary) + ']'
                    i += 1
                else:
                    lower_boundary = upper_boundary
                    upper_boundary = lower_boundary + width
        else:
            new_data[key] = values

    return new_data

# Deleting missing data
def del_missing_data(data, prop_list):
    """Delete missing data on specified list of attributes"""
    new_data = data
    for key, values in data.items():
        if key in prop_list:
            record_indexs = []
            i = 0
            bool_list =  pd.isna(values)
            for isnan in bool_list:
                if isnan == True:
                    record_indexs.append(i)
                i += 1
            
            # delete all record which has index in record_indexs
            j = 0         
            for index in record_indexs:
                for k in new_data.keys():
                    new_data[k].pop(index - j)
                j += 1
    
    return new_data

# Filling missing data
def fill_missing_data(data, prop_list):
    """Fill missing data on specified list of attributes"""
    for key, values in data.items():
        if key in prop_list:
            if type(values[0]) == type(1.1) or type(values[0]) == type(1):
                mean = mean_of_set_values(values)
                i = 0
                bool_list =  pd.isna(values)
                for isnan in bool_list:
                    if isnan == True:
                        values[i] = mean
                    i += 1
            else:
                mode = mode_of_set_values(values)
                i = 0
                bool_list =  pd.isna(values)
                for isnan in bool_list:
                    if isnan == True:
                        values[i] = mode
                    i += 1
    return data           

def main(args):
    """"Main processing"""
    data_Frame = pd.read_csv(args.input_path)
    data = data_Frame.to_dict('list')

    new_data = {}
    if args.task == "minMaxNormalization":
        new_data = min_max_normalization(data, args.propList, float(args.new_min), float(args.new_max))
    elif args.task == "zScoreNormalization":
        new_data = z_score_normalization(data, args.propList)
    elif args.task == "equalFrequencyDiscretize":
        new_data = equal_frequency_binning(data, args.propList, int(args.bin))
    elif args.task == "equalWidthDiscretize":
        new_data = equal_width_binning(data, args.propList, int(args.bin))
    elif args.task == "removeMissingInstance":
        new_data = del_missing_data(data, args.propList)
    elif args.task == "fillInMissingInstance":
        new_data = fill_missing_data(data, args.propList)

    writing_csvfile(args.output_path, new_data)
    
if __name__ == "__main__":
    main(args)