__author__ = 'zhangnan'

# Machine-Learning
#   bagging.py

#Created by zhangnan on 4/9/15.

from dt import *
import random
import time

class Bagging_Decision_Tree:
    def __init__(self, training_set, attr_info, test_set):
        self.origin_training_set = training_set
        self.test_set = test_set
        self.dt_attr_info = attr_info
        self.trees = []

    def bagging_creating_trees(self, bootstraps, N):
        for i in xrange(bootstraps):
            ds = random.sample(self.origin_training_set, N)
            root = create_dt(self.dt_attr_info, ds)
            # print_tree(root,self.dt_attr_info,[])
            # print '\n'
            self.trees.append(root)

    def bagging_training_by_each_tree(self, data):
        result = {0:0,1:0}
        for t in self.trees:
            result[judge(t, data)] += 1
        if result[0]>=result[1]: return 0
        else: return 1

    def bagging_dt_testing(self):
        correct = 0
        for item in self.test_set:
            c = self.bagging_training_by_each_tree(item)
            if c == int(item['cls']):
                correct += 1
        return float(correct)/len(self.test_set)

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
    # print_tree(root, attr_info, list([]))
    ts = time.time()
    print '\nAccuracy on training set ({} instances): {:.2%}'.format(len(data_set),training(root,data_set))
    per = training(root,test_data_set)
    print '\nAccuracy on test set ({} instances): {:.2%}'.format(len(test_data_set), per)
    te = time.time()
    print 'Executing time %2.2f sec' % (te-ts)
    Ns = [50, 75, 100, 122]
    bootstraps = [55, 95, 135, 175, 225, 395, 465]
    for N in Ns:
        print '\n'
        for b in bootstraps:
            ts = time.time()

            bagging = Bagging_Decision_Tree(data_set, attr_info, test_data_set)
            bagging.bagging_creating_trees(b, N)
            te = time.time()
            print 'Executing time %2.2f sec' % (te-ts)
            # print 'Accuracy on bootstraps={} and N={} : {:.3%}'.format(b, N, bagging.bagging_dt_testing())

if __name__ == '__main__':
  main()
