//how to remove item from a list in python?
list = [2, 4, 9, 0, 4, 6, 8, 3, 43, 44]
for i in range(len(list) - 1, -1, -1):  # start at the last element, go until the first one (index 0 - the last value in the range method will not be reached), go backwards
    if list[i] % 2 == 0:
        del list[i]


