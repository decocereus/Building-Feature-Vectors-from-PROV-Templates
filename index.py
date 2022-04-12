

# put it in the readme that you need to rename template, json file and the csv file another name so that it works.


# for calculation of provenance types, do i have to create a dictonary
# for each line of csv file and then count the number of occurence of each dictonary
# the function which does this calculation is called the feature vector ?


# ask about the knowledge of the reader- define everything in detail
# how to best define provenance types
# for feature vector do i have to count the frequency of each of hashmap built by the csv files - no
# ask about the design of the project - update the design and email him

# Another approach for counting the frequncey can be
# I can put the properties which are related to one another and put them in a hashmap
# and everytime I encounter another occurence of that relation then I can just
# incerease the freq in the hashmap

# to get the types of all the nodes we start at level 0, for level 0 the template gives us the type for everything.
# I have to get these types for everything like activity, entity, operation etc.
# then I have to look at the realtions so lets say that
# e2 wasDerivedFrom e1 then type1 of e2 = type0(e1) which is entity in this case

# In order to get the types for each and every node i have iterated over all of them and then create a set for each node.
# the set contains the types associated with each node.

# then we iterate over all the sets and calculate the frequency of each set. This frequency is our feature vector.

# then we are done


# for report
# get chapter 2-4 by 12th April

# goal for tomorrow
# write down the pseudo code and complete the first section of background

# write down the implementation pseudo code

# build template extractor
# templateDict = {entity: [player_before, player_after, pokestop_before, pokestop_after],
#                 activity: [operation],
#                  wasDerivedFrom: }

# def getEntities(template):
# def getActivities(template):
# def getRelations(template):
