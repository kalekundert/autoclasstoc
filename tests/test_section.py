#!/usr/bin/env python3

import pytest
import autoclasstoc


class ExcludeSection1(autoclasstoc.Section):
    key = 'dummy-section-1'
    title = "Dummy Section 1:"
    exclude_pattern = '__'


class ExcludeSection2(autoclasstoc.Section):
    key = 'dummy-section-2'
    title = "Dummy Section 2:"
    exclude_pattern = ['__', 'on']


class ExcludeSection3(ExcludeSection2):

    def predicate(self, name, attr, meta):
        return not self.exclude_if_match(self.exclude_pattern, name)


class ExcludeSection4(autoclasstoc.Section):
    key = 'dummy-section-2'
    title = "Dummy Section 2:"


def test_ExcludeSection1():
    names = {
        '__init__': True,
        '__len__': True,
        'foo': False,
        'bar': False,
        't__t': True
    }
    cls = ExcludeSection1('state', 'cls')

    for key, item in names.items():
        assert item == cls.exclude_if_match(cls.exclude_pattern, key)


def test_ExcludeSection2():
    names = {
        '__init__': True,
        '__len__': True,
        'foo': False,
        'bar': False,
        't__t': True,
        'on_off': True,
        'out': False
    }

    cls = ExcludeSection2('state', 'cls')
    for key, item in names.items():
        assert item == cls.exclude_if_match(cls.exclude_pattern, key)


def test_ExcludeSection3():
    names = {
        '__init__': True,
        '__len__': True,
        'foo': False,
        'bar': False,
        't__t': True,
        'on_off': True,
        'out': False
    }
    cls = ExcludeSection3('state', 'cls')
    for key, item in names.items():
        assert not item == cls.predicate(key, 'attr', 'meta')


def test_ExcludeSection4():
    names = {
        '__init__': True,
        '__len__': True,
        'foo': False,
        'bar': False,
        't__t': True,
        'on_off': True,
        'out': False
    }
    cls = ExcludeSection4('state', 'cls')
    for key, item in names.items():
        assert None == cls.exclude_if_match(cls.exclude_pattern, key)
