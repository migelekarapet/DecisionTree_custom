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
	class_values = list(set(row[-1] for row in ds))
	res_index, res_value, res_score, res_groups = 1111, 1111, 1111, None
	for index in range(len(ds[0])-1):
		for row in ds:
			ds_groups = split_ds(index, row[index], ds)
			gini_ind = gini_idx(groups, class_values)
			print('X%d < %.2f Gini=%.2f' % ((index+1), row[index], gini_ind))
			if gini < b_score:
				res_index, res_value, res_score, res_groups = index, row[index], gini_ind, ds_groups
	return {'index':res_index, 'value':res_value, 'groups':res_groups}
 
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
split = best_split(ds)
print('Split: [X%d < %.2f]' % ((split['index']+1), split['value']))