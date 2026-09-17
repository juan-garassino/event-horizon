# Requirements Document

## Introduction

This specification addresses the refactoring, validation, and enhancement of the eventHorizon black hole visualization system. The project aims to ensure the codebase is well-modularized, eliminate code duplication, validate that all visualization functions work through the single `draw_blackhole` entry point, and test visual quality including rotation accuracy and rendering parameters.

## Requirements

### Requirement 1: Code Architecture Analysis and Refactoring

**User Story:** As a developer, I want to ensure the eventHorizon codebase is properly modularized and free of duplication, so that the system is maintainable and efficient.

#### Acceptance Criteria

1. WHEN analyzing the eventHorizon codebase THEN the system SHALL identify all classes and functions across all modules
2. WHEN examining code structure THEN the system SHALL detect and report any duplicated functionality between modules
3. WHEN reviewing the architecture THEN the system SHALL verify proper separation of concerns between core, math, and visualization modules
4. WHEN checking imports THEN the system SHALL ensure no circular dependencies exist
5. WHEN validating modularity THEN the system SHALL confirm each module has a single, well-defined responsibility

### Requirement 2: Unified Entry Point with Multiple Visualization Modes

**User Story:** As a user, I want `draw_blackhole` to be the single unified function that can generate different visualization types (raytracing, points/luminet, isoradials, redshift contours, etc.) based on parameters, so that I have one consistent interface for all black hole visualizations.

#### Acceptance Criteria

1. WHEN calling `draw_blackhole` with `mode='points'` THEN the system SHALL generate luminet-style particle visualization
2. WHEN calling `draw_blackhole` with `mode='raytracing'` THEN the system SHALL generate ray-traced visualization
3. WHEN calling `draw_blackhole` with `mode='isoradials'` THEN the system SHALL generate isoradial curve plots
4. WHEN calling `draw_blackhole` with `mode='redshift'` THEN the system SHALL generate redshift contour plots
5. WHEN calling `draw_blackhole` with `mode='photon_sphere'` THEN the system SHALL generate photon sphere visualization
6. WHEN using legacy functions like `plot_isoradials` THEN the system SHALL internally call `draw_blackhole` with appropriate mode parameters
7. WHEN switching between modes THEN the system SHALL maintain consistent parameter interfaces and coordinate systems
8. WHEN validating all modes THEN the system SHALL ensure proper physics and rendering for each visualization type

### Requirement 3: Visual Quality and Rotation Testing

**User Story:** As a scientist, I want to verify that black hole visualizations are correctly oriented and rotated, so that the physics representation is accurate.

#### Acceptance Criteria

1. WHEN generating isoradial plots THEN the system SHALL verify curves are properly oriented relative to the observer frame
2. WHEN testing different inclination angles THEN the system SHALL confirm visual rotation matches expected physics
3. WHEN comparing with reference implementations THEN the system SHALL validate coordinate transformations are correct
4. WHEN checking ghost image positioning THEN the system SHALL verify proper Y-coordinate flipping and orientation
5. WHEN validating disk edges THEN the system SHALL confirm apparent inner and outer edges are correctly positioned

### Requirement 4: Rendering Parameter Optimization

**User Story:** As a user, I want to test and optimize rendering parameters like point size, colors, and resolution, so that visualizations are clear and scientifically accurate.

#### Acceptance Criteria

1. WHEN testing point sizes THEN the system SHALL evaluate different dot_size_range values for optimal visibility
2. WHEN examining color schemes THEN the system SHALL test temperature, redshift, and flux-based coloring
3. WHEN adjusting transparency THEN the system SHALL optimize alpha values for direct and ghost images
4. WHEN testing background colors THEN the system SHALL verify contrast and visibility
5. WHEN evaluating power scaling THEN the system SHALL test different power_scale values for flux visualization

### Requirement 5: High-Resolution Isoradial Enhancement

**User Story:** As a researcher, I want isoradial curves to be smooth and high-resolution rather than polygonal, so that the visualization quality meets publication standards.

#### Acceptance Criteria

1. WHEN generating isoradial curves THEN the system SHALL use sufficient angular resolution to eliminate polygonal appearance
2. WHEN calculating impact parameters THEN the system SHALL use high-precision numerical methods
3. WHEN rendering curves THEN the system SHALL apply smoothing techniques for publication quality
4. WHEN testing different resolutions THEN the system SHALL provide configurable quality levels
5. WHEN comparing curve quality THEN the system SHALL demonstrate improvement over default resolution

### Requirement 6: Comprehensive Testing Suite

**User Story:** As a developer, I want comprehensive tests for all visualization functions, so that I can ensure system reliability and catch regressions.

#### Acceptance Criteria

1. WHEN running tests THEN the system SHALL validate all major visualization functions work correctly
2. WHEN testing edge cases THEN the system SHALL handle invalid parameters gracefully
3. WHEN checking performance THEN the system SHALL measure rendering times for different quality levels
4. WHEN validating outputs THEN the system SHALL verify figure and axes objects are properly created
5. WHEN testing configurations THEN the system SHALL confirm all parameter combinations work as expected

### Requirement 7: Documentation and Examples

**User Story:** As a user, I want clear documentation and examples showing how to use the refactored system, so that I can effectively create black hole visualizations.

#### Acceptance Criteria

1. WHEN accessing documentation THEN the system SHALL provide clear examples for each visualization type
2. WHEN following tutorials THEN the system SHALL demonstrate parameter optimization techniques
3. WHEN reviewing API docs THEN the system SHALL document all available parameters and their effects
4. WHEN checking examples THEN the system SHALL show before/after comparisons of improvements
5. WHEN using the system THEN the system SHALL provide helpful error messages and suggestions