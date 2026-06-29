"""Meridian J.D. evaluation harness (docs/contracts.md section 7).

Produces the eval result records (7.2), the aggregate report (7.3), and the
dashboard feed (7.4) the UI reads. Runs deterministically under MJD_PROFILE=ci
against the mock providers and the file index, so CI numbers are byte-stable.
"""

from __future__ import annotations
