# Tested environment
The release was rebuilt and verified in the following environment:

- OS: Linux x86_64, glibc 2.41
- Python: 3.13.5
- SymPy: 1.14.0
- pdfTeX: 1.40.26, TeX Live 2025 development packaging
- latexmk: 4.86

Portable minimum:

- Python 3.10+
- SymPy 1.14.0
- A POSIX shell for the top-level runners
- `sha256sum` for checksum verification

Optional independent replays:

- Magma for the finite-field Riemann-Roch and table-generation sources
- PARI/GP for the supplied number-field polynomial checks

The Python runners set `PYTHONDONTWRITEBYTECODE=1` so verification does not add `__pycache__` directories to the extracted archive.
