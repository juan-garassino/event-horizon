# Implementation Plan

## Current State Assessment
The eventHorizon framework has comprehensive modular structure with extracted algorithms from both bhsim and luminet references. Most core mathematical algorithms have been implemented, and the particle system is functional. The key remaining work is integration testing, pipeline completion, and user interface enhancements.

**What's Complete:**
- ✅ Modular architecture with proper separation of concerns
- ✅ Configuration system (ModelConfig) with validation
- ✅ ParticleSystem with luminet-style distribution algorithms and sample_points() method
- ✅ Comprehensive geodesic calculations extracted from bhsim (UnifiedGeodesics class)
- ✅ Physics engine with luminet flux and redshift calculations (complete pipeline methods)
- ✅ Particle renderer with luminet-style tricontourf visualization (render_frame method)
- ✅ Luminet compositor for direct/ghost image composition (compose_images method)
- ✅ Ray tracing engine structure (RayTracingEngine class)
- ✅ Mathematical expressions and lambdified functions (complete geodesics module)
- ✅ Unified visualization model integration (VisualizationModel class)
- ✅ Unified plotter with luminet-style methods (plot_luminet_style, plot_isoredshift_contours)

**What Needs Implementation:**
- ❌ Complete end-to-end pipeline integration and testing with actual luminet reference functions
- ❌ Main.py integration with new luminet functionality and command-line interface
- ❌ Comprehensive validation against reference implementations
- ❌ Working Colab-ready demonstration script
- ❌ Documentation and examples

## Task Breakdown

### Phase 1: Extract and Implement Core Mathematical Algorithms ✅ COMPLETED

- [x] 1. Extract and implement bhsim geodesic algorithms ✅ COMPLETED
  - [x] 1.1 Extract bhsim mathematical expressions ✅ COMPLETED
    - ✅ Extracted expr_u(), expr_r_inv(), expr_b(), expr_q(), expr_k(), expr_zeta_inf() from references/bhsim/core/blackhole.py
    - ✅ Extracted lambdify() function with Jacobi elliptic function support (sn, elliptic_f, elliptic_k)
    - ✅ Extracted objective() and lambda_objective() functions for periastron root finding
    - ✅ Implemented in eventHorizon/math/geodesics.py with UnifiedGeodesics class
    - _Requirements: 2.1, 2.2, 2.5_

  - [x] 1.2 Implement bhsim impact parameter calculations ✅ COMPLETED
    - ✅ Extracted impact_parameter() function from references/bhsim/core/blackhole.py
    - ✅ Extracted reorient_alpha() function for ghost image coordinate transformation
    - ✅ Implemented calculate_impact_parameter() method in eventHorizon/math/geodesics.py
    - ✅ Integrated with fast_root() and find_brackets() for efficient root finding
    - _Requirements: 3.2, 3.3, 6.2_

  - [x] 1.3 Implement bhsim flux and redshift calculations ✅ COMPLETED
    - ✅ Extracted simulate_flux() function from references/bhsim/core/blackhole.py
    - ✅ Extracted expr_one_plus_z(), expr_fs(), lambda_normalized_bolometric_flux() functions
    - ✅ Implemented complete flux simulation pipeline in eventHorizon/math/geodesics.py
    - ✅ Connected to eventHorizon/core/physics_engine.py for particle physics calculations
    - _Requirements: 3.2, 3.4, 6.2_

- [x] 2. Extract and implement luminet particle physics and sampling ✅ COMPLETED
  - [x] 2.1 Extract luminet particle sampling algorithm ✅ COMPLETED
    - ✅ Extracted sample_points() method from references/luminet/core/black_hole.py
    - ✅ Implemented LuminetDistribution with linear radius sampling (bias toward center)
    - ✅ Implemented in eventHorizon/core/particle_system.py with multiple distribution types
    - ✅ Connected to UniformDistribution, BiasedCenterDistribution, and CustomDistribution
    - _Requirements: 3.1, 5.1_

  - [x] 2.2 Extract luminet physics calculations ✅ COMPLETED
    - ✅ Extracted redshift_factor() and flux_observed() functions from references/luminet/core/black_hole.py
    - ✅ Extracted calc_impact_parameter() function from luminet reference
    - ✅ Implemented complete physics pipeline in eventHorizon/core/physics_engine.py
    - ✅ Connected to eventHorizon/math/geodesics.py for unified calculations
    - _Requirements: 3.1, 5.1, 5.2_

  - [x] 2.3 Extract luminet disk physics models ✅ COMPLETED
    - ✅ Extracted temperature and flux profile calculations from luminet reference
    - ✅ Implemented Shakura-Sunyaev disk model with exact luminet formulas
    - ✅ Enhanced ParticleSystem with luminet's accurate disk physics
    - ✅ Integrated temperature and flux calculations with proper ISCO handling
    - _Requirements: 2.1, 2.2, 2.3_

### Phase 2: Extract and Implement Visualization Techniques ✅ COMPLETED

- [x] 3. Extract and implement luminet visualization methods ✅ COMPLETED
  - [x] 3.1 Extract luminet plotting and rendering methods ✅ COMPLETED
    - ✅ Extracted plot_points() method from references/luminet/core/black_hole.py
    - ✅ Extracted plot_direct_image() and plot_ghost_image() functions for multi-image rendering
    - ✅ Implemented tricontourf() and scatter plotting techniques for dot-based visualization
    - ✅ Extracted flux scaling and power scaling techniques (power_scale parameter)
    - _Requirements: 3.1, 4.1, 4.3_

  - [x] 3.2 Implement luminet particle rendering pipeline ✅ COMPLETED
    - ✅ Implemented complete render_frame() method in eventHorizon/visualization/particle_renderer.py
    - ✅ Added luminet's dot visualization approach with tricontourf rendering
    - ✅ Implemented proper flux scaling, brightness mapping, and color schemes from luminet reference
    - ✅ Connected to eventHorizon/visualization/unified_plotter.py for integrated plotting
    - _Requirements: 3.1, 4.1, 4.3_

  - [x] 3.3 Implement luminet-style image composition ✅ COMPLETED
    - ✅ Implemented complete image composition in eventHorizon/visualization/luminet_compositor.py
    - ✅ Added proper handling of disk edges and black hole boundaries
    - ✅ Implemented support for different inclination angles and viewing perspectives
    - ✅ Integrated Y-coordinate flipping for ghost images (luminet technique)
    - _Requirements: 3.1, 4.1, 4.2_

### Phase 3: Integration and Pipeline Development ✅ COMPLETED

- [x] 4. Connect all components into working end-to-end pipeline ✅ COMPLETED
  - [x] 4.1 Fix and enhance VisualizationModel integration ✅ COMPLETED
    - ✅ Fixed VisualizationModel to call correct ParticleSystem.generate_particles() method
    - ✅ Connected ParticleSystem to VisualizationModel with proper data flow
    - ✅ Implemented proper data flow between geodesics, physics, and visualization components
    - ✅ Integrated with eventHorizon/core/ray_tracing.py for complete ray tracing pipeline
    - _Requirements: 2.1, 2.2, 6.3_

  - [x] 4.2 Implement complete physics and lensing pipeline ✅ COMPLETED
    - ✅ Connected geodesic calculations to particle lensing effects using extracted algorithms
    - ✅ Implemented apply_relativistic_effects() in PhysicsEngine using bhsim and luminet algorithms
    - ✅ Created end-to-end pipeline: particle generation → physics → geodesic ray tracing → lensing → visualization
    - ✅ Implemented execute_complete_pipeline() method for unified processing
    - _Requirements: 3.1, 3.2, 3.4_

  - [x] 4.3 Ensure backward compatibility with existing functionality ✅ COMPLETED
    - ✅ Maintained all existing isoradial and isoredshift visualization capabilities
    - ✅ Ensured eventHorizon/core/isoradial_model.py continues to work with new architecture
    - ✅ Created compatibility layer and deprecation warnings for smooth transition
    - ✅ Integrated new luminet functionality alongside existing visualization methods
    - _Requirements: 1.1, 1.3, 1.4_

### Phase 4: Integration Testing and Pipeline Completion

- [x] 5. Complete end-to-end pipeline integration and testing
  - [x] 5.1 Implement complete luminet reference functions in eventHorizon modules
    - Add draw_blackhole() function to eventHorizon package as main entry point for luminet-style visualization
    - Implement plot_points(), plot_isoradials(), plot_isoredshifts(), plot_photon_sphere() functions in appropriate modules
    - Integrate luminet's sample_points() algorithm with existing ParticleSystem for realistic matter distribution
    - Ensure all luminet functions use existing ParticleRenderer.render_frame() with tricontourf and power scaling
    - Add proper direct/ghost image composition using existing LuminetCompositor.compose_images()
    - Create modular functions that work with both local installation and Colab environment
    - Test complete pipeline: particle generation → physics → geodesic ray tracing → lensing → visualization
    - _Requirements: 3.1, 4.1, 4.3, 5.1, 5.2, 6.1_

  - [x] 5.2 Integrate luminet functionality into main.py and command-line interface
    - Add luminet visualization options to existing main.py alongside current isoradial/isoredshift plots
    - Create command-line arguments for luminet-specific parameters (particle_count, power_scale, inclination)
    - Implement plot_luminet_particles() function that uses draw_blackhole() from eventHorizon package
    - Add plot_luminet_comparison() function showing luminet vs traditional visualization side-by-side
    - Ensure all existing functionality (isoradials, isoredshifts) continues to work unchanged
    - Create unified command-line interface that supports both traditional and luminet visualization modes
    - _Requirements: 1.1, 1.3, 4.1, 4.3, 6.1, 6.5_

  - [x] 5.3 Create Colab-ready demonstration notebook as package entry point
    - Create Jupyter notebook that imports eventHorizon package and demonstrates usage like pip install
    - Show how to use draw_blackhole() and other luminet functions after importing eventHorizon
    - Include examples using eventHorizon.plot_points(), eventHorizon.plot_isoradials(), etc.
    - Add interactive widgets for parameter tuning (mass, inclination, particle count, power_scale, levels)
    - Demonstrate both local and Colab usage patterns with same import statements
    - Compare luminet particle method with traditional isoradial/isoredshift methods using package functions
    - Include performance benchmarks showing improvements over original luminet reference
    - _Requirements: 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 6.1, 6.2_

  - [x] 5.4 Validate against reference implementations
    - Create validation script comparing ParticleSystem.sample_points() output with luminet reference
    - Test PhysicsEngine flux and redshift calculations against luminet reference formulas
    - Validate UnifiedGeodesics impact parameter calculations against bhsim reference
    - Compare ParticleRenderer output quality with luminet reference visualizations
    - Ensure existing isoradial/isoredshift visualizations match previous results
    - Create regression tests to prevent future breaking changes
    - _Requirements: 2.1, 2.2, 6.3_

### Phase 5: User Interface and Quality Enhancement

- [x] 6. Create user interface and quality enhancement system
  - [x] 6.1 Enhance package interface and create comprehensive examples
    - Add convenience functions to eventHorizon.__init__.py for easy import (draw_blackhole, plot_points, etc.)
    - Create examples/ directory with standalone scripts showing different use cases
    - Implement all luminet reference functions as package methods: plot_points(), plot_isoradials(), plot_isoredshifts(), plot_photon_sphere()
    - Add parameter validation and helpful error messages to all public functions
    - Create quick-start guide showing basic usage after pip install eventHorizon
    - Ensure consistent API across all visualization methods (luminet and traditional)
    - _Requirements: 4.1, 4.2, 4.4, 5.1, 5.2, 5.3, 6.1, 6.2_

  - [x] 6.2 Implement progressive quality enhancement and presets
    - Add configurable quality levels (draft, standard, high, publication) to all visualization types
    - Create presets for different use cases (interactive, batch processing, publication)
    - Implement performance monitoring for different particle counts (1k, 10k, 100k particles)
    - Add progress monitoring for long-running geodesic calculations
    - _Requirements: 4.1, 4.2, 4.4, 5.3, 6.1, 6.2_

  - [x] 6.3 Add animation and multi-inclination support
    - Implement animation capabilities for all visualization types (not just luminet)
    - Add support for creating movie sequences showing different viewing angles
    - Create animations comparing luminet particle method vs traditional isoradial method
    - Include examples showing black hole appearance evolution with different parameters
    - _Requirements: 4.1, 4.2, 4.4, 6.1, 6.2_

### Phase 6: Documentation and Finalization

- [x] 7. Create comprehensive documentation and user guides
  - [x] 7.1 Create technical documentation for new capabilities
    - Document the particle-based visualization system and extracted algorithms
    - Create API documentation for ParticleSystem, PhysicsEngine, and ParticleRenderer
    - Document the mathematical foundations from bhsim and luminet references
    - Create developer guide for extending the particle visualization system
    - _Requirements: 2.1, 2.2, 2.5, 6.3_

  - [x] 7.2 Create user tutorials and workflow guides
    - Write step-by-step tutorial for creating luminet-style visualizations
    - Create parameter tuning guide for different black hole configurations
    - Document workflow for going from particle generation to publication-quality images
    - Provide troubleshooting guide for common geodesic calculation issues
    - _Requirements: 4.4, 5.1, 5.2, 5.3, 6.2, 6.3, 6.4_

  - [x] 7.3 Create validation and performance documentation
    - Document validation methodology against reference implementations
    - Create performance benchmarks for different particle counts and quality levels
    - Document accuracy metrics and scientific validation of results
    - Provide guidelines for scientific use and publication-quality output
    - _Requirements: 4.2, 4.3, 4.4, 6.1, 6.2, 6.3_

## Implementation Priority and Dependencies

### Critical Path (Remaining tasks in order):
1. **Phase 4 (Task 5)**: Integration testing and pipeline completion - validate extracted algorithms work together
2. **Phase 5 (Task 6)**: User interface and quality enhancement - make system usable
3. **Phase 6 (Task 7)**: Documentation and finalization - complete the implementation

### Parallel Development Opportunities:
- Tasks 5.1-5.3 can be developed in parallel (different integration aspects)
- Tasks 6.1-6.3 can be developed in parallel (different interface aspects)
- Tasks 7.1-7.3 can be developed in parallel (different documentation types)

### Key Dependencies:
- Task 5.2 (main.py integration) depends on Task 5.1 (working example)
- Task 5.3 (validation) can be done in parallel with Tasks 5.1-5.2
- All Phase 5 tasks depend on Phase 4 completion
- All Phase 6 tasks can be developed alongside Phase 5

### Current Status Summary:
- **Phases 1-3 (Tasks 1-4): ✅ COMPLETED** - All core algorithms extracted and integrated
- **Phase 4 (Task 5): 🔄 IN PROGRESS** - Need to complete integration testing
- **Phase 5 (Task 6): ⏳ PENDING** - Awaiting Phase 4 completion
- **Phase 6 (Task 7): ⏳ PENDING** - Can start alongside Phase 5

The foundation is complete with all mathematical algorithms, physics calculations, and visualization techniques extracted and implemented. The remaining work focuses on integration, user experience, and documentation to make the luminet visualization system fully functional and accessible.