def divideArray(array, numOfColumns):
    result = list()
    reminder = list()
    for i in range(0, len(array)):
        reminder.append(array[i])
        if(((i+1) % numOfColumns) == 0):
            result.append(reminder.copy())
            reminder.clear()
    return result
