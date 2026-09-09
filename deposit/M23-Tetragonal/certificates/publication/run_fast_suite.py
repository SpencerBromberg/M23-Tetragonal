#!/usr/bin/env python3
"""Run the publication-facing fast certificates in isolated parallel workers.

Every component is executed through ``run_python_checker.py``, which preserves
its exit status and calls ``os._exit`` after a normal return.  The suite accepts
a component only when the process exits with status zero and its unique terminal
PASS marker appears in the captured output.  Parallel batches avoid cumulative
symbolic-library throttling in constrained review environments.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "certificates" / "publication" / "run_python_checker.py"

@dataclass(frozen=True)
class Check:
    marker: str
    argv: tuple[str, ...]
    env: tuple[tuple[str, str], ...] = ()

CHECKS = (
    Check("M23_EXACT_FRAME_TRANSITION_V94_PASS", ("certificates/publication/frame_transition/verify_exact_frame_transition.py",)),
    Check("M23_QPAIR_GOODFRAME_V93_PASS", ("certificates/qpair_goodframe_v93/verify_qpair_goodframe_v93.py",)),
    Check("M23_TETRAGONAL_EXACT_KERNEL_V92_PASS", ("certificates/exact_tetragonal_v93/M23_tetragonal_exact_kernel_certificate_v92.py",)),
    Check("M23_TETRAGONAL_GLOBAL_IDENTITY_METADATA_V93_PASS", ("certificates/exact_tetragonal_v93/verify_global_identity_metadata_v93.py",)),
    Check("M23_P31_GOOD_REDUCTION_INPUTS_PASS", ("certificates/good_reduction_p31/verify_good_reduction_inputs.py",)),
    Check("M23_SPECIALIZATION_UNITS_VERIFY_PASS", ("certificates/publication/p31_checks/verify_specialization_units.py",)),
    Check("M23_SYMMETRIC_CRT21_VERIFY_PASS", ("certificates/current_21prime/verify_symmetric_crt21.py",)),
    Check("M23_HELDOUT_P1013_VERIFY_PASS", ("certificates/heldout_p1013/verify_heldout_p1013.py",)),
    Check("M23_RAMIFICATION_STRUCTURE_VERIFY_PASS", ("certificates/publication/ramification/verify_ramification_structure.py",)),
    Check("M23_COMMON_DENOMINATOR_133_VERIFY_PASS", ("certificates/common_denominator_133/verify_common_denominator_133.py",)),
    Check("M23_PATCH_CERT1_PASS", ("certificates/publication/exact_closure/cert1_forbidden_triangle_lattice.py",)),
    Check("M23_PATCH_CERT2_PASS", ("certificates/publication/exact_closure/cert2_exact_adjoints_band_law.py",)),
    Check("M23_BAND_LAW_NUMERIC_PASS", ("certificates/publication/band_law/verify_band_law_ceiling.py",)),
    Check("M23_PATCH_CERT3_PASS", ("certificates/exact_closure_independent_v95/cert3_qpair_rref_binding_p100207139.py",)),
    Check("M23_VIRGIN_PRIME_SPOTCHECK_PASS", ("certificates/publication/virgin_prime_spotcheck/verify_virgin_prime_spotcheck.py",)),
    Check("M23_OUT_OF_WINDOW_SPOTCHECK_PASS", ("certificates/publication/out_of_window_spotcheck/verify_out_of_window_spotcheck.py",)),
    Check("M23_PATCH_CERT6_PASS", (
        "certificates/frame_transition_v95/cert6_frame_transition_p1013.py",
        "certificates/exact_tetragonal_v93/M23_tetragonal_polynomial_v92.txt",
        "certificates/heldout_p1013/M23_FastHeldout_p1013_user_output.log",
    )),
    Check("M23 LOWER-HEIGHT POLYNOMIAL CERTIFICATE: PASS", (
        "certificates/lower_height_specialization/extracted/M23_better_polynomial_certificate/verify_better_m23_polynomial.py",
    ), (("TERM", "xterm"),)),
)


def main() -> int:
    workers = max(1, min(int(os.environ.get("M23_FAST_WORKERS", "12")), len(CHECKS)))
    hard_timeout = float(os.environ.get("M23_FAST_COMPONENT_TIMEOUT", "300"))
    env0 = os.environ.copy()
    env0.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1", "PYTHONHASHSEED": "0"})
    temp = Path(tempfile.mkdtemp(prefix="m23-fast."))
    active: dict[int, tuple[subprocess.Popen[bytes], object, float]] = {}
    result: dict[int, tuple[int, float, Path]] = {}
    next_index = 0
    print("M23_TETRAGONAL_FAST_SUITE_BEGIN", flush=True)
    try:
        while next_index < len(CHECKS) or active:
            while next_index < len(CHECKS) and len(active) < workers:
                check = CHECKS[next_index]
                log = temp / f"{next_index:02d}.log"
                fh = log.open("wb")
                env = env0.copy(); env.update(dict(check.env))
                cmd = [sys.executable, str(HELPER), *check.argv]
                proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
                active[next_index] = (proc, fh, time.monotonic())
                next_index += 1
            time.sleep(0.05)
            now = time.monotonic()
            for idx, (proc, fh, started) in list(active.items()):
                rc = proc.poll()
                if rc is None and now - started > hard_timeout:
                    proc.kill(); rc = proc.wait()
                    fh.close()
                    raise TimeoutError(f"component timed out: {' '.join(CHECKS[idx].argv)}")
                if rc is not None:
                    fh.close()
                    result[idx] = (rc, now - started, temp / f"{idx:02d}.log")
                    del active[idx]

        failed = False
        for idx, check in enumerate(CHECKS):
            rc, elapsed, log = result[idx]
            data = log.read_text(errors="replace")
            print(f"\n===== {' '.join(check.argv)} =====")
            print(data, end="" if data.endswith("\n") else "\n")
            marker_ok = check.marker in data
            print(f"FAST_COMPONENT_ELAPSED_SEC = {elapsed:.3f}")
            if rc != 0 or not marker_ok:
                failed = True
                print(f"FAST_COMPONENT_FAIL rc={rc} marker={marker_ok}", file=sys.stderr)
        if failed:
            print("\nM23_TETRAGONAL_FAST_SUITE_FAIL", file=sys.stderr)
            return 1
        print("\nM23_TETRAGONAL_FAST_SUITE_PASS")
        return 0
    finally:
        for proc, fh, _ in active.values():
            if proc.poll() is None:
                proc.kill(); proc.wait()
            fh.close()
        shutil.rmtree(temp, ignore_errors=True)

if __name__ == "__main__":
    raise SystemExit(main())
