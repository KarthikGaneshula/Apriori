import time
from itertools import combinations
min_s = int(input("Enter the minimum support: "))
min_c = int(input("Enter the minimum confidence: "))
start = time.time()
file_object = open("DataSet-1.txt", "r")
l_of_data = file_object.readlines()
allItemList = []
n_list = 0
sup_all_items_s={}

d = {}  
items_list = []
print("-------------------")
print("The following are the input transactions:")
print("-------------------")
print()

for q in l_of_data:
    q = q.replace("\n", "")
    print(q)
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

frequentSet = {}
eliminatedSet = []
print()
print("-------------------------")
print("Item Sets of size", 1)
print("-------------------------")
print()
for i in d:
    print(i,round(d[i]*100/n_list))
    if (d[i]/20)*100 >= min_s:
        frequentSet[i] = d[i]
    else:
        eliminatedSet.append(set(i))
sup_all_items_s.update(d)
l = []
for i in frequentSet.keys():
    l.append(i[0])



def find_frequent_Sets(l, elims, items_list, n):
    combos = combinations(l, n)
    support_c_dict = {}
    for i in combos:
        set_of_i = set(i)
        i = tuple(sorted(i))
        for j in items_list:
            if set_of_i.issubset(j):
                if len(elims) > 0:
                    c = 0
                    for k in elims:
                        if k.issubset(set_of_i):
                            c = 1
                            break
                    if not c:
                        if i in support_c_dict:
                            support_c_dict[i] += 1
                        else:
                            support_c_dict[i] = 1
                else:
                    if i in support_c_dict:
                        support_c_dict[i] += 1
                    else:
                        support_c_dict[i] = 1
    frequentSet_final = {}
    elim_set_final = []
    if len(support_c_dict) > 0:
        print("------------------------------")
        print("Itemsets for size: ", n)
        print("------------------------------")
        print()
        for i in support_c_dict:
            print(i,round(support_c_dict[i]*100/n_list,2))
            if (support_c_dict[i]/n_list)*100 >= min_s:
                frequentSet_final[i] = support_c_dict[i]
            else:
                elim_set_final.append(set(list(i)))
        print()
        if len(frequentSet_final) > 0:
            sup_all_items_s.update(support_c_dict)
            Assoc_rules(frequentSet_final)
            return frequentSet_final, elim_set_final
    return None,None

def Print_items(frequentSet,n):
    print("----------------------------------------")
    print("Itemsets after iteration of size: ", n)
    print("Itemset", "Support value")
    print("----------------------------------------")
    print()
    for i in frequentSet:
        print(i,round(frequentSet[i]*100/n_list,2),)
    print()    

def Assoc_rules(frequentSet):
    for item in frequentSet.keys():
        print("Association Rule for the itemset - ",item)
        print("Support","Confidence")
        SizeOfSet=len(item)
        itemset=set(item)
        while SizeOfSet-1>0:
            combos = combinations(item, SizeOfSet-1)
            for i in combos:
                left_items=i
                right_items=tuple(itemset-set(i))
                item_confidence=round(sup_all_items_s[item]*100/sup_all_items_s[left_items],2)
                if item_confidence>=min_c:
                    print(left_items,"-->",right_items,item_confidence,"Qualified")
                else:
                    print(left_items,"-->",right_items,item_confidence,"Unqualified")

            SizeOfSet -=1
        print()



print()
item_set_size = 1
while len(l) > item_set_size:
    frequentSet1, eliminatedSet1 = find_frequent_Sets(l, eliminatedSet, items_list, item_set_size + 1)
    if not frequentSet1:
        break
    listOfItems = []
    for items in list(frequentSet1.keys()):
        for i in items:
            listOfItems.append(i)
    l = list(set(listOfItems))
    eliminatedSet = eliminatedSet1
    frequentSet=frequentSet1
    item_set_size += 1
print('The Apriori algorithm now executed takes: %s ' % (time.time() - start), "seconds")