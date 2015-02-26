__author__ = 'zhangnan'

# Machine-Learning
#   backpropagation.py

#Created by zhangnan on 2/23/15.

import math,sys,re


def sigmoid(val):
        return 1.0 /(1.0 + math.exp(-val))

def sigmoid_prime(val):
        return val*(1.0 - val)

def parse_file(path):
    f = open(path,'r')
    if f == None:
        print 'error: file path is not correct'
        return
    attr_info = {}
    attr_list = []
    data_set = []
    for line in f:
        if len(attr_list) == 0:
            attr_list = re.split('\s',line.rstrip())
            continue
        data = re.split(r'\t',line.rstrip())
        # dic = {}
        for m in range(len(data)):
            if len(data[m]) != 0:
                data[m] = int(data[m])
        data_set.append(data)
    return (attr_list, data_set)

def dot_product(set, weight):
    return sum(float(value) * float(weight) for value, weight in zip(set, weight))

def learning(training_set, attr_list, learning_rate, iteration):
    weight = [0.0 for i in range(len(attr_list))]
    for i in range(iteration):
        k = i%len(training_set)
        in_o = dot_product(training_set[k], weight)
        out = sigmoid(in_o)
        error = training_set[k][-1]-out
        for j in range(len(weight)):
            weight[j]  = weight[j]+float(learning_rate)*error*learning_rate*sigmoid_prime(out)*training_set[k][j]
    return weight

def test(test_set, weight):
    error = 0
    for instance in test_set:
        out = sigmoid(dot_product(instance,weight))
        if instance[-1] == round(out):
            error += 1
    return float(error)/len(test_set)

def main():
    args = sys.argv[1:]
    if len(args) != 4:
        print 'usage: training_file test_file learning_rate number_of_iteration'
    (attr_info, data_set) = parse_file(args[0])
    (test_attr_info, test_data_set) = parse_file(args[1])
    learning_rate = float(args[2])
    weight = learning(data_set, attr_info, learning_rate, int(args[3]))
    error_rate_trained = test(data_set, weight)
    error_rate_test = test(test_data_set, weight)

    print '\nAccuracy on training set ({} instances): {:.2%}'.format(len(data_set),error_rate_trained)
    print '\nAccuracy on test set ({} instances): {:.2%}'.format(len(test_data_set), error_rate_test)


if __name__ == '__main__':
  main()