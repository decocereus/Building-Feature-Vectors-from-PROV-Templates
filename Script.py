# import propertyOrder and other functions
# run those functions here
# can include the execution time of the whole process

import json


def getPropertyOrder():
    f = open('files/propertyOrder.json')
    data = json.load(f)
    propertyOrder = []
    for i in data['var']:
        propertyOrder.append(i)
    f.close()
    return propertyOrder


def getBindings(depth):
    pass


def getRelations():
    with open('files/template.provn') as f:
        for line in f:
            if line.startswith('wasDerivedFrom'):
                rels = line.split('(')
                for relation in rels:
                    if relation.startswith('var'):
                        print(relation.split(':'))


if __name__ == "__main__":
    order = getPropertyOrder()
    print(order)
