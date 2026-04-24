"""Internal package for Higgsfield FNF generation.

Top-level files in ``tools/`` are scanned for ``registry.register()`` calls;
this sub-package is invisible to that scan and exists purely as shared
plumbing for ``tools/higgsfield_generate.py`` and ``tools/higgsfield_job_status.py``.
"""
