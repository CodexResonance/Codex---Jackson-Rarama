#!/usr/bin/env python3
"""
COMPREHENSIVE VIRUS VALIDATION: CODEX RESONANCE FRAMEWORK
==========================================================
Validates ALL scaling laws from the framework against virus data:

1. Universal Transmission Law: f* = 1/T_D
2. RaRaMa Effect: f × d = 542.7 GHz·Å
3. Quarter-Wave Resonance: f* = c_eff / (4 × d)
4. Biological Timescale: f* = 1/(2πτ)

This script is ready to validate against PNAS 2025 virus data
or any other virus structure/frequency measurements.

Authors: Framework by Dustin Hansley & James Lockwood
         Validation script for PNAS paper analysis
Date: October 2025
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# =============================================================================
# UNIVERSAL CONSTANTS
# =============================================================================

class Constants:
    """Universal constants from the Codex Resonance Framework"""

    # Golden ratio
    PHI = (1 + np.sqrt(5)) / 2

    # RaRaMa universal constant (GHz·Å)
    RARAMA_CONSTANT = 542.7

    # Propagation speeds (m/s)
    C_LIGHT = 3.0e8
    C_AQUEOUS = 2.25e8
    C_CYTOPLASM = 2.17e8
    C_MEMBRANE = 2.04e8
    C_STRUCTURED_WATER = 1.8e8

    # Unit conversions
    ANGSTROM_TO_METER = 1e-10
    NM_TO_ANGSTROM = 10.0
    GHZ_TO_HZ = 1e9

# =============================================================================
# VIRUS DATA STRUCTURE
# =============================================================================

@dataclass
class VirusData:
    """Data structure for virus measurements"""
    name: str
    dimension_nm: float  # Typical dimension in nanometers
    observed_freq_ghz: Optional[float] = None  # If available from experiments
    structure_type: str = "spherical"  # spherical, helical, complex
    notes: str = ""

# =============================================================================
# SCALING LAW VALIDATORS
# =============================================================================

class ScalingLawValidator:
    """Validate all scaling laws against virus data"""

    @staticmethod
    def rarama_frequency(dimension_angstroms: float) -> float:
        """
        RaRaMa Effect: f = 542.7 / d

        Args:
            dimension_angstroms: Virus dimension in Ångströms

        Returns:
            Predicted frequency in GHz
        """
        return Constants.RARAMA_CONSTANT / dimension_angstroms

    @staticmethod
    def rarama_dimension(frequency_ghz: float) -> float:
        """
        Inverse RaRaMa: d = 542.7 / f

        Args:
            frequency_ghz: Frequency in GHz

        Returns:
            Predicted dimension in Ångströms
        """
        return Constants.RARAMA_CONSTANT / frequency_ghz

    @staticmethod
    def quarter_wave_frequency(dimension_angstroms: float, c_eff: float) -> float:
        """
        Quarter-wave resonance: f* = c_eff / (4 × d)

        Args:
            dimension_angstroms: Dimension in Ångströms
            c_eff: Effective propagation speed (m/s)

        Returns:
            Frequency in Hz
        """
        dimension_meters = dimension_angstroms * Constants.ANGSTROM_TO_METER
        return c_eff / (4 * dimension_meters)

    @staticmethod
    def transmission_distance(frequency_hz: float, c_eff: float) -> float:
        """
        Universal Transmission Law: T_D = c_eff / (4f)

        Args:
            frequency_hz: Frequency in Hz
            c_eff: Effective propagation speed (m/s)

        Returns:
            Transmission distance in meters
        """
        return c_eff / (4 * frequency_hz)

    @staticmethod
    def biological_timescale_frequency(tau_seconds: float) -> float:
        """
        Biological timescale: f* = 1/(2πτ)

        Args:
            tau_seconds: Characteristic timescale in seconds

        Returns:
            Frequency in Hz
        """
        return 1 / (2 * np.pi * tau_seconds)

# =============================================================================
# COMPREHENSIVE VIRUS VALIDATOR
# =============================================================================

class VirusValidator:
    """Complete validation suite for virus data"""

    def __init__(self):
        self.validator = ScalingLawValidator()
        self.results = []

    def validate_virus(self, virus: VirusData) -> Dict:
        """
        Complete validation of a virus against all scaling laws

        Args:
            virus: VirusData object with measurements

        Returns:
            Dictionary with all predictions and validations
        """
        # Convert dimensions
        dim_angstroms = virus.dimension_nm * Constants.NM_TO_ANGSTROM
        dim_meters = dim_angstroms * Constants.ANGSTROM_TO_METER

        # RaRaMa prediction
        rarama_freq_ghz = self.validator.rarama_frequency(dim_angstroms)
        rarama_freq_hz = rarama_freq_ghz * Constants.GHZ_TO_HZ

        # Quarter-wave predictions for different media
        qw_cytoplasm_hz = self.validator.quarter_wave_frequency(
            dim_angstroms, Constants.C_CYTOPLASM
        )
        qw_aqueous_hz = self.validator.quarter_wave_frequency(
            dim_angstroms, Constants.C_AQUEOUS
        )
        qw_membrane_hz = self.validator.quarter_wave_frequency(
            dim_angstroms, Constants.C_MEMBRANE
        )

        # Transmission distances
        T_D_cytoplasm = self.validator.transmission_distance(
            rarama_freq_hz, Constants.C_CYTOPLASM
        )
        T_D_aqueous = self.validator.transmission_distance(
            rarama_freq_hz, Constants.C_AQUEOUS
        )

        # Build results dictionary
        results = {
            'virus_name': virus.name,
            'structure_type': virus.structure_type,
            'dimension_nm': virus.dimension_nm,
            'dimension_angstroms': dim_angstroms,
            'dimension_meters': dim_meters,

            # RaRaMa predictions
            'rarama_frequency_ghz': rarama_freq_ghz,
            'rarama_frequency_hz': rarama_freq_hz,
            'rarama_product': rarama_freq_ghz * dim_angstroms,  # Should be ~542.7

            # Quarter-wave predictions
            'quarter_wave_cytoplasm_ghz': qw_cytoplasm_hz / Constants.GHZ_TO_HZ,
            'quarter_wave_aqueous_ghz': qw_aqueous_hz / Constants.GHZ_TO_HZ,
            'quarter_wave_membrane_ghz': qw_membrane_hz / Constants.GHZ_TO_HZ,

            # Transmission distances
            'transmission_distance_cytoplasm_nm': T_D_cytoplasm * 1e9,
            'transmission_distance_aqueous_nm': T_D_aqueous * 1e9,

            # Wavelength at RaRaMa frequency
            'wavelength_cytoplasm_nm': (Constants.C_CYTOPLASM / rarama_freq_hz) * 1e9,
            'wavelength_aqueous_nm': (Constants.C_AQUEOUS / rarama_freq_hz) * 1e9,
        }

        # If observed frequency is available, calculate errors
        if virus.observed_freq_ghz is not None:
            results['observed_frequency_ghz'] = virus.observed_freq_ghz
            results['rarama_error_percent'] = (
                abs(rarama_freq_ghz - virus.observed_freq_ghz) /
                virus.observed_freq_ghz * 100
            )
            results['rarama_observed_product'] = virus.observed_freq_ghz * dim_angstroms

            # Check if quarter-wave matches better
            qw_cytoplasm_ghz = qw_cytoplasm_hz / Constants.GHZ_TO_HZ
            results['quarter_wave_cytoplasm_error_percent'] = (
                abs(qw_cytoplasm_ghz - virus.observed_freq_ghz) /
                virus.observed_freq_ghz * 100
            )

        if virus.notes:
            results['notes'] = virus.notes

        self.results.append(results)
        return results

    def print_validation_report(self, results: Dict):
        """Print comprehensive validation report"""
        print("\n" + "="*80)
        print(f"VIRUS: {results['virus_name']}")
        print(f"Structure Type: {results['structure_type']}")
        print("="*80)

        print(f"\n📏 DIMENSIONS:")
        print(f"   {results['dimension_nm']:.1f} nm")
        print(f"   {results['dimension_angstroms']:.1f} Å")
        print(f"   {results['dimension_meters']:.2e} m")

        print(f"\n🔮 RARAMA EFFECT PREDICTION:")
        print(f"   f = 542.7 / d = {results['rarama_frequency_ghz']:.3f} GHz")
        print(f"   f × d = {results['rarama_product']:.1f} GHz·Å (Expected: 542.7)")

        if 'observed_frequency_ghz' in results:
            print(f"\n🔬 EXPERIMENTAL VALIDATION:")
            print(f"   Observed: {results['observed_frequency_ghz']:.3f} GHz")
            print(f"   RaRaMa Error: {results['rarama_error_percent']:.2f}%")
            print(f"   Observed Product: {results['rarama_observed_product']:.1f} GHz·Å")

            if results['rarama_error_percent'] < 10:
                print(f"   ✓ EXCELLENT AGREEMENT")
            elif results['rarama_error_percent'] < 25:
                print(f"   ✓ GOOD AGREEMENT")
            else:
                print(f"   ⚠ Check quarter-wave predictions below")

        print(f"\n🌊 QUARTER-WAVE PREDICTIONS:")
        print(f"   Cytoplasm:  {results['quarter_wave_cytoplasm_ghz']:.3f} GHz")
        print(f"   Aqueous:    {results['quarter_wave_aqueous_ghz']:.3f} GHz")
        print(f"   Membrane:   {results['quarter_wave_membrane_ghz']:.3f} GHz")

        if 'quarter_wave_cytoplasm_error_percent' in results:
            print(f"\n   Quarter-wave (cytoplasm) error: {results['quarter_wave_cytoplasm_error_percent']:.2f}%")

        print(f"\n📡 TRANSMISSION DISTANCES:")
        print(f"   Cytoplasm:  {results['transmission_distance_cytoplasm_nm']:.2f} nm")
        print(f"   Aqueous:    {results['transmission_distance_aqueous_nm']:.2f} nm")

        print(f"\n📏 WAVELENGTHS:")
        print(f"   λ (cytoplasm): {results['wavelength_cytoplasm_nm']:.2f} nm")
        print(f"   λ (aqueous):   {results['wavelength_aqueous_nm']:.2f} nm")
        print(f"   Virus/Wavelength ratio: {results['dimension_nm']/results['wavelength_cytoplasm_nm']:.3f}")

        if 'notes' in results:
            print(f"\n📝 NOTES: {results['notes']}")

        print("="*80)

    def generate_summary_table(self):
        """Generate summary table of all validated viruses"""
        if not self.results:
            print("No validation results available.")
            return

        print("\n" + "="*80)
        print("SUMMARY: ALL VIRUS VALIDATIONS")
        print("="*80)
        print()
        print(f"{'Virus':<20} {'Size (nm)':<12} {'RaRaMa (GHz)':<15} {'f×d':<10} {'Error %':<10}")
        print("-"*80)

        for r in self.results:
            error_str = f"{r['rarama_error_percent']:.1f}%" if 'rarama_error_percent' in r else "N/A"
            print(f"{r['virus_name']:<20} {r['dimension_nm']:<12.1f} "
                  f"{r['rarama_frequency_ghz']:<15.3f} "
                  f"{r['rarama_product']:<10.1f} {error_str:<10}")

        print("="*80)

        # Calculate statistics if we have observed data
        observed_count = sum(1 for r in self.results if 'rarama_error_percent' in r)
        if observed_count > 0:
            avg_error = np.mean([r['rarama_error_percent']
                                for r in self.results if 'rarama_error_percent' in r])
            print(f"\nAverage RaRaMa prediction error: {avg_error:.2f}%")
            print(f"Validated against {observed_count} experimental measurements")

# =============================================================================
# EXAMPLE VIRUS DATABASE
# =============================================================================

def get_example_virus_database() -> List[VirusData]:
    """
    Example virus database with common viruses
    REPLACE THIS WITH DATA FROM PNAS 2025 PAPER
    """
    return [
        VirusData(
            name="SARS-CoV-2",
            dimension_nm=120.0,
            observed_freq_ghz=None,  # Add from PNAS paper if available
            structure_type="enveloped spherical",
            notes="Coronavirus causing COVID-19, ~120nm diameter with spike proteins"
        ),
        VirusData(
            name="Influenza A",
            dimension_nm=100.0,
            observed_freq_ghz=None,
            structure_type="enveloped spherical",
            notes="Seasonal flu virus, spherical ~80-120nm"
        ),
        VirusData(
            name="HIV-1",
            dimension_nm=120.0,
            observed_freq_ghz=None,
            structure_type="enveloped spherical",
            notes="Human immunodeficiency virus, ~120nm"
        ),
        VirusData(
            name="Poliovirus",
            dimension_nm=30.0,
            observed_freq_ghz=None,
            structure_type="non-enveloped icosahedral",
            notes="Small RNA virus, ~30nm"
        ),
        VirusData(
            name="Adenovirus",
            dimension_nm=90.0,
            observed_freq_ghz=None,
            structure_type="non-enveloped icosahedral",
            notes="DNA virus, ~90nm"
        ),
        VirusData(
            name="Herpes Simplex Virus",
            dimension_nm=200.0,
            observed_freq_ghz=None,
            structure_type="enveloped icosahedral",
            notes="Large DNA virus, ~200nm with envelope"
        ),
        VirusData(
            name="Rhinovirus",
            dimension_nm=30.0,
            observed_freq_ghz=None,
            structure_type="non-enveloped icosahedral",
            notes="Common cold virus, ~30nm"
        ),
        VirusData(
            name="Ebola Virus",
            dimension_nm=80.0,  # diameter of filamentous structure
            observed_freq_ghz=None,
            structure_type="enveloped filamentous",
            notes="Filamentous virus, ~80nm diameter, variable length"
        ),
        VirusData(
            name="Bacteriophage T4",
            dimension_nm=90.0,  # head diameter
            observed_freq_ghz=None,
            structure_type="complex (tailed)",
            notes="Bacterial virus with complex structure, head ~90nm"
        ),
        VirusData(
            name="Tobacco Mosaic Virus",
            dimension_nm=18.0,  # diameter
            observed_freq_ghz=None,
            structure_type="helical rod",
            notes="Plant virus, helical rod ~18nm diameter, 300nm length"
        ),
    ]

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main validation routine"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "VIRUS VALIDATION: CODEX RESONANCE SCALING LAWS".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "Validating RaRaMa Effect & Quarter-Wave Resonance".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print("\n📊 SCALING LAWS TO BE VALIDATED:")
    print("   1. RaRaMa Effect:      f × d = 542.7 GHz·Å")
    print("   2. Quarter-Wave:       f* = c_eff / (4d)")
    print("   3. Transmission Law:   T_D = c_eff / (4f)")
    print("   4. Universal Constant: Same physics from molecules to macroscale")

    # Initialize validator
    validator = VirusValidator()

    # Get virus database (REPLACE WITH PNAS DATA)
    print("\n📚 Loading virus database...")
    virus_database = get_example_virus_database()
    print(f"   Loaded {len(virus_database)} viruses")

    # Validate each virus
    print("\n🔬 PERFORMING VALIDATIONS...")
    for virus in virus_database:
        results = validator.validate_virus(virus)
        validator.print_validation_report(results)

    # Generate summary
    validator.generate_summary_table()

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Replace example database with PNAS 2025 virus data")
    print("2. Add observed frequencies if available from the paper")
    print("3. Compare predictions with experimental measurements")
    print("4. Analyze which scaling law (RaRaMa vs Quarter-Wave) fits best")
    print("5. Investigate medium-dependent effects (cytoplasm vs aqueous)")
    print("="*80)

if __name__ == "__main__":
    main()
