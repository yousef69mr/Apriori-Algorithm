import pandas as pd
import numpy as np
from itertools import combinations


def clean_dataset(dataset):
    cleaned_dataset = dataset.iloc[:, 1:]
    columns = np.array(cleaned_dataset.columns)  # ['Item 1' 'Item 2' 'Item 3']

    # print(columns)
    for column in columns:
        cleaned_dataset[column] = cleaned_dataset[column].str.upper().str.strip().str.replace(" ", "")

    return cleaned_dataset


def reduce_data_size(dataset):
    # remove duplicate rows
    reduced_dataset = dataset.drop_duplicates()
    # remove irrelevant columns
    reduced_dataset = reduced_dataset.iloc[:, 2:]

    return reduced_dataset  # ['Transaction Number','Item 1' 'Item 2' 'Item 3']


def unique_items(dataset):
    items = set(dataset.to_numpy().flatten())
    # print(items)
    return sorted(items)


def calculate_support_dictionary(data, min_support):
    # data = np.array(dataset)

    # create a dictionary of items with their supports
    items_support = {}
    for transaction in data:
        for item in transaction:
            # # same term but space between
            # if item.replace(" ", "") in items_support:
            #     item = item.replace(" ", "")
            if item in items_support:
                items_support[item] += 1
            else:
                items_support[item] = 1
    # print(items_support)
    # filter out items with support less than minimum support
    filtered_items_support = {frozenset({key}): value for key, value in items_support.items() if value >= min_support}
    # print(filtered_items_support)
    return filtered_items_support


def print_level(items_support, num_of_pairs):
    print("/*************************/")
    print(f'=> level {num_of_pairs} :')
    for key, value in items_support.items():
        print(f'{list(key)} : {value}')
    print("/*************************/")


def calculate_frequent_items(first_level, data, min_support_count):

    previous_level = first_level
    position = 1
    for count in range(2, 1000):

        # Get the list of items with count equal to the current level
        # generating pairs
        new_candidates = set()
        temp = list(previous_level)
        for i in range(0, len(temp)):
            for j in range(i + 1, len(temp)):
                t = temp[i].union(temp[j])
                if len(t) == count:
                    new_candidates.add(temp[i].union(temp[j]))
        new_candidates = list(new_candidates)

        # print(new_candidates)

        # Count the occurrence of each item
        item_count = {}
        for item in new_candidates:
            item_count[item] = 0
            for transaction in data:
                temp = set(transaction)
                if item.issubset(temp):
                    item_count[item] += 1

        # print_level(item_count, count)

        # Get the list of items with support greater than or equal to the support count
        level = {}
        for item in item_count:
            if item_count[item] >= min_support_count:
                level[item] = item_count[item]

        # Break if there are no items in the current level
        if len(level) == 0:
            return position, previous_level

        print_level(level, count)

        # Set the previous level to the current level
        previous_level = level
        position = count


def calculate_association_rules(level, data, min_confidence):
    for item_set in level:
        # Get the combinations of the item
        combinations_list = [frozenset(q) for q in combinations(item_set, len(item_set) - 1)]

        print(f'Frequent Item Set: {list(item_set)}: {level[item_set]}\nAssociation Rules:')

        # # Calculate the maximum confidence
        # max_confidence = 0

        # 2 pairs
        if len(combinations_list) == 2:
            a = combinations_list[0]
            b = item_set - a
            ab = item_set
            support_ab = 0
            support_a = 0
            support_b = 0
            for transaction in data:
                temp = set(transaction)
                if a.issubset(temp):
                    support_a += 1
                if b.issubset(temp):
                    support_b += 1
                if ab.issubset(temp):
                    support_ab += 1
            temp1 = (support_ab / support_a) * 100
            # if temp1 > max_confidence and temp1 >= (min_confidence * 100):
            #     max_confidence = temp1
            temp2 = (support_ab / support_b) * 100
            # if temp2 > max_confidence and temp2 >= (min_confidence * 100):
            #     max_confidence = temp2
            if temp1 >= (min_confidence * 100):
                print(f'{list(a)} -> {list(b)} = {temp1}%')
            if temp2 >= (min_confidence * 100):
                print(f'{list(b)} -> {list(a)} = {temp2}%')
        else:
            # 3 pairs or more
            for a in combinations_list:
                b = item_set - a
                ab = item_set
                support_ab = 0
                support_a = 0
                support_b = 0
                for transaction in data:
                    temp = set(transaction)
                    if a.issubset(temp):
                        support_a += 1
                    if b.issubset(temp):
                        support_b += 1
                    if ab.issubset(temp):
                        support_ab += 1
                temp1 = (support_ab / support_a) * 100
                # if temp1 > max_confidence and temp1 >= (min_confidence * 100):
                #     max_confidence = temp1
                temp2 = (support_ab / support_b) * 100
                # if temp2 > max_confidence and temp2 >= (min_confidence * 100):
                #     max_confidence = temp2

                if temp1 >= (min_confidence * 100):
                    print(f'{list(a)} -> {list(b)} = {temp1}%')
                if temp2 >= (min_confidence * 100):
                    print(f'{list(b)} -> {list(a)} = {temp2}%')

        # # Print the items with maximum confidence
        # curr = 1
        # print("choosing:", end=' ')
        # for a in combinations_list:
        #     b = item_set - an
        #     ab = item_set
        #     support_ab = 0
        #     support_a = 0
        #     support_b = 0
        #     for transaction in data:
        #         temp = set(transaction)
        #         if a.issubset(temp):
        #             support_a += 1
        #         if b.issubset(temp):
        #             support_b += 1
        #         if ab.issubset(temp):
        #             support_ab += 1
        #     temp = (support_ab / support_a) * 100
        #     if temp == max_confidence and temp >= (min_confidence * 100):
        #         print(curr, end=' ')
        #     curr += 1
        #     temp = (support_ab / support_b) * 100
        #     if temp == max_confidence and temp >= (min_confidence * 100):
        #         print(curr, end=' ')
        #     curr += 1
        print()
        print()


def run():
    dataset = pd.read_excel('CoffeeShopTransactions.xlsx')
    # print(dataset)
    # reduce dataset dimensions
    reduced_dataset = reduce_data_size(dataset)
    # print(reduced_dataset)
    # print(reduced_dataset.info())
    # clean dataset
    cleaned_dataset = clean_dataset(reduced_dataset)
    # print(cleaned_dataset)
    items = unique_items(cleaned_dataset)
    print(items)
    while True:

        min_support_percentage = float(input("Enter minimum support [0 -> 1] : "))
        min_support_count = int(len(cleaned_dataset) * min_support_percentage)
        print("Minimum support count : ", min_support_count)
        min_confidence = float(input("Enter minimum confidence [0 -> 1] : "))

        data = np.array(cleaned_dataset)
        try:
            level_1 = calculate_support_dictionary(data, min_support_count)
            print_level(level_1, 1)
            position, level = calculate_frequent_items(level_1, data, min_support_count)

            print("# Result :")
            print_level(level, position)

            print("/*************************/")
            print("Minimum Confidence : ", f'{min_confidence * 100}%')
            print("/*************************/")
            calculate_association_rules(level, data, min_confidence)

        except Exception as e:
            print("############################")
            print(f'Error : {e}')
            print("############################")


if __name__ == '__main__':
    run()
