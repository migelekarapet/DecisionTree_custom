# this method splits the ds based on factor and factor value
def split_ds(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
 
# Gini index is then calculated for the partitioned ds
def gini_idx(groups, classes):
	# number of samples at the pont of split is obtained below
	n_samples = float(sum([len(group) for group in groups]))
	# the iterations below calculate the sum of weighted Gini indices for each of the groups
	n_gini = 0.0
	for group in groups:
		size = float(len(group))
		# check
		if size == 0:
			continue
		score = 0.0
		# the group is scored based on calculated proportion for each class per group
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# the group score is weighted accordingly
		n_gini += (1.0 - score) * (size / n_samples)
	return n_gini
 
# this method calculates the best split point for the given ds
def best_split(ds):
	# run over the possible values that the class variable entails
	values_cls = list(set(row[-1] for row in ds))
	res_index, res_value, res_score, res_groups = 1111, 1111, 1111, None
	# as we can see from below the ds is list of lists. ds[0] is firts element which has dimensions of 3. we substract 1
	# to get iterations over values and not the class (0,1)
	#furthrmore, the iterations in second cycle are taking the index = 0 (in first iteration) or index = 1 in second. 
	# the second cycle per se passes the the index (e.g. index=0) and row[0] first value of row in first inner iteration
	# it has 6.1524 value in our example below. Then this value along with index=0 is passed to split_ds() along with entire dataset
	# the split_ds() method divides this into two groups. it iterates over all rows in the dataset (for index=0 in this case) 
	#and performs a check on whether value any row's 0'th element is lower than  6.1524 (and then assigns entire row to left group) or, 	
	# on opposite, the value is higher - and then assigns enrire row in iteration to the right group. split_ds() then returns both groups
	# those are passed to gini_idx() to perform the cost of split evaluation. 
	# Furthermore,for row in ds selects the next row and index [0] applied to it results in 3.2598;And the process described above repeats
	# when all the raws are exhausted the index = 1 (second column) is passed from top to bottom to next iteration
	# thus here the 5.0729 is passed with index = 1 to split_ds() along with entire dataset. And the whole process repeats. 
	# as a result for a test dataset we'll have something like 
	# X1 < 6.16 Gini=0.35
	# X1 < 3.26 Gini=0.47
	# X1 < 5.37 Gini=0.72
	# ...
	# X2 < 5.16 Gini=0.19
	# X2 < 5.37 Gini=0.42
	# whus iterating over X1 and X2 attributes. Finally a best split (using lowest Gini index value) could be chosen

	for index in range(len(ds[0])-1):
		for row in ds:
			ds_groups = split_ds(index, row[index], ds)
			gini_ind = gini_idx(ds_groups, values_cls)
			print('X%d < %.2f Gini=%.2f' % ((index+1), row[index], gini_ind))
			if gini < b_score:
				res_index, res_value, res_score, res_groups = index, row[index], gini_ind, ds_groups
	return {'index':res_index, 'value':res_value, 'groups':res_groups}


# terminating node value creaiton
def terminating(group):
	results = [row[-1] for row in group]
	return max(set(results), key=results.count)
 
# make terminating or creation of node's child split
def split_node(node, depth_max, size_min, depth):
	left, right = node['groups']
	del(node['groups'])
	# emptyness check
	if not left or not right:
		node['left'] = node['right'] = terminating(left + right)
		return
	# verifying if we reached max depth
	if depth >= depth_max:
		node['left'], node['right'] = terminating(left), terminating(right)
		return
	# node's left child
	if len(left) <= size_min:
		node['left'] = terminating(left)
	else:
		node['left'] = best_split(left)
		split_node(node['left'], depth_max, size_min, depth+1)
	# node's right child
	if len(right) <= size_min:
		node['right'] = terminating(right)
	else:
		node['right'] = best_split(right)
		split_node(node['right'], depth_max, size_min, depth+1)
 

# decision tree construciton
def dec_tree_construct(trn, depth_max, size_min):
	root = best_split(trn)
	split_node(root, depth_max, size_min, 1)
	return root
 
# decision tree printing
def tree_print(node, depth=0):
	if isinstance(node, dict):
		print('%s[X%d < %.2f]' % ((depth*' ', (node['index']+1), node['value'])))
		tree_print(node['left'], depth+1)
		tree_print(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))
ds = [[6.1524,5.0729,0],
	[3.2598,3.1597,0],
	[5.3698,4.1587,0],
	[5.7854,4.8965,0],
	[4.3256,4.2058,0],
	[9.8596,5.1309,1],
	[9.0058,5.0789,1],
	[9.7856,2.8315,1],
	[12.5961,5.1587,1],
	[8.3258,5.3698,1]]

#dec_tree = dec_tree_construct(ds, 1, 1)
#tree_print(dec_tree)

# we'll now perform a prediction for decision tree's most likely node 
def node_prediction(nd, row):
	if row[nd['index']] < nd['value']:
		if isinstance(nd['left'], dict):
			return node_prediction(nd['left'], row)
		else:
			return nd['left']
	else:
		if isinstance(nd['right'], dict):
			return node_prediction(nd['right'], row)
		else:
			return nd['right']
 
# node_prediction call is made from here
def decision_tree(train, test, max_depth, min_size):
	tree = build_tree(train, max_depth, min_size)
	predictions = list()
	for row in test:
		prediction = node_prediction(tree, row)
		predictions.append(prediction)
	return(predictions)
 
# implement main for soem example ...

