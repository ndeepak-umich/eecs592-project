import numpy as np

class Node:
	def __init__(self,x,index,climit,p=None,lc=None,rc=None):

		self.data=x
		self.index=index
		self.parent=p
		self.lchild=lc
		self.rchild=rc
		self.max_child=climit
		self.nchild=0

def bitstring_to_gene(x):
	split_index = int((len(x)-1)/2)
	head = x[:split_index]
	tail = x[split_index:]
	gene = []
	for i in head:
		if i == 0:
			gene.append('U')
		else:
			gene.append('I')
	for i in tail:
		if i == 0:
			gene.append('C')
		else:
			gene.append('F')

	return gene

def queue_tree(gene):
	split_index = int((len(gene)-1)/2)
	head = gene[:split_index]
	tail = gene[split_index:]
	queue = []
	root = Node(gene[0], 0, 2)
	queue.append(root)
	index = 0
	for i in range(1,len(head)):
		while (queue[index].nchild >= queue[index].max_child):
			index += 1
		child = Node(head[i], i, 2, queue[index])
		if queue[index].nchild == 0:
			queue[index].lchild = child
		elif queue[index].nchild == 1:
			queue[index].rchild = child
		else:
			print("Error")

		queue[index].nchild += 1
		queue.append(child)

	number_of_leaves = int((len(head)+1)/2)
	depth = np.log2(len(head))
	first_leaf = int(2**depth - 1)
	post_order_traversal = []
	for i in range(first_leaf, len(head)):
		post_order_traversal.append(i)
	for i in range(number_of_leaves - 1, first_leaf):
		post_order_traversal.append(i)

	leaf_index = 0
	for i in range(len(tail)):
		while (queue[post_order_traversal[leaf_index]].nchild >= queue[post_order_traversal[leaf_index]].max_child):
			leaf_index += 1
		child = Node(tail[i], i+len(head), 2, queue[post_order_traversal[leaf_index]])
		if queue[post_order_traversal[leaf_index]].nchild == 0:
			queue[post_order_traversal[leaf_index]].lchild = child
		elif queue[post_order_traversal[leaf_index]].nchild == 1:
			queue[post_order_traversal[leaf_index]].rchild = child
		else:
			print("Error")
		queue[post_order_traversal[leaf_index]].nchild += 1
		queue.append(child)

	return queue

def intersection(list1, list2):
	list3 = [value for value in list1 if value in list2]
	return list3

def decode(queue, index):
	root = queue[index]
	if root.nchild == 0:
		return root.data
	lchild = root.lchild
	rchild = root.rchild
	cnn_decoded = []
	match root.data:
		case "U":
			lchild_set = decode(queue, lchild.index)
			rchild_set = decode(queue, rchild.index)
			cnn_decoded.extend(lchild_set)
			cnn_decoded.extend(rchild_set)
		case "I":
			lchild_set = decode(queue, lchild.index)
			rchild_set = decode(queue, rchild.index)
			cnn_decoded = intersection(lchild_set, rchild_set)
	return cnn_decoded

def Gene_to_Set(gene):
	queue = queue_tree(gene)
	return decode(queue, 0)
