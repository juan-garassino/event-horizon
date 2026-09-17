# Design Document

## Overview

This design document outlines the refactoring and validation approach for the eventHorizon black hole visualization system. The design focuses on creating a unified `draw_blackhole` function that serves as the single entry point for all visualization modes, eliminating code duplication, and ensuring high-quality visual output with proper physics representation.

## Architecture

### Core Design Principles

1. **Single Entry Point**: `draw_blackhole` function handles all visualization modes through parameter selection
2. **Mode-Based Routing**: Different visualization types accessed via `mode` parameter
3. **Modular Components**: Clear separation between physics, rendering, and visualization logic
4. **Backward Compatibility**: Legacy functions maintained as thin wrappers around `draw_blackhole`
5. **Quality Configurability**: Adjustable resolution and rendering parameters for different use cases

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    draw_blackhole()                         │
│                  (Unified Entry Point)                     │
├─────────────────────────────────────────────────────────────┤
│  Mode Router                                                │
│  ├─ points (luminet)     ├─ isoradials                     │
│  ├─ raytracing           ├─ redshift                       │
│  ├─ photon_sphere       ├─ apparent_edges                 │
└─────────────────────────────────────────────────────────────┘
           │                    │                    │
┌──────────▼──────────┐ ┌───────▼────────┐ ┌────────▼────────┐
│   Physics Engine    │ │  Visualization  │ │   Rendering     │
│                     │ │     Model       │ │    Pipeline     │
│ ├─ ParticleSystem   │ │ ├─ Geodesics    │ │ ├─ Renderer     │
│ ├─ Lensing          │ │ ├─ Coordinates  │ │ ├─ Compositor   │
│ ├─ Redshift         │ │ ├─ Flux Calc    │ │ ├─ Plotter      │
│ └─ Temperature      │ │ └─ Numerical    │ │ └─ Quality      │
└─────────────────────┘ └────────────────┘ └─────────────────┘
```

## Components and Interfaces

### 1. Unified Entry Point Interface

```python
def draw_blackhole(
    mass: float = 1.0,
    inclination: float = 80.0,
    mode: str = 'points',  # NEW: Mode selection parameter
    # Mode-specific parameters
    particle_count: int = 10000,  # for 'points' mode
    radii: List[float] = None,    # for 'isoradials' mode
    redshift_levels: List[float] = None,  # for 'redshift' mode
    # Rendering parameters
    resolution: str = 'standard',  # 'draft', 'standard', 'high', 'publication'
    point_size: float = 1.0,
    color_scheme: str = 'temperature',
    # Quality parameters
    angular_resolution: int = 360,  # for smooth curves
    power_scale: float = 0.9,
    levels: int = 100,
    # Output parameters
    figsize: Tuple[int, int] = (10, 10),
    ax_lim: Tuple[float, float] = (-40, 40),
    background_color: str = 'black',
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
```

### 2. Mode Router Component

The mode router dispatches to appropriate visualization handlers:

```python
class ModeRouter:
    def route_visualization(self, mode: str, params: Dict[str, Any]) -> VisualizationHandler:
        handlers = {
            'points': LuminetPointsHandler,
            'raytracing': RayTracingHandler,
            'isoradials': IsoradialHandler,
            'redshift': RedshiftHandler,
            'photon_sphere': PhotonSphereHandler,
            'apparent_edges': ApparentEdgeHandler
        }
        return handlers[mode](params)
```

### 3. Visualization Handlers

Each mode has a dedicated handler that implements the specific visualization logic:

#### LuminetPointsHandler
- Generates particle distributions
- Applies physics pipeline (lensing, redshift, flux)
- Renders using tricontourf technique
- Handles direct and ghost images

#### IsoradialHandler
- Calculates geodesic curves for constant radii
- Uses high-resolution angular sampling
- Applies coordinate transformations
- Renders smooth curves with anti-aliasing

#### RedshiftHandler
- Generates particle grid for redshift calculation
- Computes redshift factors across disk
- Creates contour plots of constant redshift
- Applies proper color mapping

#### RayTracingHandler
- Implements full ray tracing pipeline
- Handles multiple image orders
- Applies relativistic effects
- Generates high-fidelity images

### 4. Enhanced Resolution System

```python
class ResolutionManager:
    PRESETS = {
        'draft': {
            'angular_resolution': 100,
            'particle_count': 1000,
            'levels': 50,
            'curve_smoothing': False
        },
        'standard': {
            'angular_resolution': 360,
            'particle_count': 10000,
            'levels': 100,
            'curve_smoothing': True
        },
        'high': {
            'angular_resolution': 720,
            'particle_count': 50000,
            'levels': 200,
            'curve_smoothing': True
        },
        'publication': {
            'angular_resolution': 1440,
            'particle_count': 100000,
            'levels': 500,
            'curve_smoothing': True,
            'anti_aliasing': True
        }
    }
```

## Data Models

### Enhanced Particle Data Structure

```python
@dataclass
class EnhancedParticle:
    # Spatial coordinates
    radius: float
    angle: float
    
    # Physical properties
    temperature: float
    flux: float
    redshift_factor: float
    
    # Observed coordinates (high precision)
    impact_parameter: float
    observed_x: float
    observed_y: float
    
    # Rendering properties
    brightness: float
    color: Tuple[float, float, float]
    alpha: float
    size: float
    
    # Metadata
    image_order: int
    is_visible: bool
    quality_level: str
```

### Visualization Configuration

```python
@dataclass
class VisualizationConfig:
    mode: str
    resolution: str
    physics_params: PhysicsConfig
    rendering_params: RenderingConfig
    quality_params: QualityConfig
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        pass
    
    def optimize_for_mode(self) -> None:
        """Optimize parameters for specific visualization mode"""
        pass
```

## Error Handling

### Parameter Validation System

```python
class ParameterValidator:
    def validate_mode(self, mode: str) -> bool:
        """Validate visualization mode"""
        valid_modes = ['points', 'raytracing', 'isoradials', 'redshift', 'photon_sphere']
        return mode in valid_modes
    
    def validate_physics_params(self, mass: float, inclination: float) -> bool:
        """Validate physics parameters"""
        return mass > 0 and 0 <= inclination <= 180
    
    def suggest_corrections(self, invalid_params: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest parameter corrections"""
        pass
```

### Graceful Degradation

- If high-resolution calculation fails, fall back to standard resolution
- If specific mode fails, provide alternative visualization
- If geodesic calculation fails, use approximation methods
- Provide informative error messages with suggestions

## Testing Strategy

### 1. Unit Testing Framework

```python
class TestVisualizationModes:
    def test_points_mode(self):
        """Test luminet points visualization"""
        pass
    
    def test_isoradials_mode(self):
        """Test isoradial curve generation"""
        pass
    
    def test_redshift_mode(self):
        """Test redshift contour visualization"""
        pass
    
    def test_parameter_validation(self):
        """Test parameter validation and error handling"""
        pass
```

### 2. Visual Quality Tests

```python
class TestVisualQuality:
    def test_rotation_accuracy(self):
        """Verify correct rotation for different inclinations"""
        pass
    
    def test_coordinate_transformations(self):
        """Validate coordinate system transformations"""
        pass
    
    def test_curve_smoothness(self):
        """Ensure isoradial curves are smooth, not polygonal"""
        pass
    
    def test_color_accuracy(self):
        """Validate color mapping for temperature/redshift"""
        pass
```

### 3. Performance Benchmarks

```python
class TestPerformance:
    def benchmark_resolution_levels(self):
        """Measure performance across resolution levels"""
        pass
    
    def test_memory_usage(self):
        """Monitor memory consumption for large particle counts"""
        pass
    
    def test_rendering_speed(self):
        """Measure rendering performance for different modes"""
        pass
```

### 4. Integration Tests

```python
class TestIntegration:
    def test_mode_switching(self):
        """Test switching between visualization modes"""
        pass
    
    def test_backward_compatibility(self):
        """Ensure legacy functions still work"""
        pass
    
    def test_parameter_forwarding(self):
        """Verify parameters are correctly passed between components"""
        pass
```

## Implementation Plan

### Phase 1: Architecture Refactoring
1. Create unified `draw_blackhole` function with mode parameter
2. Implement mode router and handler system
3. Refactor existing functions to use new architecture
4. Eliminate code duplication between modules

### Phase 2: Enhanced Resolution System
1. Implement high-resolution isoradial calculation
2. Add curve smoothing and anti-aliasing
3. Create resolution presets (draft, standard, high, publication)
4. Optimize numerical methods for accuracy

### Phase 3: Visual Quality Improvements
1. Fix rotation and coordinate transformation issues
2. Enhance color schemes and transparency handling
3. Improve point size and rendering parameters
4. Add visual quality validation tests

### Phase 4: Testing and Validation
1. Implement comprehensive test suite
2. Add performance benchmarks
3. Create visual regression tests
4. Validate against reference implementations

### Phase 5: Documentation and Examples
1. Update API documentation
2. Create usage examples for each mode
3. Add parameter optimization guides
4. Document best practices for different use cases

## Quality Assurance

### Code Quality Metrics
- Zero code duplication between modules
- 100% test coverage for core functions
- All visualization modes accessible through `draw_blackhole`
- Performance within acceptable bounds for each resolution level

### Visual Quality Standards
- Isoradial curves must be smooth (no polygonal appearance)
- Rotations must match expected physics for all inclination angles
- Color schemes must accurately represent physical quantities
- Ghost images must be properly oriented and positioned

### Performance Targets
- Draft quality: < 1 second
- Standard quality: < 5 seconds  
- High quality: < 30 seconds
- Publication quality: < 2 minutes

This design provides a comprehensive framework for refactoring the eventHorizon system while maintaining scientific accuracy and improving usability.