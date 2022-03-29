

# put it in the readme that you need to rename template, json file and the csv file another name so that it works.


# for calculation of provenance types, do i have to create a dictonary
# for each line of csv file and then count the number of occurence of each dictonary
# the function which does this calculation is called the feature vector ?

# def featureVector(depth):
# allDicts = []
# for i in range(depth):
# currentDict = getSuccessorNodesDict(line)
# allDicts.append(currentDict)
# the calculate how many dictonaries are same


# ask about the knowledge of the reader
# how to best define provenance types
# for feature vector do i have to count the frequency of each of hashmap built by the csv files
# ask about the design of the project

# Another approach for counting the frequncey can be
# I can put the properties which are related to one another and put them in a hashmap
# and everytime I encounter another occurence of that relation then I can just
# incerease the freq in the hashmap

# lets say we have property 4 relating to prop 9
# then in the hashmap we have
# dict = {'4-9': 1, '7-9': 5}


# for design

# getPropertyOrder
