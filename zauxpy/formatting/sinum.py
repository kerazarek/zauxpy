#!/usr/bin/env python

from collections import OrderedDict
from math import log10
from re import sub

SI_PREFIXES = OrderedDict([
	('a', -18),  # atto
	('f', -15),  # femto
	('p', -12),  # pico
	('n', -9),   # nano
	('μ', -6),   # micro
	('m', -3),   # milli
	(' ', 0),    # -
	('k', 3),    # kilo
	('M', 6),    # mega
	('G', 9),    # giga
	('T', 12),   # tera
	('P', 15),   # peta
	('E', 18)    # exa
])


def sinum(num, unit="u", coef_fmt="{:.3f}", remove_trailing_zeros=True):
	num = float(num)
	try:
		num_oom = log10(num)
	except ValueError:
		num_oom = 1
	num_pfx = [pfx for pfx in SI_PREFIXES if num_oom > SI_PREFIXES[pfx]]
	if len(num_pfx) == 0:
		raise ValueError(f"sinum({num}): num invalid or no prefix applicable")
	num_pfx = num_pfx[-1]
	num_coef = num / (10 ** SI_PREFIXES[num_pfx])
	if coef_fmt is None:
		num_coef = str(num_coef)
	else:
		num_coef = coef_fmt.format(num_coef)
	if remove_trailing_zeros:
		num_coef = sub(r"^(\s*\d+\.[1-9]*)0+\s*$", r"\1", num_coef)
		num_coef = sub(r"\.$", '', num_coef)
	num_fmtd = f"{num_coef} {num_pfx:1s}{unit}"
	return num_fmtd
