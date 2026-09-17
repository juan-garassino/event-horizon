# Implementation Plan

- [x] 1. Code Architecture Analysis and Duplication Detection
  - Analyze all eventHorizon modules to identify classes and functions
  - Detect and document any code duplication between modules
  - Verify proper separation of concerns and module responsibilities
  - Check for circular dependencies and import issues
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 2. Create Unified draw_blackhole Function with Mode Support
  - [x] 2.1 Implement mode parameter and routing system in draw_blackhole
    - Add mode parameter to function signature with validation
    - Create mode router to dispatch to appropriate handlers
    - Implement parameter validation for each mode
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [x] 2.2 Implement LuminetPointsHandler for points mode
    - Extract existing luminet particle visualization logic
    - Integrate with unified parameter system
    - Ensure proper physics pipeline execution
    - _Requirements: 2.1, 2.7, 2.8_

  - [x] 2.3 Implement IsoradialHandler for isoradials mode
    - Create high-resolution isoradial curve calculation
    - Implement smooth curve rendering with configurable angular resolution
    - Add coordinate transformation and rotation validation
    - _Requirements: 2.3, 3.1, 3.2, 5.1, 5.2_

  - [x] 2.4 Implement RedshiftHandler for redshift mode
    - Create redshift contour visualization through draw_blackhole
    - Integrate particle generation and physics pipeline
    - Implement proper color mapping and contour rendering
    - _Requirements: 2.4, 3.3, 4.2_

  - [x] 2.5 Implement PhotonSphereHandler for photon_sphere mode
    - Create photon sphere visualization through unified interface
    - Add event horizon and reference circle rendering
    - Ensure proper scaling and coordinate systems
    - _Requirements: 2.5, 3.4_

- [x] 3. Refactor Legacy Functions as Wrappers
  - [x] 3.1 Update plot_isoradials to use draw_blackhole
    - Modify function to call draw_blackhole with mode='isoradials'
    - Ensure all parameters are properly forwarded
    - Maintain backward compatibility
    - _Requirements: 2.6, 2.7_

  - [x] 3.2 Update plot_isoredshifts to use draw_blackhole
    - Modify function to call draw_blackhole with mode='redshift'
    - Forward all redshift-specific parameters
    - Maintain existing API compatibility
    - _Requirements: 2.6, 2.7_

  - [x] 3.3 Update plot_photon_sphere to use draw_blackhole
    - Modify function to call draw_blackhole with mode='photon_sphere'
    - Ensure proper parameter mapping
    - Maintain visual consistency
    - _Requirements: 2.6, 2.7_

  - [x] 3.4 Update plot_apparent_inner_edge to use draw_blackhole
    - Create apparent_edges mode or integrate with existing modes
    - Ensure geodesic calculations work through unified system
    - Maintain coordinate transformation accuracy
    - _Requirements: 2.6, 2.7_

- [ ] 4. Implement Enhanced Resolution and Quality System
  - [x] 4.1 Create ResolutionManager with quality presets
    - Implement draft, standard, high, and publication quality levels
    - Define angular resolution, particle count, and rendering parameters for each level
    - Add automatic parameter optimization based on mode and quality
    - _Requirements: 5.4, 6.4_

  - [x] 4.2 Enhance isoradial curve smoothness
    - Implement high angular resolution sampling (up to 1440 points)
    - Add curve smoothing and anti-aliasing techniques
    - Test different interpolation methods for optimal smoothness
    - _Requirements: 5.1, 5.2, 5.3_

  - [ ] 4.3 Optimize rendering parameters
    - Test and optimize point sizes for different visualization modes
    - Implement adaptive transparency based on particle density
    - Enhance color schemes for temperature, redshift, and flux visualization
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 5. Visual Quality and Rotation Validation
  - [ ] 5.1 Implement coordinate transformation validation
    - Create test suite for verifying coordinate system transformations
    - Test rotation accuracy for different inclination angles
    - Validate ghost image positioning and Y-coordinate flipping
    - _Requirements: 3.1, 3.2, 3.4_

  - [ ] 5.2 Test and fix rotation issues
    - Generate test visualizations at multiple inclination angles
    - Compare with reference implementations for accuracy
    - Fix any coordinate transformation or rotation bugs
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ] 5.3 Validate disk edge positioning
    - Test apparent inner and outer edge calculations
    - Verify proper lensing effects on disk boundaries
    - Ensure consistent coordinate systems across all modes
    - _Requirements: 3.5_

- [ ] 6. Comprehensive Testing Suite Implementation
  - [ ] 6.1 Create unit tests for all visualization modes
    - Test each mode through draw_blackhole function
    - Validate parameter passing and error handling
    - Test edge cases and invalid parameter combinations
    - _Requirements: 6.1, 6.2, 6.4_

  - [ ] 6.2 Implement visual quality regression tests
    - Create reference images for each visualization mode
    - Implement automated visual comparison testing
    - Test rotation accuracy and coordinate transformations
    - _Requirements: 6.1, 3.1, 3.2, 3.3_

  - [ ] 6.3 Add performance benchmarking tests
    - Measure rendering times for different quality levels
    - Test memory usage with large particle counts
    - Benchmark isoradial curve generation at high resolution
    - _Requirements: 6.3, 5.4_

  - [ ]* 6.4 Create integration tests for mode switching
    - Test switching between different visualization modes
    - Validate parameter consistency across modes
    - Test backward compatibility with legacy functions
    - _Requirements: 6.5, 2.7_

- [ ] 7. Code Quality and Duplication Elimination
  - [ ] 7.1 Remove identified code duplication
    - Consolidate duplicate functionality between modules
    - Ensure single source of truth for each calculation
    - Maintain proper module separation and interfaces
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ] 7.2 Optimize import structure and dependencies
    - Remove circular dependencies if any exist
    - Optimize import statements for better performance
    - Ensure clean module interfaces
    - _Requirements: 1.4, 1.5_

  - [ ] 7.3 Validate modular architecture
    - Confirm each module has single, well-defined responsibility
    - Test module interfaces and API consistency
    - Ensure proper error handling and parameter validation
    - _Requirements: 1.5, 6.2_

- [ ] 8. Documentation and Examples Creation
  - [ ] 8.1 Create comprehensive API documentation
    - Document all parameters for draw_blackhole function
    - Provide examples for each visualization mode
    - Document quality presets and their use cases
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 8.2 Create parameter optimization guide
    - Document optimal parameters for different use cases
    - Provide before/after examples of quality improvements
    - Create troubleshooting guide for common issues
    - _Requirements: 7.2, 7.4_

  - [ ]* 8.3 Generate performance and quality comparison reports
    - Create visual comparisons showing improvement in isoradial smoothness
    - Document performance improvements and benchmarks
    - Show rotation accuracy validation results
    - _Requirements: 7.4, 7.5_

- [ ] 9. Final Integration and Validation
  - [ ] 9.1 Perform end-to-end testing of refactored system
    - Test all visualization modes through draw_blackhole
    - Validate visual quality meets publication standards
    - Ensure performance targets are met for each quality level
    - _Requirements: 6.1, 6.3, 6.4, 6.5_

  - [ ] 9.2 Validate scientific accuracy
    - Compare outputs with reference implementations
    - Verify physics calculations are correct
    - Test edge cases and extreme parameter values
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ] 9.3 Create demonstration notebook
    - Show all visualization modes working through draw_blackhole
    - Demonstrate quality improvements and parameter optimization
    - Provide interactive examples for users
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_