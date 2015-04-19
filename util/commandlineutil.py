__author__ = 'tangz'

_PERIOD_RANGE_INDICATOR = ":"
_COMMA_SEPARATOR = ","

def parse_state_str(states_str):
    split_strs = states_str.strip().lstrip('[').rstrip(']').split(_COMMA_SEPARATOR)
    return [state_str.strip() for state_str in split_strs]

def parse_periods(periods_str):
    if _PERIOD_RANGE_INDICATOR in periods_str:
        return _parse_period_range(periods_str)
    else:
        return _parse_enumerated_periods(periods_str)

def _parse_period_range(period_range_str):
    split_strs = period_range_str.strip().split(_PERIOD_RANGE_INDICATOR)
    init_per = int(split_strs[0].strip())
    fin_per = int(split_strs[1].strip())
    return range(init_per, fin_per + 1)

def _parse_enumerated_periods(period_enum_str):
    split_strs = period_enum_str.strip().split(_COMMA_SEPARATOR)
    return [int(int_str.strip()) for int_str in split_strs]