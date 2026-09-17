# Implementation Plan

- [x] 1. Create comprehensive reference implementation analysis script
  - Write a detailed analysis script that extracts and documents the complete Luminet data pipeline
  - Parse the reference BlackHole class to understand initialization, parameter loading, and configuration
  - Document the step-by-step DataFrame creation process from sampling to final visualization
  - Extract and analyze the coordinate transformation pipeline including the critical `-π/2` rotation
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Analyze and document the reference sampling and physics pipeline
  - [x] 2.1 Extract and document the particle sampling methodology
    - Analyze the biased sampling strategy: `r = min_radius + max_radius * np.random.random()`
    - Document the impact parameter calculation using elliptic integrals and midpoint refinement
    - Extract the coordinate transformation process with `polar_to_cartesian_lists` and rotation
    - _Requirements: 1.1, 1.2_

  - [x] 2.2 Document the relativistic physics calculations
    - Analyze the `calc_impact_parameter` function and its elliptic integral approach
    - Document the redshift factor calculation and flux computation methods
    - Extract the apparent disk edge calculation using Isoradial objects
    - _Requirements: 1.1, 1.4_

  - [x] 2.3 Analyze the ghost image processing pipeline
    - Document the separate DataFrame creation for ghost images (n=1 parameter)
    - Extract the Y-coordinate flipping technique: `[-e for e in points_['Y']]`
    - Analyze the angle offset application: `a + np.pi` for ghost image filtering
    - _Requirements: 1.2, 3.1, 3.2_

- [-] 3. Document the reference visualization rendering hierarchy
  - [x] 3.1 Analyze the rendering order and layering system
    - Extract the background setup and color scheme (black background, 'Greys_r' colormap)
    - Document the ghost image rendering with alpha=0.5 and inner/outer region splitting
    - Analyze the direct image rendering with full opacity and apparent edge filtering
    - Document the artifact masking using `fill_between` with black color and proper zorder
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 2.2 Extract the tricontour rendering parameters
    - Document the exact tricontourf parameters: levels, nchunk, norm, cmap
    - Analyze the flux scaling formula: `(abs(fl + min_flux) / (max_flux + min_flux)) ** power_scale`
    - Extract the particle filtering logic for disk edge boundaries
    - _Requirements: 2.1, 2.2, 3.1, 3.2_

- [-] 4. Create EventHorizon vs Reference comparison analysis
  - [x] 4.1 Compare data structures and DataFrame schemas
    - Map reference columns ['X', 'Y', 'impact_parameter', 'angle', 'z_factor', 'flux_o'] to EventHorizon format
    - Analyze differences in coordinate systems and transformations
    - Document discrepancies in particle sampling and physics calculations
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 4.2 Analyze rendering method differences
    - Compare scatter plot vs tricontour rendering approaches in EventHorizon
    - Identify why scatter plots work better than tricontour in current implementation
    - Document missing artifact masking and edge boundary handling
    - Analyze coordinate transformation discrepancies affecting ghost image positioning
    - _Requirements: 3.1, 3.2, 3.3, 4.1_

  - [x] 4.3 Create visual comparison test suite
    - Generate side-by-side comparisons of reference vs EventHorizon output
    - Create test cases for different inclination angles (29°, 59°, 80°, 90°)
    - Implement automated visual difference detection and reporting
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 5. Implement targeted fixes for EventHorizon tricontour rendering
  - [ ] 5.1 Fix coordinate system alignment
    - Implement exact `-π/2` rotation in EventHorizon coordinate transformations
    - Ensure polar-to-cartesian conversion matches reference implementation
    - Verify coordinate system consistency across all visualization modes
    - _Requirements: 4.4, 5.1, 5.2_

  - [ ] 5.2 Implement proper ghost image Y-coordinate transformation
    - Add Y-coordinate flipping for ghost images in LuminetCompositor
    - Implement proper angle offset handling for ghost image filtering
    - Ensure correct layering with zorder parameters for ghost vs direct images
    - _Requirements: 3.1, 3.2, 4.4, 5.1_

  - [ ] 5.3 Fix tricontour rendering parameters and artifact masking
    - Align tricontourf parameters (levels, nchunk, norm) with reference implementation
    - Implement flux normalization matching reference formula exactly
    - Add black fill regions for triangulation artifact removal
    - Implement disk edge boundary masking using apparent edge functions
    - _Requirements: 3.1, 3.2, 3.3, 4.4, 5.1_

- [ ] 6. Create comprehensive validation and testing framework
  - [ ] 6.1 Implement numerical accuracy validation
    - Create test cases comparing impact parameter calculations with reference values
    - Validate redshift factor and flux calculations against reference implementation
    - Test coordinate transformation accuracy with known input/output pairs
    - _Requirements: 4.3, 4.4, 5.4_

  - [ ] 6.2 Implement visual accuracy validation
    - Create automated image comparison tools for photon ring definition and sharpness
    - Validate event horizon boundary positioning and black region masking
    - Test brightness distribution and flux scaling accuracy
    - Verify ghost image positioning and Y-coordinate transformation correctness
    - _Requirements: 4.1, 4.2, 4.3, 5.1, 5.2_

  - [ ] 6.3 Create performance benchmarking suite
    - Compare computation times between reference and EventHorizon implementations
    - Analyze memory usage patterns for DataFrame operations
    - Benchmark rendering performance for different visualization methods
    - _Requirements: 5.3, 5.4_

- [ ] 7. Generate comprehensive analysis report and recommendations
  - [ ] 7.1 Create detailed findings documentation
    - Document all identified discrepancies between reference and EventHorizon implementations
    - Provide specific code-level recommendations for each identified issue
    - Prioritize fixes based on visual impact and scientific accuracy
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 7.2 Create implementation guide for fixes
    - Provide step-by-step implementation instructions for each recommended fix
    - Include code examples and configuration changes needed
    - Document testing procedures to validate each fix
    - _Requirements: 5.1, 5.2, 5.3, 5.4_