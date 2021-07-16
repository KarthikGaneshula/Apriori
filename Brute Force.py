from itertools import combinations
import time
min_s = int(input("Enter the minimum support: "))
min_c = int(input("Enter the minimum Confidence: "))
start = time.time()
file_object = open("DataSet-5.txt", "r")
l_of_data = file_object.readlines()
allItemList = []
items_list = []
d = {}
n_list = 0
support_of_all_item_set={}
for q in l_of_data:
    q = q.replace("\n", "")
    allItemList.append("".join(q.split(" ")[1].split(",")))
    s = set()
    for i in "".join(q.split(" ")[1:]).split(","):

        if (i,) in d:
            d[(i,)] += 1
        else:
            d[(i,)] = 1
        s.add(i)
    items_list.append(s)
    n_list+=1

k = []
for i in items_list:
	i = list(i)
	k.extend(i)

k = list(set(k))


def find_support(l):
	dict_sup = {}
	length = len(items_list)
	for i in l:
		c = 0
		for j in items_list:
			if type(i) != tuple:
				if set([i]).issubset(set(j)):
					c += 1
			else:
				if set(i).issubset(set(j)):
					c += 1
		dict_sup[i] = c*100/length
	return dict_sup
individual_support = find_support(k)

def Printer(frequentSet):
	print("ItemSets for input: ")
	for i in frequentSet.keys():
		print(i,)

def Assoc_rules(frequentSet):
    for item in frequentSet.keys():
        SizeOfSet=len(item)
        itemset=set(item)
        while SizeOfSet-1>0:
            combos = combinations(item, SizeOfSet-1)
            for i in combos:
                lefts=i[0]
                rights=tuple(itemset-set(i))
                item_confidence=round(current_support[item]*100/individual_support[lefts],2)
                if item_confidence >= min_c and current_support[item] >= min_s:
                	print("Association rules of the item: ", item, "\nSupport: ", current_support[item])
                	print(lefts," -->", rights, "Confidence: ", item_confidence)
                	print()
            SizeOfSet -=1

current_size = 1
f = []
while current_size <= len(items_list[0]):
	print("--------------------------------------------------------------------------------------------------------------")
	print("ItemSets with ", current_size, " items")
	print("--------------------------------------------------------------------------------------------------------------")

	if current_size == 1:
		for i in individual_support.keys():
			print(i, "support: ", individual_support[i])
			print()
	elif current_size > 1:
		current_support = find_support(list(combinations(k,current_size)))
		for i in current_support.keys():
			lefts = i[0]
			item_confidence=round(current_support[i]*100/individual_support[lefts],2)
			if current_support[i] >= min_s:
				f.append(i)
				print(i, "with support: ", current_support[i], "and Confidence: ", item_confidence)
				print()
		Assoc_rules(current_support)
	if current_size > 1:
		if len(f) > 1:
			f = []
		else:
			break
	current_size += 1

print()
print()
print("Time taken for the Brute Force is ", time.time() - start)
