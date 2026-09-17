# Design Document

## Overview

This analysis will systematically examine the reference Luminet implementation to understand the complete black hole visualization pipeline and identify discrepancies with the EventHorizon implementation. The focus is on understanding why scatter plots work better than tricontour rendering in EventHorizon and documenting the exact data flow from physics calculations to final visualization.

## Architecture

### Reference Luminet Data Pipeline

The reference implementation follows this sequential pipeline:

1. **Parameter Initialization** → Configuration loading from `parameters.ini`
2. **Particle Sampling** → Random sampling with bias toward disk center
3. **Impact Parameter Calculation** → Relativistic ray tracing using elliptic integrals
4. **Coordinate Transformation** → Polar to Cartesian conversion with rotation
5. **Flux and Redshift Calculation** → Relativistic effects on observed brightness
6. **Data Storage** → CSV files for direct and ghost images
7. **Visualization Rendering** → Tricontourf with specific layering and masking

### EventHorizon Current Architecture

The EventHorizon implementation uses:

1. **Unified Model Interface** → `VisualizationModel` with configuration management
2. **Particle System** → Object-oriented particle generation
3. **Physics Engine** → Modular physics calculations
4. **Ray Tracing Engine** → Separate ray tracing module
5. **Compositor** → `LuminetCompositor` for image composition

## Components and Interfaces

### Data Flow Analysis

#### Reference Luminet DataFrame Structure
```python
# Direct image DataFrame columns:
['X', 'Y', 'impact_parameter', 'angle', 'z_factor', 'flux_o']

# Ghost image DataFrame columns (separate file):
['X', 'Y', 'impact_parameter', 'angle', 'z_factor', 'flux_o']
```

#### EventHorizon DataFrame Structure
```python
# Unified particle DataFrame columns:
['radius', 'angle', 'temperature', 'flux', 'redshift_factor', 
 'impact_parameter', 'observed_alpha', 'observed_x', 'observed_y', 
 'image_order', 'brightness', 'color_r', 'color_g', 'color_b', 
 'particle_id', 'is_visible']
```

### Key Algorithmic Differences

#### 1. Sampling Strategy
- **Reference**: Biased sampling toward disk center using `r = min_radius + max_radius * np.random.random()`
- **EventHorizon**: Uniform or configurable sampling patterns

#### 2. Impact Parameter Calculation
- **Reference**: Direct elliptic integral solution with midpoint refinement
- **EventHorizon**: Modular approach through `PhysicsEngine`

#### 3. Coordinate System Handling
- **Reference**: Manual rotation by `-π/2` in `polar_to_cartesian_lists`
- **EventHorizon**: Configurable coordinate transformations

#### 4. Ghost Image Processing
- **Reference**: Separate DataFrame with Y-coordinate flipping: `[-e for e in points_['Y']]`
- **EventHorizon**: Unified handling with `image_order` field

### Rendering Pipeline Differences

#### Reference Luminet Rendering Order
1. **Background Setup** → Black background with optional reference image
2. **Ghost Image Rendering** → Split into inner/outer regions, Y-flipped, alpha=0.5
3. **Direct Image Rendering** → Full opacity, filtered by apparent outer edge
4. **Artifact Masking** → Black fill for triangulation artifacts using disk edges
5. **Edge Boundaries** → Apparent inner/outer edge calculations

#### EventHorizon Rendering Order
1. **Unified Particle Processing** → Single DataFrame with all particles
2. **Compositor Application** → `LuminetCompositor` with configuration
3. **Layered Rendering** → Based on `image_order` and `zorder`

## Data Models

### Reference Luminet Key Data Structures

#### BlackHole Class Properties
```python
self.disk_outer_edge = 50. * self.M
self.disk_inner_edge = 6. * self.M
self.disk_apparent_outer_edge  # Isoradial object
self.disk_apparent_inner_edge  # Isoradial object
self.critical_b = 3 * sqrt(3) * self.M  # Photon sphere
```

#### Particle Data Flow
1. **Sampling Loop**: `for _ in range(n_points)`
2. **Random Generation**: `r = min_radius + max_radius * np.random.random()`
3. **Impact Parameter**: `b_ = calc_impact_parameter(r, incl, theta, M, **solver_params)`
4. **Coordinate Transform**: `x, y = polar_to_cartesian_lists([b_], [theta], rotation=-π/2)`
5. **Flux Calculation**: `f_o = flux_observed(r, acc, M, redshift_factor_)`

### EventHorizon Data Models

#### Particle Object Structure
```python
@dataclass
class Particle:
    radius: float
    angle: float
    temperature: float
    flux: float
    redshift_factor: float
    impact_parameter: float
    observed_alpha: float
    observed_x: float
    observed_y: float
    image_order: int
    brightness: float
    color: Tuple[float, float, float]
    particle_id: str
    is_visible: bool
```

## Error Handling

### Reference Implementation Error Patterns
- **Non-physical Solutions**: Returns `None` for impact parameters when P ≤ 2M
- **Ellipse Fallback**: Uses `ellipse(r, alpha, incl)` for failed ray tracing
- **Boundary Filtering**: Filters particles outside apparent disk edges

### EventHorizon Error Handling
- **Configuration Validation**: Comprehensive parameter checking
- **Graceful Degradation**: Fallback to scatter plots when tricontour fails
- **Exception Handling**: Try-catch blocks in compositor

## Testing Strategy

### Analysis Methodology

#### 1. Data Pipeline Comparison
- **Input Validation**: Compare parameter loading and initialization
- **Sampling Verification**: Analyze particle distribution patterns
- **Coordinate Transformation**: Verify polar-to-cartesian conversions
- **Physics Calculations**: Compare impact parameter and flux calculations

#### 2. Rendering Comparison
- **Visual Output Analysis**: Side-by-side image comparison
- **Scatter vs Tricontour**: Identify rendering method differences
- **Edge Handling**: Compare disk boundary implementations
- **Ghost Image Processing**: Verify Y-coordinate transformation

#### 3. Performance Benchmarking
- **Computation Time**: Compare calculation speeds
- **Memory Usage**: Analyze DataFrame memory footprint
- **Rendering Performance**: Compare visualization generation times

### Validation Criteria

#### Visual Accuracy Metrics
- **Photon Ring Definition**: Sharpness and position accuracy
- **Event Horizon Boundary**: Proper black region masking
- **Brightness Distribution**: Flux scaling and normalization
- **Ghost Image Positioning**: Correct Y-coordinate transformation

#### Numerical Accuracy Metrics
- **Impact Parameter Precision**: Comparison with reference values
- **Redshift Factor Accuracy**: Relativistic calculation verification
- **Coordinate Transformation**: Spatial positioning accuracy

## Implementation Recommendations

### Priority 1: Critical Fixes

#### 1. Coordinate System Alignment
- Implement exact `-π/2` rotation in coordinate transformations
- Verify polar-to-cartesian conversion matches reference

#### 2. Ghost Image Y-Coordinate Flipping
- Apply `[-e for e in points_['Y']]` transformation in compositor
- Ensure proper layering with `zorder` parameters

#### 3. Disk Edge Filtering
- Implement apparent edge boundary functions
- Apply proper particle filtering before rendering

### Priority 2: Rendering Improvements

#### 1. Tricontour Parameter Matching
- Use identical `levels`, `nchunk`, and `norm` parameters
- Implement proper alpha blending for ghost images

#### 2. Artifact Masking
- Add black fill regions for triangulation artifacts
- Implement disk edge boundary masking

#### 3. Flux Normalization
- Match reference flux scaling: `(abs(fl + min_flux) / (max_flux + min_flux)) ** power_scale`
- Ensure consistent power scaling across direct and ghost images

### Priority 3: Data Structure Optimization

#### 1. DataFrame Column Alignment
- Map EventHorizon columns to reference format
- Ensure proper data type consistency

#### 2. Sampling Strategy Alignment
- Implement biased sampling toward disk center
- Match reference random number generation patterns

#### 3. Configuration Parameter Mapping
- Align solver parameters with reference `parameters.ini`
- Ensure consistent physical constants and tolerances