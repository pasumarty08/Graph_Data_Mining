import csv
import pandas as pd
import numpy as np
import random
import sys

random.seed(0)

# Function that implements Greedy algorithm
def Greedy(budgets, bids, queries):
	revenue = 0.0
	for q in queries:
		bidder = find_bidder_greedy(bids[q], budgets)
		if bidder != -1:
			revenue += bids[q][bidder]
			budgets[bidder] -= bids[q][bidder]

	return revenue;

# Function that implements Balance algorithm
def Balance(budget, bids, queries):
	revenue = 0.0;
	for q in queries:
		bidder = find_bidder_balance(bids[q], budget)
		if bidder != -1:
			revenue += bids[q][bidder]
			budget[bidder] -= bids[q][bidder]

	return revenue;

# Function that implements MSVV algorithm
def MSVV(rembudget, budgets, bids, queries):
	revenue = 0.0;
	for q in queries:
		bidder = find_bidder_msvv(bids[q], rembudget, budgets)
		if bidder != -1:
			revenue += bids[q][bidder]
			rembudget[bidder] -= bids[q][bidder]

	return revenue;

def check_budget(b, budgets):
	keys = b.keys()
	for k in keys:
		if budgets[k] >= b[k]:
			return 0
	return -1

def psi (xu):
	return 1 - np.exp(xu-1);

def find_bidder_greedy(b, budgets):
	keys = list(b.keys())
	maxBidder = keys[0]
	maxBid = -1;
	c = check_budget(b, budgets)
	if c == -1:
		return -1;
	for k in keys:
		if budgets[k] >= b[k]:
			if maxBid < b[k]:
				maxBidder = k
				maxBid = b[k]
			elif maxBid == b[k]:
				if maxBidder > k:
					maxBidder = k
					maxBid = b[k]
	return maxBidder

def find_bidder_balance(b, budgets):
	keys = list(b.keys())
	maxBidder = keys[0]
	c = check_budget(b, budgets)
	if c == -1:
		return -1;
	for k in keys:
		if budgets[k] >= b[k]:
			if budgets[maxBidder] < budgets[k]:
				maxBidder = k
			elif budgets[maxBidder] == budgets[k]:
				if maxBidder > k:
					maxBidder = k

	return maxBidder

def scaledBid (bid, rembud, bud):
	xu = (bud-rembud)/bud
	return bid*psi(xu)

def find_bidder_msvv(b, rembudgets, budgets):
	keys = list(b.keys())
	maxBidder = keys[0]
	c = check_budget(b, rembudgets)
	if c == -1:
		return -1;
	for k in keys:
		if budgets[k] >= b[k]:
			m1 = scaledBid(b[maxBidder], rembudgets[maxBidder], budgets[maxBidder])
			m2 = scaledBid(b[k], rembudgets[k], budgets[k])
			if m1 < m2:
				maxBidder = k
			elif m1 == m2:
				if maxBidder > k:
					maxBidder = k

	return maxBidder

def TotalRevenue(budget, bids, queries, type):
	total_revenue = 0.0;
	ITMAX = 100;
	for i in range(0,ITMAX):
		budgetDict = dict(budget)
		if type ==1:
			revenue = Greedy(budgetDict, bids, queries);
		elif type == 2:
			revenue = Balance(budgetDict, bids, queries);
		elif type == 3:
			revenue = MSVV(budgetDict, dict(budget), bids, queries);
		else:
			revenue = 0.0
		total_revenue += revenue

	return total_revenue/ITMAX

def main(type):
	budgetDict = dict();
	bidDict = dict();

	bidderData = pd.read_csv('bidder_dataset.csv')
	# The bidder dataset consists of four columns namely, Advertiser, Keyword, Bid Value, Budget
	# We have to map every advertiser with their budget so that we can keep tabs on their budget
	# Similarly, we have to keep a track of the bidvalue of each advertiser for a given keyword
	# The above mapping can be done using dictionaries.
	# The budgetDict contains key pair values of advertiser and their daily max budgets respectively.
	# The bidDict contains unique values of keyword and {the advertiser paired with the bidvalue} for that combination 

	for i in range(0, len(bidderData)):
		a = bidderData.iloc[i]['Advertiser']
		k = bidderData.iloc[i]['Keyword']
		bv = bidderData.iloc[i]['Bid Value']
		b = bidderData.iloc[i]['Budget']
		if not (a in budgetDict):
			budgetDict[a] = b
		if not (k in bidDict):
			bidDict[k] = {}
		if not (a in bidDict[k]):
			bidDict[k][a] = bv

	with open('queries.txt') as f:
		queries = f.readlines()
	queries = [x.strip() for x in queries]

	rev = TotalRevenue(budgetDict, bidDict, queries, type)
	print (rev)
	print (rev/sum(budgetDict.values()))

# Your code must take one argument as input, which will denote which algorithm to run. 
# The input arguments will be given as: greedy, balance, or msvv.
if __name__ == "__main__":
	if len(sys.argv) == 2:
		if sys.argv[1] == 'greedy':
			main(1)
		elif sys.argv[1] == 'balance':
			main(2)
		elif sys.argv[1] == 'msvv':
			main(3)
		else:
			print('Invalid Input')
	else:
		print("Please choose an algorithm: greedy, balance, or msvv")


