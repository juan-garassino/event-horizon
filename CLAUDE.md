# evenHorizon

## What this project is
A recreation of Jean-Pierre Luminet's 1979 hand-computed image of a black hole —
one of the first scientific visualizations of what a black hole actually looks like.

The goal is to write code that simulates how light bends around a black hole
and what an accretion disk (a swirling disk of hot glowing gas) would look like
from far away.

## What's physically happening (plain language)
- A black hole warps space so severely that light doesn't travel in straight lines
- Each "ray" of light we trace actually curves around the black hole
- The glowing disk of gas appears distorted — the bottom half of the disk
  is bent up and over the top, creating a bright arc above the black hole
- One side of the disk appears much brighter than the other because the gas
  is moving toward us on one side (like a siren getting louder as it approaches)
- There's a faint "ghost" image of the disk below the black hole from light
  that went around the back

## The pipeline (in order)
1. **Geodesic integration** — trace how each light ray curves through space
   (this is the hard physics part — involves general relativity equations)
2. **Disk physics** — for each ray that hits the disk, compute how bright
   and what color that point appears (temperature, Doppler effect, gravity dimming)
3. **Rendering** — assemble all the rays into a final image

## Physics model
- Non-rotating black hole (Schwarzschild solution — the simplest case)
- All units are "geometric": G=1, c=1, M=1 (the black hole mass is 1)
- This means the event horizon (point of no return) is at radius r=2
- The disk starts at r=6 (nothing can orbit stably closer than this)
- Observer is at 80° from the disk plane — nearly edge-on, like Luminet's image

## Stack
- Python, NumPy, SciPy (for ODE integration), PIL (for saving images)
- Pure numerical simulation — no 3D engine, no GPU needed
- Can be slow — a high-quality render takes hours on CPU

## Skills available
- `eh-geodesic` — light bending / ray tracing code
- `eh-disk` — brightness and color calculations
- `eh-render` — image assembly and output
- `eh-improve` — autonomous improvement agent

## ⚡ AGENT BEHAVIOR — READ THIS FIRST

When the user says anything like:
- "this isn't working"
- "help me improve this"
- "something looks wrong"
- "fix this" / "make it better" / "it's broken"
- "the image looks wrong"

**Do NOT just give advice. Immediately launch the `eh-improve` agent.**
Run it autonomously: validate the physics, render a preview, diagnose
what's wrong, apply fixes, and report what changed.

When the user says anything like:
- "I don't understand why X"
- "explain how X works"
- "what should I do for X"

Use the skills interactively to explain and guide — don't launch the agent.

When the user says anything like:
- "write the geodesic code"
- "implement X from scratch"
- "help me build X"

Use the relevant skill (`eh-geodesic`, `eh-disk`, `eh-render`) to write
the code together interactively.

## How to ask (no jargon needed)
- "The image is all black" → launches eh-improve
- "One side isn't brighter" → launches eh-improve
- "No second image below the disk" → launches eh-improve
- "Explain why one side is brighter" → interactive, uses eh-disk
- "Write the ray tracing code" → interactive, uses eh-geodesic
- "Check if the physics is correct" → launches eh-improve

## Key numbers to remember
- Event horizon: r = 2
- Photon sphere (light can orbit): r = 3
- Inner disk edge: r = 6
- Critical impact parameter: b = 5.196 (rays closer than this fall in)
- Observer angle: 80° from disk plane
- Observer distance: very far away (500+ units)

## Current status
- Renders work end to end: `uv run python main.py --mode scatter -N 2000 --no-display` took about
  1 min on CPU (2026-11-11; other modes in README).
- Tests: `uv sync --extra dev && uv run pytest -q` (83 tests, about 12 s on CPU). pytest only
  collects `tests/` (`[tool.pytest.ini_options]` in pyproject); `scripts/dev/` holds exploratory
  scripts, not tests.
- Covered: characteristic radii (2M, 3M, 6M) and b_c = 3√3 M; the sympy expressions for eq.13 / 15 / 19;
  eq.13 impact parameters checked against an independent quadrature of the photon orbit equation;
  vectorized vs exact solver agreement; face-on isoradials are circles; b(α) = b(2π − α) symmetry;
  b ∝ M scaling; redshift limits (1/√(1−3M/r) without Doppler, √2 at the ISCO, → 1 far away,
  approaching side blueshifted); Novikov-Thorne flux zero at/inside the ISCO and peaking at r ≈ 9.55M;
  the `Isoradial` model and the lookup-table particle generator.
- Not covered yet: rendering/plotting output, Kerr (spin is stubbed), and reference values read off
  Luminet's figures (see docs/validation/scientific_validation.md § 3).

## File structure
- `eventHorizon/physics/geodesics.py` — sympy expressions for Luminet eq.13 / 15 / 19, the vectorized
  periastron root finder (`fast_root`) and `impact_parameter`.
- `eventHorizon/physics/disk_physics.py` — scalar redshift, intrinsic/observed flux and the exact
  bisection eq.13 solver used by the contour handler.
- `eventHorizon/physics/fast_geodesics.py` — lookup table b(α, r) plus vectorized redshift/flux for
  the particle renderers.
- `eventHorizon/math/` — older copy of `physics/geodesics.py` and `fast_geodesics.py` (still imported by
  `core/isoradial_model.py`); fixes must be applied to both copies.
- `eventHorizon/core/isoradial_model.py` — `Isoradial` (working); the isoredshift/grid/velocity
  models there are stubs.
- `eventHorizon/handlers/`, `visualization/`, `api.py` — render modes and the public API; `main.py` is the CLI.
- `tests/` — pytest suite; `tests/conftest.py` holds the shared eq.13 objective and the quadrature helper.

## Branches
The `lacague` branch is an incomplete OO refactor (stubbed physics) — archived, not
merged. The production-grade exact Luminet solver lives embedded in PromptPlot
(`promptplot/generative/generators.py`); porting it into a clean `eventHorizon/math`
module is a tracked follow-up.
