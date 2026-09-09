#!/usr/bin/env python3
"""Run every top-level certificate suite with explicit exit/marker checks."""
from __future__ import annotations
import os, subprocess, sys, tempfile, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SUITES=(
 ('RUN_FAST_CERTIFICATES.sh','M23_TETRAGONAL_FAST_SUITE_PASS'),
 ('RUN_EXACT_TETRAGONAL.sh','M23_EXACT_TETRAGONAL_SUITE_PASS'),
 ('RUN_GLOBAL_HEIGHT_MINIMALITY.sh','M23_GLOBAL_PGL2Q_HEIGHT_MINIMALITY_PASS'),
 ('RUN_BOUNDED_HEIGHT_SEARCH.sh','M23_BOUNDED_HEIGHT_SEARCH_PASS'),
)
def run(script:str,marker:str,timeout:float)->bool:
    env=os.environ.copy(); env.update({'PYTHONDONTWRITEBYTECODE':'1','PYTHONUNBUFFERED':'1','PYTHONHASHSEED':'0','TERM':env.get('TERM') or 'xterm'})
    with tempfile.NamedTemporaryFile(prefix='m23-suite.',delete=False) as f:
        log=Path(f.name)
        proc=subprocess.Popen(['sh',str(ROOT/script)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
    start=time.monotonic(); last=start
    try:
        while proc.poll() is None:
            time.sleep(.1); now=time.monotonic()
            if now-last>=5:
                print(f'SUITE_ACTIVE = {script}',flush=True); last=now
            if now-start>timeout:
                proc.kill(); proc.wait(); print(f'SUITE_TIMEOUT = {script}',file=sys.stderr,flush=True); return False
        data=log.read_text(errors='replace')
        print(f'\n===== {script} =====')
        print(data,end='' if data.endswith('\n') else '\n')
        ok=proc.returncode==0 and marker in data
        print(f'SUITE_ELAPSED_SEC = {time.monotonic()-start:.3f}')
        if not ok: print(f'SUITE_FAIL script={script} rc={proc.returncode} marker={marker in data}',file=sys.stderr)
        return ok
    finally:
        log.unlink(missing_ok=True)
def main()->int:
    timeout=float(os.environ.get('M23_ALL_SUITE_TIMEOUT','900'))
    print('M23_TETRAGONAL_CERTIFICATE_SUITE_BEGIN',flush=True)
    for script,marker in SUITES:
        if not run(script,marker,timeout):
            print('\nM23_TETRAGONAL_CERTIFICATE_SUITE_FAIL',file=sys.stderr)
            return 1
    print('\nM23_TETRAGONAL_CERTIFICATE_SUITE_PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
