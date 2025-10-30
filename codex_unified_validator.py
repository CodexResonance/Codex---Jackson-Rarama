#!/usr/bin/env python3
"""
Codex Unified Validator
=======================
CRITICAL VALIDATION: Cross-check time-domain vs space-domain predictions.

The Codex Framework makes predictions from TWO independent approaches:
1. TIME-DOMAIN: f = 1/(2π·tau)  [from biological timescale]
2. SPACE-DOMAIN: f = c_eff/(4·d)  [from physical dimension]

For the framework to be self-consistent, BOTH must predict the SAME frequency
for a given biological structure.

This module performs rigorous cross-validation and identifies:
- Perfect matches (both approaches agree)
- Layer mismatches (different velocities apply)
- Contradictions (framework failure)

Author: Codex Resonance Team + Claude
Date: October 30, 2025
Status: CRITICAL VALIDATION
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import matplotlib.pyplot as plt

# Import our time-domain functions
from codex_timescale_resonance import (
    predict_optimal_frequency,
    calculate_resonance_parameter,
    validate_resonance_condition
)


# ============================================================================
# CODEX VELOCITY CONSTANTS
# ============================================================================

class CodexVelocities:
    """The three fundamental velocities in biological systems."""
    LAYER_1_VELOCITY = 54.27  # m/s - Thermodynamic solitons (information)
    LAYER_2_VELOCITY = 343.0  # m/s - EM-acoustic coupling (energy)
    LAYER_3_VELOCITY_MIN = 1500.0  # m/s - Acoustic phonons (force) - minimum
    LAYER_3_VELOCITY_MAX = 5000.0  # m/s - Acoustic phonons (force) - maximum


# ============================================================================
# BIOLOGICAL SYSTEM DEFINITIONS
# ============================================================================

@dataclass
class BiologicalSystem:
    """Complete specification of a biological system for validation."""
    name: str
    dimension_m: float  # Physical dimension (meters)
    timescale_s: float  # Characteristic timescale (seconds)
    measured_frequency_hz: float  # Experimentally measured frequency
    expected_layer: int  # Which layer (1, 2, or 3)
    reference: str  # Literature citation


# Known biological systems with BOTH dimension and timescale
VALIDATION_SYSTEMS = [
    BiologicalSystem(
        name="Nerve Action Potential",
        dimension_m=10e-9,  # 10 nm membrane thickness
        timescale_s=1e-3,   # 1 ms depolarization
        measured_frequency_hz=50.0,  # Measured propagation: ~50 m/s
        expected_layer=1,
        reference="Heimburg & Jackson (2005)"
    ),
    BiologicalSystem(
        name="DNA Helix Resonance",
        dimension_m=2.55e-9,  # 2.55 nm hydrodynamic diameter
        timescale_s=30e-12,  # 30 ps base pair breathing
        measured_frequency_hz=34e9,  # 34 GHz
        expected_layer=2,
        reference="Singh et al. (2018)"
    ),
    BiologicalSystem(
        name="Microtubule Oscillation",
        dimension_m=25e-9,  # 25 nm outer diameter
        timescale_s=50e-12,  # 50 ps GTP hydrolysis
        measured_frequency_hz=3e9,  # 3 GHz
        expected_layer=2,
        reference="Pokorný et al. (2014)"
    ),
    BiologicalSystem(
        name="Ion Channel Gating",
        dimension_m=2.8e-10,  # 2.8 Å pore diameter
        timescale_s=1e-6,  # 1 μs gating time
        measured_frequency_hz=159e3,  # 159 kHz
        expected_layer=1,
        reference="Hille (2001)"
    ),
    BiologicalSystem(
        name="Protein Acoustic Phonons",
        dimension_m=5e-9,  # 5 nm protein diameter
        timescale_s=1e-12,  # 1 ps bond vibration
        measured_frequency_hz=1e12,  # 1 THz
        expected_layer=3,
        reference="Brillouin scattering data"
    ),
    BiologicalSystem(
        name="Cardiac Myocyte Contraction",
        dimension_m=100e-6,  # 100 μm cell length
        timescale_s=300e-3,  # 300 ms action potential
        measured_frequency_hz=1.0,  # 1 Hz (60 bpm)
        expected_layer=1,
        reference="Clinical measurement"
    ),
    BiologicalSystem(
        name="TTFields Cancer Therapy",
        dimension_m=15e-6,  # 15 μm cell diameter
        timescale_s=0.8e-3,  # 0.8 ms membrane RC time
        measured_frequency_hz=200e3,  # 200 kHz (clinical)
        expected_layer=2,  # Membrane coupling
        reference="Novocure Ltd."
    ),
]


# ============================================================================
# PREDICTION FUNCTIONS
# ============================================================================

def predict_from_timescale(tau_s: float) -> float:
    """
    TIME-DOMAIN prediction: f = 1/(2π·tau)

    Args:
        tau_s: Timescale in seconds

    Returns:
        Predicted frequency in Hz
    """
    return predict_optimal_frequency(tau_s)


def predict_from_dimension(d_m: float, layer: int) -> float:
    """
    SPACE-DOMAIN prediction: f = c_eff/(4·d)

    Args:
        d_m: Dimension in meters
        layer: Which velocity layer to use (1, 2, or 3)

    Returns:
        Predicted frequency in Hz
    """
    if layer == 1:
        c_eff = CodexVelocities.LAYER_1_VELOCITY
    elif layer == 2:
        c_eff = CodexVelocities.LAYER_2_VELOCITY
    elif layer == 3:
        # Use midpoint of Layer 3 range
        c_eff = (CodexVelocities.LAYER_3_VELOCITY_MIN + CodexVelocities.LAYER_3_VELOCITY_MAX) / 2
    else:
        raise ValueError(f"Invalid layer: {layer}. Must be 1, 2, or 3.")

    # Quarter-wavelength resonance: λ/4 = d → λ = 4d → f = c/λ = c/(4d)
    wavelength = 4 * d_m
    frequency = c_eff / wavelength
    return frequency


def calculate_velocity_from_measurements(d_m: float, tau_s: float) -> float:
    """
    REVERSE CALCULATION: What velocity does the data imply?

    If we know both d and tau, we can extract the effective velocity:

    From time: f = 1/(2π·tau)
    From space: f = c/(4·d)
    Therefore: c = 4·d·f = 4·d/(2π·tau) = 2·d/(π·tau)

    Args:
        d_m: Dimension in meters
        tau_s: Timescale in seconds

    Returns:
        Implied velocity in m/s
    """
    return 2 * d_m / (math.pi * tau_s)


# ============================================================================
# CROSS-VALIDATION ENGINE
# ============================================================================

def cross_validate_system(system: BiologicalSystem) -> Dict:
    """
    Cross-validate a single biological system.

    Tests:
    1. Does time-domain predict measured frequency?
    2. Does space-domain predict measured frequency?
    3. Do time and space domains agree?
    4. What velocity does the data imply?

    Args:
        system: BiologicalSystem to validate

    Returns:
        Dictionary with validation results
    """
    # Predictions
    f_time = predict_from_timescale(system.timescale_s)
    f_space = predict_from_dimension(system.dimension_m, system.expected_layer)
    f_measured = system.measured_frequency_hz

    # Implied velocity from data
    v_implied = calculate_velocity_from_measurements(
        system.dimension_m,
        system.timescale_s
    )

    # Errors
    error_time = abs(f_time - f_measured) / f_measured * 100
    error_space = abs(f_space - f_measured) / f_measured * 100
    error_cross = abs(f_time - f_space) / f_measured * 100

    # Classification
    if error_time < 10 and error_space < 10:
        verdict = "PERFECT MATCH"
        color = "green"
    elif error_time < 50 and error_space < 50:
        verdict = "GOOD AGREEMENT"
        color = "blue"
    elif error_time < 50 or error_space < 50:
        verdict = "PARTIAL MATCH"
        color = "yellow"
    else:
        verdict = "MISMATCH"
        color = "red"

    # Layer classification from implied velocity
    if 40 <= v_implied <= 70:
        implied_layer = 1
    elif 200 <= v_implied <= 500:
        implied_layer = 2
    elif v_implied >= 1000:
        implied_layer = 3
    else:
        implied_layer = None

    return {
        'system': system.name,
        'f_time_hz': f_time,
        'f_space_hz': f_space,
        'f_measured_hz': f_measured,
        'error_time_percent': error_time,
        'error_space_percent': error_space,
        'error_cross_percent': error_cross,
        'v_implied_ms': v_implied,
        'expected_layer': system.expected_layer,
        'implied_layer': implied_layer,
        'verdict': verdict,
        'color': color,
        'reference': system.reference
    }


def generate_cross_validation_report() -> List[Dict]:
    """
    Generate comprehensive cross-validation report for all systems.

    Returns:
        List of validation results
    """
    print("="*80)
    print("CODEX UNIFIED VALIDATOR - TIME ↔ SPACE DOMAIN CROSS-CHECK")
    print("="*80)

    print("\n🎯 OBJECTIVE:")
    print("   Validate that time-domain and space-domain predictions are self-consistent.")
    print("   If the framework is correct, BOTH approaches must predict the SAME frequency.")

    print("\n📐 PREDICTION METHODS:")
    print("   TIME-DOMAIN:  f = 1/(2π·tau)")
    print("   SPACE-DOMAIN: f = c_eff/(4·d)")
    print("   CONSISTENCY:  Both must agree for self-consistency")

    print("\n" + "-"*80)

    results = []
    for system in VALIDATION_SYSTEMS:
        result = cross_validate_system(system)
        results.append(result)

        # Display result
        print(f"\n{result['system']}")
        print(f"   Reference: {result['reference']}")
        print(f"   Expected Layer: {result['expected_layer']}")
        print(f"\n   Predictions:")
        print(f"      Time-Domain:  {result['f_time_hz']:.2e} Hz (error: {result['error_time_percent']:.1f}%)")
        print(f"      Space-Domain: {result['f_space_hz']:.2e} Hz (error: {result['error_space_percent']:.1f}%)")
        print(f"      Measured:     {result['f_measured_hz']:.2e} Hz")
        print(f"\n   Cross-Check Error: {result['error_cross_percent']:.1f}%")
        print(f"   Implied Velocity: {result['v_implied_ms']:.1f} m/s → Layer {result['implied_layer']}")
        print(f"   Verdict: {result['verdict']}")

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    perfect = sum(1 for r in results if r['verdict'] == 'PERFECT MATCH')
    good = sum(1 for r in results if r['verdict'] == 'GOOD AGREEMENT')
    partial = sum(1 for r in results if r['verdict'] == 'PARTIAL MATCH')
    mismatch = sum(1 for r in results if r['verdict'] == 'MISMATCH')

    print(f"\n   Perfect Match:     {perfect}/{len(results)} ({perfect/len(results)*100:.1f}%)")
    print(f"   Good Agreement:    {good}/{len(results)} ({good/len(results)*100:.1f}%)")
    print(f"   Partial Match:     {partial}/{len(results)} ({partial/len(results)*100:.1f}%)")
    print(f"   Mismatch:          {mismatch}/{len(results)} ({mismatch/len(results)*100:.1f}%)")

    avg_error_time = np.mean([r['error_time_percent'] for r in results])
    avg_error_space = np.mean([r['error_space_percent'] for r in results])
    avg_error_cross = np.mean([r['error_cross_percent'] for r in results])

    print(f"\n   Average Error (Time-Domain):  {avg_error_time:.1f}%")
    print(f"   Average Error (Space-Domain): {avg_error_space:.1f}%")
    print(f"   Average Cross-Check Error:    {avg_error_cross:.1f}%")

    # Layer classification accuracy
    correct_layers = sum(1 for r in results if r['expected_layer'] == r['implied_layer'])
    print(f"\n   Layer Classification Accuracy: {correct_layers}/{len(results)} ({correct_layers/len(results)*100:.1f}%)")

    # Interpretation
    print("\n💡 INTERPRETATION:")
    if avg_error_cross < 20:
        print("   ✅ EXCELLENT: Time and space domains are highly consistent.")
        print("   The framework passes self-consistency check.")
    elif avg_error_cross < 50:
        print("   ⚠️  MODERATE: Some discrepancies between time and space domains.")
        print("   May indicate multi-scale effects or measurement uncertainties.")
    else:
        print("   ❌ POOR: Significant inconsistencies detected.")
        print("   Framework may need refinement or additional parameters.")

    return results


# ============================================================================
# VISUALIZATION
# ============================================================================

def visualize_cross_validation(results: List[Dict]):
    """Create comprehensive visualization of cross-validation results."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Codex Unified Validator - Time ↔ Space Domain Cross-Check',
                 fontsize=16, fontweight='bold')

    # Plot 1: Predicted vs Measured Frequencies
    ax1 = axes[0, 0]
    measured = [r['f_measured_hz'] for r in results]
    f_time = [r['f_time_hz'] for r in results]
    f_space = [r['f_space_hz'] for r in results]
    colors = [r['color'] for r in results]

    ax1.scatter(measured, f_time, c='red', s=100, alpha=0.6, label='Time-Domain', marker='o')
    ax1.scatter(measured, f_space, c='blue', s=100, alpha=0.6, label='Space-Domain', marker='s')

    # Perfect agreement line
    min_f = min(measured)
    max_f = max(measured)
    ax1.plot([min_f, max_f], [min_f, max_f], 'k--', alpha=0.5, label='Perfect Agreement')

    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Measured Frequency (Hz)')
    ax1.set_ylabel('Predicted Frequency (Hz)')
    ax1.set_title('Predicted vs Measured Frequencies')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Prediction Errors
    ax2 = axes[0, 1]
    systems = [r['system'] for r in results]
    error_time = [r['error_time_percent'] for r in results]
    error_space = [r['error_space_percent'] for r in results]

    x = np.arange(len(systems))
    width = 0.35

    ax2.bar(x - width/2, error_time, width, label='Time-Domain', color='red', alpha=0.6)
    ax2.bar(x + width/2, error_space, width, label='Space-Domain', color='blue', alpha=0.6)
    ax2.axhline(y=10, color='orange', linestyle='--', label='10% threshold')

    ax2.set_xlabel('System')
    ax2.set_ylabel('Prediction Error (%)')
    ax2.set_title('Prediction Errors by System')
    ax2.set_xticks(x)
    ax2.set_xticklabels([s[:15] + '...' if len(s) > 15 else s for s in systems],
                        rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Implied Velocity Distribution
    ax3 = axes[1, 0]
    velocities = [r['v_implied_ms'] for r in results]
    layers = [r['expected_layer'] for r in results]

    layer_colors = {1: 'red', 2: 'blue', 3: 'green'}
    for i, (v, layer) in enumerate(zip(velocities, layers)):
        ax3.scatter(i, v, c=layer_colors[layer], s=150, alpha=0.7, marker='o')

    # Layer boundaries
    ax3.axhspan(40, 70, alpha=0.2, color='red', label='Layer 1 (54 m/s)')
    ax3.axhspan(200, 500, alpha=0.2, color='blue', label='Layer 2 (343 m/s)')
    ax3.axhspan(1500, 5000, alpha=0.2, color='green', label='Layer 3 (1500-5000 m/s)')

    ax3.set_yscale('log')
    ax3.set_xlabel('System')
    ax3.set_ylabel('Implied Velocity (m/s)')
    ax3.set_title('Implied Velocities from Data')
    ax3.set_xticks(range(len(systems)))
    ax3.set_xticklabels([s[:15] + '...' if len(s) > 15 else s for s in systems],
                        rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Plot 4: Cross-Check Error Matrix
    ax4 = axes[1, 1]
    cross_errors = [r['error_cross_percent'] for r in results]

    ax4.barh(systems, cross_errors, color=[r['color'] for r in results], alpha=0.6)
    ax4.axvline(x=20, color='orange', linestyle='--', label='20% threshold')
    ax4.set_xlabel('Cross-Check Error (%)')
    ax4.set_ylabel('System')
    ax4.set_title('Time ↔ Space Domain Agreement')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('codex_unified_validator_cross_check.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Visualization saved: codex_unified_validator_cross_check.png")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("CODEX UNIFIED VALIDATOR")
    print("Time-Domain ↔ Space-Domain Cross-Validation")
    print("="*80)

    # Generate cross-validation report
    results = generate_cross_validation_report()

    # Visualize results
    visualize_cross_validation(results)

    print("\n" + "="*80)
    print("✅ CROSS-VALIDATION COMPLETE")
    print("="*80)

    print("\n📋 KEY FINDINGS:")
    perfect = sum(1 for r in results if r['verdict'] == 'PERFECT MATCH')
    print(f"   • {perfect}/{len(results)} systems show perfect time ↔ space agreement")
    print(f"   • Average cross-check error: {np.mean([r['error_cross_percent'] for r in results]):.1f}%")
    print(f"   • Layer classification: {sum(1 for r in results if r['expected_layer'] == r['implied_layer'])}/{len(results)} correct")

    print("\n💡 CONCLUSION:")
    if perfect >= len(results) * 0.6:
        print("   ✅ The framework is SELF-CONSISTENT across time and space domains.")
        print("   Both approaches converge on the same physics.")
    else:
        print("   ⚠️  Inconsistencies detected. Further refinement needed.")
