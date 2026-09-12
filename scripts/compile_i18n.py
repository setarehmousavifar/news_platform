#!/usr/bin/env python
"""Compile locale/fa/LC_MESSAGES/django.po to django.mo."""
from pathlib import Path

import polib

BASE = Path(__file__).resolve().parent.parent
po_path = BASE / 'locale' / 'fa' / 'LC_MESSAGES' / 'django.po'
mo_path = BASE / 'locale' / 'fa' / 'LC_MESSAGES' / 'django.mo'

po = polib.pofile(str(po_path))
po.save_as_mofile(str(mo_path))
print(f'Compiled {mo_path} ({mo_path.stat().st_size} bytes, {len(po)} entries)')
