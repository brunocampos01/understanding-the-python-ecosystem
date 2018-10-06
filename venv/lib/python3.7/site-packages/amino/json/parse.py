#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x1c09273d

# Compiled with Coconut version 1.3.0 [Dead Parrot]

# Coconut Header: -------------------------------------------------------------

from __future__ import generator_stop
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

import json  # line 1
from typing import Any  # line 2

from amino import Either  # line 4
from amino import Left  # line 4
from amino import Lists  # line 4
from amino import Map  # line 4
from amino import Try  # line 4
from amino.json.data import Json  # line 5
from amino.json.data import JsonArray  # line 5
from amino.json.data import JsonScalar  # line 5
from amino.json.data import JsonObject  # line 5


def to_json(a: 'Any') -> 'Json':  # line 8
    _coconut_match_to = a  # line 9
    _coconut_match_check = False  # line 9
    if _coconut.isinstance(_coconut_match_to, (list, tuple)):  # line 9
        a = _coconut_match_to  # line 9
        _coconut_match_check = True  # line 9
    if _coconut_match_check:  # line 9
        result = JsonArray(Lists.wrap(a) / to_json)  # line 11
    if not _coconut_match_check:  # line 12
        if _coconut.isinstance(_coconut_match_to, dict):  # line 12
            a = _coconut_match_to  # line 12
            _coconut_match_check = True  # line 12
        if _coconut_match_check:  # line 12
            result = JsonObject(Map(a).valmap(to_json))  # line 13
    if not _coconut_match_check:  # line 14
        a = _coconut_match_to  # line 14
        _coconut_match_check = True  # line 14
        if _coconut_match_check:  # line 14
            result = JsonScalar(a)  # line 15
    return result  # line 16


def parse_json(payload: 'str') -> 'Either[str, Json]':  # line 19
    return Try(json.loads, payload) / to_json  # line 20
