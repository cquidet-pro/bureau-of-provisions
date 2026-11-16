# Blender / Metal investigation — 15 November 2026

Checked while publishing the approved close-up and white strap corrections.
Machine: Apple M1 Pro, 16 GPU cores, 32 GB unified memory; macOS 27.2.1.
Blender: 5.3.0, build `02f0899d78e3`, built 10 November 2026.
No original model, global Blender preference or existing shader cache was changed.

## Evidence

- Crash reports `Blender-2026-11-15-232010.ips` and
  `Blender-2026-11-15-233639.ips` abort in Cocoa application registration /
  `GHOST_SystemCocoa::init()`. Matching macOS logs deny the sandboxed process
  access to `AGXDeviceUserClient` and graphics/window services. These launch
  failures are distinct from a Cycles GPU command failure. Run native Blender
  with graphics access even when Cycles is set to CPU, since Blender still
  initializes macOS graphics services.
- The unrestricted GPU process at 23:20 logged repeated Metal
  `mdb_txn_commit error: MDB_MAP_FULL: Environment mapsize limit reached`.
  This is a shader-cache database mapping limit, not evidence of exhausted
  disk space. The data volume had approximately 291 GiB free.
- At 23:36:06 the kernel logged `AGX: Channel error 14`, and Blender logged
  `kIOGPUCommandBufferCallbackErrorImpactingInteractivity`. Cycles identified
  `PSO_SPECIALIZED_INTERSECT.integrator_intersect_shadow`. The failing small
  draft overlapped the earlier long GPU render; concurrent GPU load is a
  possible contributor, not an established root cause.
- Saved Cycles preferences were MetalRT `AUTO`, kernel optimization `FULL`.
  The main Blender GUI was also open. No evidence reviewed establishes model
  corruption or a hardware defect.

## Isolated checks

The same native raised-straw view, one background GPU process at a time,
completed its small 435×578 / 16-sample draft with both normal settings
(5.68 s total) and `CYCLES_METAL_SPECIALIZATION_LEVEL=0` (5.53 s).
This means the GPU works on the small test and disabling specialization alone
is not a demonstrated fix. A normal 2176×2890 / up-to-128-sample GPU test was
stopped after 90 seconds without an image or a reported driver error; a timeout
is not itself proof of a crash. The same high-resolution test with specialization disabled also reached its
90-second cutoff without an image or driver error. Neither high-resolution
GPU test establishes a fix or proves a crash. The approved CPU view completed
in about 157 s.

Production uses `BOP_RENDER_DEVICE=CPU` for this release. Latest user instruction,
16 November: future jobs start on the normal GPU path and compare speed; stop
the batch at the first error, crash or apparent stall and investigate immediately
before any retry or CPU fallback. Keep the source PNG
masters and lossless deliveries; diagnose GPU execution separately from product
appearance. Do not delete live caches or disable macOS GPU protections based
solely on these warnings.

Raw macOS/Blender diagnostics are retained locally in `/private/tmp/bop-gpu-diagnostics.log`
and `/private/tmp/bop-metal-*.log`. Crash reports remain in the user's normal
DiagnosticReports directory; raw reports containing machine identifiers are
not committed.

References: [Blender GPU rendering](https://docs.blender.org/manual/en/5.1/render/cycles/gpu_rendering.html),
[Cycles Metal device implementation](https://github.com/blender/blender/blob/main/intern/cycles/device/metal/device_impl.mm).
