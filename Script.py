
import pprint
from collections import defaultdict, Counter
from typing import Iterable, Dict, FrozenSet
from itertools import chain
import sys
import os


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
    'actedOnBehalfOf': 'del',
    'wasInformedBy': 'wib',
    'wasStartedBy': 'wsb',
    'wasEndedBy': 'web',
    'wasInvalidatedBy': 'inv',
    'wasInfluencedBy': 'inf',
    'alternateOf': 'alt',
    'specializationOf': 'spe',
    'hadMember': 'mem',
    'mentionOf': 'men'
}


# These sets are immutable, once something has been added it cannot be removed.
FrozenSet = frozenset()
PROV_TYPE_DICT = {}
PROV_RELATION_DICT = {}
ADDITIONAL_TYPE_DICT = {}
FingerPrint = set(SHORT_NAMES.keys())

'''Main Functions'''

'''
This function grabs any additional identifiers associated with any entities, activities or agents present in the template
'''


def getAdditionalTypes(currentLine):
    currentPropType = currentLine[1][4:]  # key
    for element in currentLine[2:]:
        if element != '-':
            element.strip()
            provType = element.split('=')
            if provType[0] == 'prov:type ':
                additionalType = provType[1].strip()[5:].replace('\'', "")
                ADDITIONAL_TYPE_DICT[currentPropType] = additionalType
            else:
                continue


'''
This function extracts all important piece of information which is required for construting prov types
'''


def getTemplateInfo(path):

    provTypes = ['activity', 'entity', 'agent']
    provRelations = ['wasDerivedFrom', 'used', 'wasInformedBy', "wasGeneratedBy",
                     'wasAttributedTo', 'wasAssociatedWith', 'actedOnBehalfOf']
    assert os.path.exists(
        path), "I did not find the file at, "+str(path)
    fh = open(path, 'r+')
    print('Template found, constructing feature vector.')
    for line in fh:
        formattedTemplate = line.strip().replace(
            '(', ',').replace('[', "").replace(']', "").replace(')', "").split(',')
        checkType = formattedTemplate[0]
        if checkType in provTypes:
            typeToAdd = formattedTemplate[1][4:]
            PROV_TYPE_DICT[typeToAdd] = checkType
            getAdditionalTypes(formattedTemplate)
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
    fh.close()


'''
This function first calculates the lvl 0 prov types,
builds the predecessor dict where we store the information about the relations and all the core prov types involved.

Once that's done, we move on to calculating prov types upto the depth defined by the user.
'''


def calculateProvenanceTypes(path, depth=0):
    getTemplateInfo(path)  # adds data to the global variables
    lvl0Types = defaultdict(set)
    predecessors = defaultdict(set)

    for prop in PROV_TYPE_DICT.keys():
        if prop in PROV_TYPE_DICT.keys():
            lvl0Types[prop].add((PROV_TYPE_DICT[prop], ADDITIONAL_TYPE_DICT[prop]
                                 if prop in ADDITIONAL_TYPE_DICT else None))

    for rel, types in PROV_RELATION_DICT.items():
        for pred, succ in types:
            predecessors[succ].add((rel, pred))

    # rel_type: [pred, succ] in provRelationType
    # succ: (rel, pred) in predecessors
    flatProvTypes = defaultdict(dict)
    # building lvl 0 types
    flatProvTypes[0] = {node: (frozenset(lvl0Types[node]),)
                        for node in lvl0Types}

    for k in range(1, depth+1):
        # important note, we start from 1 and not 0 since we have already built the lvl0 types
        for node, types in flatProvTypes[k-1].items():
            for relation, pred in predecessors[node]:
                currentType = types + (frozenset({relation}), )
                flatProvTypes[k][pred] = (joinFlatTypes(
                    flatProvTypes[k][pred], currentType) if pred in flatProvTypes[k] else currentType)

    return flatProvTypes


'''Counting and formatting each prov type's frequency'''


def countProvTypeFreq(flatProvTypes: Iterable) -> Dict[str, int]:
    counter = Counter(flatProvTypes)
    return {formatProvTypes(t): count for t, count in counter.items()}


'''The driver function for the whole script'''


def buildFeatureVector(path, depth=0):
    provTypes = calculateProvenanceTypes(path, depth)
    return countProvTypeFreq(chain.from_iterable(provLevel.values() for provLevel in provTypes.values()))


'''Utility Functions'''


'''
This functions joins two prov types of equal lengths.
It serves the purpose of joining types which are of equal length.
Through this function we can create different frozen sets for relations and core prov types.

These functions are taken from 'https://github.com/trungdong/provenance-kernel-evaluation/blob/master/scripts/flatprovenancetypes.py'
'''


def joinFlatTypes(type1, type2):
    if type1 is None:
        return type2
    if type2 is None:
        return type1
    assert len(type1) == len(type2)
    return tuple(val1 | val2 for val1, val2 in zip(type1, type2))


'''These function are purely for formatting the prov types in more readable way.'''


def formatFingerPrint(f):
    try:
        types = sorted(SHORT_NAMES[qn] for qn in f)
    except KeyError:
        types = sorted(SHORT_NAMES[qn] for qn in f if qn in SHORT_NAMES)
        additionalTypes = sorted([qn for qn in f if qn not in SHORT_NAMES])
        types.extend(additionalTypes)
    return '[' + '|'.join(str(t) for t in types) + ']'


def formatProvTypes(type):
    return "→".join(map(formatFingerPrint, reversed(type)))


if __name__ == "__main__":
    path = str(input('Path: '))
    depth = int(input('depth: '))
    featureVector = buildFeatureVector(path, depth)
    print('')
    print('Feature vector: ')
    pprint.pprint(featureVector)
