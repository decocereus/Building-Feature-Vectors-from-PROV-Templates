# read the json file and get the property order
# build successor nodes dictonary
# make sure that the dictonary can be used in other files.
import json


def getPropertyOrder():
    f = open('files/propertyOrder.json')
    data = json.load(f)
    propertyOrder = []
    for i in data['var']:
        propertyOrder.append(i)
    f.close()
    return propertyOrder


if __name__ == "__main__":
    order = getPropertyOrder()
    print(order)
