__author__ = 'zhangnan'

# Machine Learning
#   dt.py

#Created by zhangnan on 1/18/15.

import sys
import re
import math
import copy
from math import log

class Node:
    attr_name = None
    attr_value = None
    children = []    #node array
    cate = None


def parse_file(path):
    f = open(path,'r')
    if f == None:
        print 'error: file path is not correct'
        return
    attr_info = {}
    attr_list = []
    data_set = []
    entropy = 0
    # count1 = 0
    for line in f:
        if len(attr_info) == 0:
            attr_list = re.split('\s',line.rstrip())
            for i in range(0,len(attr_list),2): attr_info[attr_list[i]] = attr_list[i+1]
            continue
        data = re.split(r'\t',line.rstrip())
        dic = {}
        for m in range(len(data)-1):
            dic[attr_list[2*m]] = data[m]
        dic['cls'] = data[-1]
        data_set.append(dic)
        # if int(data[-1]) == 1: count1 += 1
    return (attr_info, data_set)


def print_tree(node, attr_info,stack):
    if node.attr_name:
        text = len(stack)*'| ' + node.attr_name + ' = '
        stack.append(node)
        for child in node.children:
            if len(child.children) == 0:
                print text + str(node.children.index(child)+1) + ':{}'.format(str(child.cate))
            else:
                print text + str(node.children.index(child)+1) + ':'
                print_tree(child,attr_info,stack)
        stack.pop()

def entropy(pos_count, n):
    m = -((1-float(pos_count)/n)*(math.log(1-float(pos_count)/n,2.0)))
    i = float(pos_count)/n
    k = (float(pos_count)/n) * math.log(i,2.0)
    return m-k

# def ig()

def create_dt(attr_info, data_set):
    if attr_info == None or data_set == None:
        print 'invalid data and attribute'
        return
    n = len(data_set)
    pos_count = 0
    for i in range(n):
        if int(data_set[i]['cls']) == 1:
            pos_count += 1

    node = Node()
    if pos_count == 0:
        # print 'all values negative'
        node.cate = 0
        return node
    if pos_count == n:
        # print 'all values positive'
        node.cate = 1
        return node

    e = entropy(pos_count,n)
    max_ig = 0
    max_ig_attr = attr_info.keys()[0]
    max_pos_attr = [0 for m in range(int(attr_info[max_ig_attr]))]
    max_all_attr = [0 for m in range(int(attr_info[max_ig_attr]))]
    for key in attr_info.keys():
        if key == 'cls':
            continue
        attr_value_cnt = int(attr_info[key])
        pos_attr = [0 for m in range(attr_value_cnt)]
        all_attr = [0 for m in range(attr_value_cnt)]
        pos_for_curnt = 0
        for j in range(len(data_set)):
            all_attr[int(data_set[j][key])-1] += 1
            if int(data_set[j]['cls']) == 1:
                pos_attr[int(data_set[j][key])-1] += 1
        ig = e
        for m in range(attr_value_cnt):
            if pos_attr[m] == 0 or pos_attr[m] == all_attr[m]:
                continue
            else:
                ig -= all_attr[m]/float(n)*entropy(pos_attr[m],all_attr[m])
        if ig>max_ig:
            max_ig = ig
            max_ig_attr = key
            max_pos_attr = pos_attr
            max_all_attr = all_attr
            if ig == e:
                break
    attr_cnt = int(attr_info[max_ig_attr])
    node.attr_name = max_ig_attr
    node.children = list([])
    # print '\n'
    # print node.attr_name
    # for i in range(len(data_set)):
    #     del data_set[i][max_ig_attr_idx]
    # new_attr_info = list(attr_info)
    # del attr_info[max_ig_attr]
    new_attr = {}
    for attr in attr_info:
                if attr != max_ig_attr:
                    new_attr[attr] = attr_info[attr]
    for m in range(attr_cnt):
        if max_pos_attr[m] == 0 or max_pos_attr[m] == max_all_attr[m]:
            child = Node()
            if max_pos_attr[m] == 0:
                child.cate = 0
                # print 'append child classified 0'
                node.children.append(child)
            else:
                child.cate = 1
                # print 'append child classified 1'
                node.children.append(child)
        else:
            # print 'push '
            sub_data_set = [r for r in data_set if int(r[max_ig_attr]) == m+1]
            if len(new_attr) == 0:
                sub_pos = 0
                for set in sub_data_set:
                    if int(set['cls']) == 1:
                        sub_pos += 1
                child = Node()
                if sub_pos >= len(sub_data_set)/2:
                    child.cate = 1
                    # print 'append child classified 1'
                    node.children.append(child)
                else:
                    child.cate = 0
                    # print 'append child classified 0'
                    node.children.append(child)
                continue
            node.children.append(create_dt(new_attr, sub_data_set))
            # print 'pop '

    return node

def judge(root, item):
    if len(root.children) == 0:
        return root.cate
    else:
        return judge(root.children[int(item[root.attr_name])-1],item)



def training(root, data):
    correct = 0
    for item in data:
        if judge(root,item) == int(item['cls']):
            correct += 1
    return float(correct)/len(data)

# def testing(root, data):


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if len(args) != 2:
        print 'usage: training_file test_file'

    (attr_info, data_set) = parse_file(args[0])
    (test_attr_info, test_data_set) = parse_file(args[1])

    #used for problem section A) B) C)
    root = create_dt(attr_info, data_set)
    print_tree(root, attr_info, list([]))
    print '\nAccuracy on training set ({} instances): {:.2%}'.format(len(data_set),training(root,data_set))
    per = training(root,test_data_set)
    print '\nAccuracy on test set ({} instances): {:.2%}'.format(len(data_set), per)

    # used for problem section D)
    # text = ''
    # for i in range(50,len(data_set),50):
    #     root = create_dt(attr_info, data_set)
    #     # print_tree(root, attr_info, list([]))
    #
    #     # print '\nAccuracy on training set ({} instances): {:.2%}'.format(len(data_set),training(root,data_set))
    #     per = training(root,test_data_set)
    #     print '\nAccuracy on test set ({} instances): {:.2%}'.format(len(data_set), per)
    #     text += '\t' + str(per)
    # print text
if __name__ == '__main__':
  main()