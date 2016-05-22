__author__ = 'jayanthvenkataraman'

from math import log
import operator

def create_data_set():
    data_set = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return data_set, labels

def calculate_shannon_entropy(dataSet):
    num_entries = len(dataSet)
    label_counts = {}
    for feature_vector in dataSet: #the the number of unique elements and their occurance
        current_label = feature_vector[-1]
        if current_label not in label_counts.keys(): label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_entropy = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num_entries
        shannon_entropy -= prob * log(prob,2) #log base 2
    return shannon_entropy

def split_data_set(data_set, feature_index, feature_value):
    result_data_set = []
    for feature_vector in data_set:
        if feature_vector[feature_index] == feature_value:
            reduced_feature_vector = feature_vector[:feature_index]     #chop out axis used for splitting
            reduced_feature_vector.extend(feature_vector[feature_index+1:])
            result_data_set.append(reduced_feature_vector)
    return result_data_set

def choose_best_feature_to_split(data_set):
    num_features = len(data_set[0]) - 1      #the last column is used for the labels
    base_entropy = calculate_shannon_entropy(data_set)
    best_information_gain = 0.0; best_feature = -1
    for i in range(num_features):        #iterate over all the features
        feature_value_list = [example[i] for example in data_set]#create a list of all the examples of this feature
        unique_vals = set(feature_value_list)       #get a set of unique values
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set)/float(len(data_set))
            new_entropy += prob * calculate_shannon_entropy(sub_data_set)
        information_gain = base_entropy - new_entropy     #calculate the info gain; ie reduction in entropy
        if (information_gain > best_information_gain):       #compare this to the best gain so far
            best_information_gain = information_gain         #if better than current best, set to best
            best_feature = i
    return best_feature                      #returns an integer

def majority_count(class_list):
    class_count={}
    for vote in class_list:
        if vote not in class_count.keys(): class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def create_tree(data_set,labels):
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]#stop splitting when all of the classes are equal
    if len(data_set[0]) == 1: #stop splitting when there are no more features in dataSet
        return majority_count(class_list)
    best_feature = choose_best_feature_to_split(data_set)
    best_feature_label = labels[best_feature]
    my_tree = {best_feature_label:{}}
    del(labels[best_feature])
    feature_values = [example[best_feature] for example in data_set]
    unique_values = set(feature_values)
    for value in unique_values:
        sub_labels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        my_tree[best_feature_label][value] = create_tree(split_data_set(data_set, best_feature, value),sub_labels)
    return my_tree

def classify(input_tree,feature_labels,test_vector):
    first_str = input_tree.keys()[0]
    second_dict = input_tree[first_str]
    feature_index = feature_labels.index(first_str)
    key = test_vector[feature_index]
    value_of_feature = second_dict[key]
    if isinstance(value_of_feature, dict):
        classLabel = classify(value_of_feature, feature_labels, test_vector)
    else: classLabel = value_of_feature
    return classLabel

def store_tree(input_tree,file_name):
    import pickle
    fw = open(file_name,'w')
    pickle.dump(input_tree,fw)
    fw.close()

def grab_tree(file_name):
    import pickle
    fr = open(file_name)
    return pickle.load(fr)