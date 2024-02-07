from __future__ import print_function

import pytest
from parserator.training import readTrainingData

from usaddress import GROUP_LABEL, parse


def load_data(xml_file: str) -> list[tuple[str, list[tuple[str, str]]]]:
    return list(readTrainingData([xml_file], GROUP_LABEL))


def parse_case(case):
    address_text, components = case
    labels_true = [label for token, label in components]
    labels_pred = [label for token, label in parse(address_text)]
    return address_text, labels_pred, labels_true


def idfn(case: tuple[str, list[tuple[str, str]]]):
    return case[0]


@pytest.mark.parametrize(
    "case",
    load_data("measure_performance/test_data/simple_address_patterns.xml"),
    ids=idfn,
)
def test_simple(case):
    # these are simple address patterns
    address_text, labels_pred, labels_true = parse_case(case)
    assert_equals(address_text, labels_pred, labels_true)


@pytest.mark.parametrize(
    "case",
    load_data("measure_performance/test_data/labeled.xml"),
    ids=idfn,
)
def test_all(case):
    # for making sure that performance isn't degrading
    # from now on, labeled examples of new address formats
    # should go both in training data & test data
    address_text, labels_pred, labels_true = parse_case(case)
    assert_equals(address_text, labels_pred, labels_true)


@pytest.mark.parametrize(
    "case",
    load_data("measure_performance/test_data/synthetic_osm_data.xml"),
    ids=idfn,
)
def test_synthetic_addresses(case):
    address_text, labels_pred, labels_true = parse_case(case)
    assert_equals(address_text, labels_pred, labels_true)


@pytest.mark.parametrize(
    "case",
    load_data("measure_performance/test_data/us50_test_tagged.xml"),
    ids=idfn,
)
def test_us50(case):
    address_text, labels_pred, labels_true = parse_case(case)
    assert_almost_equals(address_text, labels_pred, labels_true)


def assert_equals(addr, labels_pred, labels_true):
    prettyPrint(addr, labels_pred, labels_true)
    assert labels_pred == labels_true


def assert_almost_equals(addr, labels_pred, labels_true):
    labels = []
    fuzzy_labels = []
    for label in labels_pred:
        if label.startswith("StreetName"):
            fuzzy_labels.append("StreetName")
        elif label.startswith("AddressNumber"):
            fuzzy_labels.append("AddressNumber")
        elif label == ("Null"):
            fuzzy_labels.append("NotAddress")
        else:
            fuzzy_labels.append(label)
    for label in labels_true:
        labels.append(label)
    prettyPrint(addr, fuzzy_labels, labels)

    assert fuzzy_labels == labels


def prettyPrint(addr, predicted, true):
    print("ADDRESS:    ", addr)
    print("pred:       ", predicted)
    print("true:       ", true)
