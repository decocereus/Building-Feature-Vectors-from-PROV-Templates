import json
import pprint
from collections import defaultdict, Counter
from typing import Iterable, Dict
from itertools import chain


provTypes = ['activity', 'entity', 'agent']
provRelations = ['wasDerivedFrom', 'used', 'wasInformedBy', "wasGeneratedBy",
                 'wasAttributedTo', 'wasAssociatedWith', 'actedOnBehalfOf']

SHORT_NAMES = {
    'entity': 'ent',
    'activity': 'act',
    'agent': 'agt',
    'wasDerivedFrom': 'der',
    'used': 'usd',
    'wasInformedBy': 'wib',
    "wasGeneratedBy": 'gen',
    'wasAttributedTo': 'att',
    'wasAssociatedWith': 'waw',
    'actedOnBehalfOf': 'del'

}


PROV_TYPE_DICT = {}
PROV_RELATION_DICT = {}
ADDITONAL_TYPE_DICT = {}
FingerPrint = set(SHORT_NAMES.keys())

'''Main Functions'''


def getPropertyOrder():
    f = open('files/propertyOrder.json')
    data = json.load(f)
    propertyOrder = []
    for i in data['var']:
        propertyOrder.append(i)
    f.close()
    return propertyOrder


def getAddionalTypes(currentLine):
    currentPropType = currentLine[1][4:]  # key
    for element in currentLine[2:]:
        if element != '-':
            element.strip()
            provType = element.split('=')
            if provType[0] == 'prov:type ':
                addtionalType = provType[1].strip()[5:].replace('\'', "")
                ADDITONAL_TYPE_DICT[currentPropType] = addtionalType
            else:
                continue


def getTemplateInfo():
    with open('files/template.provn') as fh:
        for line in fh:
            formattedTemplate = line.strip().replace(
                '(', ',').replace('[', "").replace(']', "").replace(')', "").split(',')
            checkType = formattedTemplate[0]
            if checkType in provTypes:
                typeToAdd = formattedTemplate[1][4:]
                PROV_TYPE_DICT[typeToAdd] = checkType
                getAddionalTypes(formattedTemplate)
            elif checkType in provRelations:
                relation = formattedTemplate[0]
                predecessor = formattedTemplate[1].strip()[4:]
                successor = formattedTemplate[2].strip()[4:]
                if relation in PROV_RELATION_DICT:
                    PROV_RELATION_DICT[relation].append(
                        [predecessor, successor])
                else:
                    PROV_RELATION_DICT[relation] = [[predecessor, successor]]
            else:
                continue


def calculateProvenanceTypes(depth=0):
    getTemplateInfo()
    lvl0Types = defaultdict(set)
    predecessors = defaultdict(set)

    propertyOrder = getPropertyOrder()

    for prop in propertyOrder:
        if prop in PROV_TYPE_DICT.keys():
            lvl0Types[prop].add((PROV_TYPE_DICT[prop], ADDITONAL_TYPE_DICT[prop]
                                 if prop in ADDITONAL_TYPE_DICT else None))

    for rel, types in PROV_RELATION_DICT.items():
        for pred, succ in types:
            predecessors[succ].add((rel, pred))

    # rel_type: [pred, succ] in provRelationType
    # succ: (rel, pred) in predecessors
    flatProvTypes = defaultdict(dict)
    flatProvTypes[0] = {node: (set(lvl0Types[node]),)
                        for node in lvl0Types}

    for k in range(1, depth+1):
        for node, types in flatProvTypes[k-1].items():
            for relation, pred in predecessors[node]:
                currentType = types + (set({relation}), )
                flatProvTypes[k][pred] = (joinFlatTypes(
                    flatProvTypes[k][pred], currentType) if pred in flatProvTypes[k] else currentType)

    return flatProvTypes


def countProvTypeFreq(flatProvTypes: Iterable) -> Dict[str, int]:

    counter = Counter(flatProvTypes)
    return {formatProvTypes(t): count for t, count in counter}


def buildFeatureVector(depth=0):
    provTypes = calculateProvenanceTypes(depth)
    print(chain.from_iterable(provLevel.values()
          for provLevel in provTypes.values()))
    return countProvTypeFreq(chain.from_iterable(provLevel.values() for provLevel in provTypes.values()))


'''Utility Functions'''


def joinFlatTypes(type1, type2):
    if type1 is None:
        return type2
    if type2 is None:
        return type1
    assert len(type1) == len(type2)
    return tuple(val1 | val2 for val1, val2 in zip(type1, type2))


def formatFingerPrint(f):
    try:
        types = sorted(SHORT_NAMES[qn] for qn in f)
    except KeyError:
        types = sorted(SHORT_NAMES[qn] for qn in f if qn in SHORT_NAMES)
        additionalTypes = sorted([qn for qn in f if qn not in SHORT_NAMES])
        types.extend(additionalTypes)
    return '[' + '|'.join(types) + ']'


def formatProvTypes(type):
    return "→".join(map(formatFingerPrint, reversed(type)))


if __name__ == "__main__":
    featureVector = buildFeatureVector(3)
    pprint.pprint(featureVector)
