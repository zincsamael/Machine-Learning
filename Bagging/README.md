Bagging 

In this problem, I'm using the Decision Tree as the basic classifier to train the each data set.

For random choosing data with replacement, I'm using the python built-in function random.sample(dataset, num) 
which can choose num of data from the dataset list randomly. For each bagging step, I'm choosing N data from 
the original training data set, then which can be seen as replacement random choosing.

For bagging step, I'm using following function:

def bagging_creating_trees(self, bootstraps, N):
        for i in xrange(bootstraps):
            ds = random.sample(self.origin_training_set, N)
            root = create_dt(self.dt_attr_info, ds)
            # print_tree(root,self.dt_attr_info,[])
            # print '\n'
            self.trees.append(root)

firstly, call the create_dt 'bootstrap' times, which as a result I can get 'bootstrap' number of tree roots 
and store them in the list self.trees.

For classify step/label step,  I'm using following function:

def bagging_training_by_each_tree(self, data):
        result = {0:0,1:0}
        for t in self.trees:
            result[judge(t, data)] += 1
        if result[0]>=result[1]: return 0
        else: return 1

because for all the data set there are only 2 labels as 0 or 1, then for the convenience, I'm initialize the 
result as a dictionary for only 2 keys with value 0 for each. Then count the number of 0 and 1, then get the 
 bigger one as the label for current data item. I've mentioned in the report that I'm using odd number of 
 each bootstrap, just in case that the draw of 0 and 1.
 
 
        