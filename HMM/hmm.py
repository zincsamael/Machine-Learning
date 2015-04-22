__author__ = 'zhangnan'

# Machine-Learning
#   hmm.py

#Created by zhangnan on 3/12/15.

import sys,re

def parse_model(path):
    '''This is used for parse the model file.'''
    f = open(path, 'r')
    if f == None:
        print 'error: file path is not correct'
        return
    lines = f.readlines()
    stats_trans = []
    stats_count = int(lines[0])
    stats_pi = map(float,re.split(r' ',lines[1].rstrip()))
    trans = map(float,re.split(r' ',lines[2].rstrip()))
    for i in range(0,len(trans),stats_count):
        stats_trans.append(trans[i:i+stats_count])
    observe_count = int(lines[3])
    observe = {}
    set = lines[4].replace(' ','').rstrip()
    for i in range(len(set)):
        observe[set[i]] = i
    trans = map(float,re.split(r' ',lines[5].rstrip()))
    observe_trans = []
    for i in range(0,len(trans),observe_count):
        observe_trans.append(trans[i:i+observe_count])
    return (stats_count, stats_pi, stats_trans, observe_count, observe, observe_trans)

def parse_sequence(path):
    '''This is used for parse the test sequence.'''
    f = open(path, 'r')
    sequences = []
    for line in f:
        sequences.append(line.replace(' ','').rstrip('\n'))
    return sequences

# def relax(p,pi)

def hmm_viterbi(stats_pi, stats_trans, obs_trans, obs, sequences):
    '''This is the viterbi decoding implementation where can produce the probability and parent of each step '''
    for sq in sequences:
        '''Iteration for all the sequences in test.dat'''
        dp = []   # probability table
        pi = []   # parent table
        for i in range(len(sq)):
            '''For each sequence, loop all the characters'''
            idx = obs[sq[i]]
            if i == 0:
                # Initialled from pi vector(stats_pi).
                dp.append([p[idx]*trans for p,trans in zip(obs_trans,stats_pi)])
                continue
            prob_vector = [] # In each iteration, store the maximized probability at each state.
            parent_vector = [] # In each iteration, store the parent to record where current state comes from.
            for m in range(len(obs_trans)):
                '''Each character in certain sequence also denote such state.'''
                parent = 0
                max_prob = 0
                for k in range(len(obs_trans)):
                    '''Calculate the max probability'''
                    c_p = dp[i-1][k]
                    c_trans = stats_trans[k][m]
                    c_obs = obs_trans[m][idx]
                    x = c_p*c_trans*c_obs
                    if x>max_prob:
                        max_prob = x
                        parent = k
                parent_vector.append(parent)
                prob_vector.append(max_prob)
            dp.append(prob_vector)
            pi.append(parent_vector)
        maxp = 0
        parent = 0
        for i in range(len(dp[-1])):
            if maxp<dp[-1][i]:
                maxp = dp[-1][i]
                parent = pi[-1][i]
        print dp
        print '\n'
        print pi
        def get_p(x,idx,stack):
            '''This is use for print the seqence of the best probable state squence after record all the probability and parent'''
            next = idx
            stack.append(idx)
            for i in range(len(x)-1,-1,-1):
                next = x[i][next]
                stack.append(next)
            stack.reverse()
            return stack
        print sq
        print get_p(pi,parent,[])
        # print pi


def main():
    '''This is the main function.'''
    args = sys.argv[1:]
    if len(args) != 2:
        print "usage: model test_file"
    (stats_count, stats_pi, stats_trans, obs_count, obs, obs_trans) = parse_model('model')
    # stats_count = 3
    # stats_pi = [0.3,0.3,0.4]
    # stats_trans = [[0.80,0.19,0.01],[0.10,0.80,0.10],[0.01,0.19,0.80]]
    # obs_count = 2
    # obs = {'a':0, 'c':1}
    # obs_trans = [[0.7,0.3],[0.5,0.5],[0.3,0.7]]
    sequence = parse_sequence('test.dat')
    # print sequence
    hmm_viterbi(stats_pi,stats_trans,obs_trans,obs,sequence)

if __name__ == '__main__':
  main()