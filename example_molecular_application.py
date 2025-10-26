#!/usr/bin/env python3
"""
PRACTICAL APPLICATION EXAMPLE
==============================
Applying Geometric Phase / Codex Resonance Framework to Real Molecules

This demonstrates the workflow from molecule → theory → predictions → tests

Example: Targeting a specific cancer-relevant protein with frequency-based therapy

Author: Framework Application
Date: October 2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Tuple

# =============================================================================
# MOLECULAR TARGET DATABASE
# =============================================================================

@dataclass
class MolecularTarget:
    """Data structure for therapeutic targets"""
    name: str
    molecular_weight: float  # Da
    dimension_nm: float  # Estimated size
    function: str
    cancer_relevance: str
    known_timescales: Dict[str, float]  # Process → time (seconds)

class CancerTargets:
    """Database of cancer-relevant molecular targets"""

    @staticmethod
    def get_targets() -> List[MolecularTarget]:
        """Return list of validated cancer targets"""
        return [
            MolecularTarget(
                name="Tubulin (αβ heterodimer)",
                molecular_weight=100_000,  # ~100 kDa
                dimension_nm=8.0,  # ~8 nm protein
                function="Microtubule component, mitotic spindle",
                cancer_relevance="Mitosis disruption (cancer cells divide rapidly)",
                known_timescales={
                    'GTP_hydrolysis': 0.5e-3,  # 0.5 ms
                    'polymerization': 10e-3,  # 10 ms
                    'conformational_change': 1e-6,  # 1 μs
                }
            ),
            MolecularTarget(
                name="p53 tumor suppressor",
                molecular_weight=53_000,  # 53 kDa
                dimension_nm=5.0,  # ~5 nm
                function="DNA damage response, apoptosis",
                cancer_relevance="Mutated in >50% of cancers",
                known_timescales={
                    'DNA_binding': 1e-3,  # 1 ms
                    'tetramerization': 1e-6,  # 1 μs
                    'conformational_switch': 100e-9,  # 100 ns
                }
            ),
            MolecularTarget(
                name="EGFR (epidermal growth factor receptor)",
                molecular_weight=170_000,  # 170 kDa
                dimension_nm=10.0,  # ~10 nm transmembrane protein
                function="Cell proliferation signaling",
                cancer_relevance="Overexpressed in many solid tumors",
                known_timescales={
                    'ligand_binding': 10e-3,  # 10 ms
                    'dimerization': 1e-3,  # 1 ms
                    'kinase_activation': 100e-6,  # 100 μs
                }
            ),
            MolecularTarget(
                name="Cancer cell membrane",
                molecular_weight=float('inf'),  # Extended structure
                dimension_nm=7.5,  # ~7.5 nm bilayer thickness
                function="Cell boundary, selective permeability",
                cancer_relevance="Altered lipid composition, different fluidity",
                known_timescales={
                    'lipid_flip_flop': 1.0,  # ~1 s (very slow!)
                    'lateral_diffusion': 1e-6,  # 1 μs
                    'ion_channel_gating': 1e-3,  # 1 ms
                }
            ),
        ]

# =============================================================================
# FREQUENCY PREDICTION ENGINE
# =============================================================================

class FrequencyPredictor:
    """Predict therapeutic frequencies using Codex framework"""

    # Constants
    RARAMA_CONSTANT = 542.7  # GHz·Å
    CODEX_VELOCITY = 54.27  # m/s

    @staticmethod
    def rarama_frequency(dimension_nm: float) -> float:
        """
        Predict fundamental RaRaMa frequency

        Args:
            dimension_nm: Molecular dimension in nm

        Returns:
            Frequency in Hz
        """
        dimension_angstrom = dimension_nm * 10
        freq_ghz = FrequencyPredictor.RARAMA_CONSTANT / dimension_angstrom
        return freq_ghz * 1e9  # Convert to Hz

    @staticmethod
    def timescale_frequency(tau_seconds: float) -> float:
        """
        Predict frequency from characteristic timescale

        f* = 1/(2πτ)

        Args:
            tau_seconds: Timescale in seconds

        Returns:
            Frequency in Hz
        """
        return 1.0 / (2 * np.pi * tau_seconds)

    @staticmethod
    def harmonic_series(fundamental_hz: float, n_harmonics: int = 5) -> List[float]:
        """
        Generate harmonic series from topological quantization

        f_n = n × f_0

        Args:
            fundamental_hz: Fundamental frequency
            n_harmonics: Number of harmonics

        Returns:
            List of harmonic frequencies
        """
        return [fundamental_hz * n for n in range(1, n_harmonics + 1)]

    @staticmethod
    def analyze_target(target: MolecularTarget) -> Dict:
        """
        Complete frequency analysis for molecular target

        Args:
            target: MolecularTarget object

        Returns:
            Dictionary with all predictions
        """
        # RaRaMa prediction
        f_rarama = FrequencyPredictor.rarama_frequency(target.dimension_nm)

        # Timescale-based predictions
        timescale_freqs = {
            process: FrequencyPredictor.timescale_frequency(tau)
            for process, tau in target.known_timescales.items()
        }

        # Harmonic series
        harmonics = FrequencyPredictor.harmonic_series(f_rarama, n_harmonics=5)

        # Wavelength
        wavelength_nm = (FrequencyPredictor.CODEX_VELOCITY / f_rarama) * 1e9

        return {
            'target_name': target.name,
            'dimension_nm': target.dimension_nm,
            'f_rarama_hz': f_rarama,
            'f_rarama_ghz': f_rarama / 1e9,
            'f_rarama_mhz': f_rarama / 1e6,
            'wavelength_nm': wavelength_nm,
            'timescale_frequencies': timescale_freqs,
            'harmonics_hz': harmonics,
            'harmonics_ghz': [h/1e9 for h in harmonics],
            'therapeutic_window': (f_rarama * 0.9, f_rarama * 1.1),  # ±10%
        }

# =============================================================================
# VISUALIZATION
# =============================================================================

class FrequencyVisualizer:
    """Visualize predicted frequency landscapes"""

    @staticmethod
    def plot_target_spectrum(analysis: Dict, filename: str = 'target_spectrum.png'):
        """
        Create spectrum plot for a target

        Args:
            analysis: Output from FrequencyPredictor.analyze_target()
            filename: Output filename
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Top panel: RaRaMa + harmonics
        harmonics_ghz = analysis['harmonics_ghz']
        fundamental_ghz = analysis['f_rarama_ghz']

        colors = plt.cm.viridis(np.linspace(0, 1, len(harmonics_ghz)))

        ax1.bar(range(len(harmonics_ghz)), harmonics_ghz,
               color=colors, alpha=0.7, edgecolor='black', linewidth=2)

        # Label fundamental
        ax1.bar(0, harmonics_ghz[0], color='red', alpha=0.8,
               edgecolor='black', linewidth=3, label='Fundamental (n=1)')

        ax1.set_xticks(range(len(harmonics_ghz)))
        ax1.set_xticklabels([f'n={i+1}' for i in range(len(harmonics_ghz))])
        ax1.set_ylabel('Frequency (GHz)', fontsize=14, fontweight='bold')
        ax1.set_title(f'Topological Harmonic Series: {analysis["target_name"]}',
                     fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.legend(fontsize=12)

        # Add frequency values on bars
        for i, freq in enumerate(harmonics_ghz):
            ax1.text(i, freq + max(harmonics_ghz)*0.02, f'{freq:.3f}\nGHz',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Bottom panel: Timescale-based frequencies
        if analysis['timescale_frequencies']:
            processes = list(analysis['timescale_frequencies'].keys())
            freqs_hz = list(analysis['timescale_frequencies'].values())
            freqs_ghz = [f/1e9 for f in freqs_hz]

            # Sort by frequency
            sorted_indices = np.argsort(freqs_hz)
            processes = [processes[i] for i in sorted_indices]
            freqs_ghz = [freqs_ghz[i] for i in sorted_indices]

            y_pos = np.arange(len(processes))

            ax2.barh(y_pos, freqs_ghz, color='steelblue', alpha=0.7,
                    edgecolor='black', linewidth=2)

            # Add RaRaMa reference line
            ax2.axvline(fundamental_ghz, color='red', linestyle='--',
                       linewidth=3, label=f'RaRaMa: {fundamental_ghz:.3f} GHz',
                       alpha=0.8)

            ax2.set_yticks(y_pos)
            ax2.set_yticklabels([p.replace('_', ' ').title() for p in processes])
            ax2.set_xlabel('Frequency (GHz)', fontsize=14, fontweight='bold')
            ax2.set_title('Process-Specific Timescale Frequencies',
                         fontsize=14, fontweight='bold')
            ax2.set_xscale('log')
            ax2.grid(True, alpha=0.3, axis='x')
            ax2.legend(fontsize=11)

            # Add frequency values
            for i, freq in enumerate(freqs_ghz):
                ax2.text(freq * 1.1, i, f'{freq:.2e} GHz',
                        va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"   Spectrum plot saved: {filename}")
        return filename

# =============================================================================
# THERAPEUTIC STRATEGY GENERATOR
# =============================================================================

class TherapeuticStrategy:
    """Generate frequency-based therapeutic strategies"""

    @staticmethod
    def generate_protocol(target: MolecularTarget, analysis: Dict) -> Dict:
        """
        Generate therapeutic protocol for target

        Args:
            target: MolecularTarget
            analysis: Frequency analysis results

        Returns:
            Treatment protocol dictionary
        """
        f_target = analysis['f_rarama_hz']
        f_min, f_max = analysis['therapeutic_window']

        # Determine frequency regime
        if f_target < 1e6:  # < 1 MHz
            regime = "Low frequency (kHz)"
            delivery = "Direct electrical stimulation"
        elif f_target < 1e9:  # < 1 GHz
            regime = "Microwave (MHz)"
            delivery = "Near-field antenna array"
        elif f_target < 1e12:  # < 1 THz
            regime = "Millimeter wave (GHz)"
            delivery = "Waveguide or horn antenna"
        else:
            regime = "Terahertz (THz)"
            delivery = "THz quantum cascade laser"

        # TTFields comparison (if applicable)
        ttfields_freq = 200e3  # 200 kHz
        ttfields_ratio = f_target / ttfields_freq

        protocol = {
            'target': target.name,
            'primary_frequency_hz': f_target,
            'primary_frequency_readable': f"{f_target/1e6:.3f} MHz" if f_target > 1e6 else f"{f_target/1e3:.3f} kHz",
            'therapeutic_window_hz': (f_min, f_max),
            'regime': regime,
            'delivery_method': delivery,
            'harmonics_hz': analysis['harmonics_hz'][:3],  # Use first 3 harmonics
            'ttfields_comparison': {
                'ttfields_frequency': ttfields_freq,
                'ratio': ttfields_ratio,
                'interpretation': f"{ttfields_ratio:.1f}× TTFields frequency"
            },
            'rationale': f"Target {target.cancer_relevance}",
            'expected_mechanism': "Topological phase disruption → selective interference with cancer cell processes",
        }

        return protocol

    @staticmethod
    def print_protocol(protocol: Dict):
        """Pretty-print therapeutic protocol"""
        print("\n" + "─"*80)
        print(f"THERAPEUTIC PROTOCOL: {protocol['target']}")
        print("─"*80)

        print(f"\n🎯 PRIMARY FREQUENCY:")
        print(f"   {protocol['primary_frequency_readable']}")
        print(f"   ({protocol['primary_frequency_hz']:.3e} Hz)")

        print(f"\n📡 DELIVERY:")
        print(f"   Regime: {protocol['regime']}")
        print(f"   Method: {protocol['delivery_method']}")

        print(f"\n🔬 THERAPEUTIC WINDOW:")
        f_min, f_max = protocol['therapeutic_window_hz']
        print(f"   {f_min/1e6:.3f} - {f_max/1e6:.3f} MHz")
        print(f"   (±10% around primary frequency)")

        print(f"\n🎵 HARMONIC AUGMENTATION:")
        for i, h_hz in enumerate(protocol['harmonics_hz'], 1):
            print(f"   n={i}: {h_hz/1e6:.3f} MHz")

        print(f"\n⚡ COMPARISON TO TTFIELDS:")
        ttf = protocol['ttfields_comparison']
        print(f"   TTFields: {ttf['ttfields_frequency']/1e3:.0f} kHz")
        print(f"   This protocol: {ttf['interpretation']}")

        print(f"\n💡 RATIONALE:")
        print(f"   {protocol['rationale']}")

        print(f"\n🔧 MECHANISM:")
        print(f"   {protocol['expected_mechanism']}")

        print("─"*80)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Run complete molecular targeting analysis"""

    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "GEOMETRIC PHASE THERAPY: MOLECULAR TARGET ANALYSIS".center(78) + "║")
    print("║" + " "*78 + "║")
    print("║" + "From Theory → Predictions → Therapeutic Protocols".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")

    # Get targets
    targets = CancerTargets.get_targets()

    print(f"\n📋 Loaded {len(targets)} cancer-relevant molecular targets")

    # Analyze each target
    all_analyses = []
    all_protocols = []

    for target in targets:
        print("\n" + "="*80)
        print(f"ANALYZING: {target.name}")
        print("="*80)

        # Predict frequencies
        analysis = FrequencyPredictor.analyze_target(target)
        all_analyses.append(analysis)

        print(f"\n📐 MOLECULAR DIMENSIONS:")
        print(f"   Size: {target.dimension_nm} nm")
        print(f"   MW: {target.molecular_weight/1000:.0f} kDa")

        print(f"\n🔮 RARAMA PREDICTION:")
        print(f"   Fundamental: {analysis['f_rarama_mhz']:.3f} MHz")
        print(f"   Wavelength: {analysis['wavelength_nm']:.1f} nm")

        print(f"\n🎵 HARMONIC SERIES:")
        for i, h_ghz in enumerate(analysis['harmonics_ghz'], 1):
            print(f"   n={i}: {h_ghz:.3f} GHz = {h_ghz*1000:.1f} MHz")

        if analysis['timescale_frequencies']:
            print(f"\n⏱️  TIMESCALE-BASED FREQUENCIES:")
            for process, freq in analysis['timescale_frequencies'].items():
                print(f"   {process.replace('_', ' ').title()}: {freq/1e6:.3f} MHz")

        # Generate therapeutic protocol
        protocol = TherapeuticStrategy.generate_protocol(target, analysis)
        all_protocols.append(protocol)
        TherapeuticStrategy.print_protocol(protocol)

        # Create visualization
        filename = f"spectrum_{target.name.replace(' ', '_').lower()}.png"
        FrequencyVisualizer.plot_target_spectrum(analysis, filename)

    # Summary comparison
    print("\n" + "="*80)
    print("COMPARATIVE SUMMARY: ALL TARGETS")
    print("="*80)

    print(f"\n{'Target':<35} {'Size (nm)':<12} {'f_RaRaMa (MHz)':<18} {'Regime':<15}")
    print("-"*80)

    for target, analysis in zip(targets, all_analyses):
        freq_mhz = analysis['f_rarama_mhz']

        if freq_mhz < 1:
            regime = "kHz"
        elif freq_mhz < 1000:
            regime = "MHz"
        else:
            regime = "GHz"

        print(f"{target.name:<35} {target.dimension_nm:<12.1f} "
              f"{freq_mhz:<18.3f} {regime:<15}")

    print("="*80)

    print(f"""
💡 KEY INSIGHTS:

1. Different targets have DIFFERENT optimal frequencies
   → Enables selective targeting

2. Frequencies span kHz to GHz range
   → Multiple delivery modalities needed

3. Harmonic series allows multi-frequency protocols
   → May enhance efficacy through topological interference

4. Timescale frequencies often differ from RaRaMa
   → Suggests multi-mode targeting strategy

5. Most frequencies are HIGHER than TTFields (200 kHz)
   → New frequency regimes to explore clinically
""")

    print("\n" + "="*80)
    print("RECOMMENDED NEXT STEPS")
    print("="*80)

    print("""
1. COMPUTATIONAL VALIDATION
   - DFT calculations of vibronic coupling for each target
   - CASSCF conical intersection searches
   - Molecular dynamics with explicit water

2. EXPERIMENTAL VALIDATION
   - THz spectroscopy of purified targets
   - Frequency-dependent binding assays
   - Cell viability screens across predicted frequencies

3. CLINICAL TRANSLATION
   - Safety testing of novel frequency regimes
   - Combination with existing therapies
   - Patient-specific frequency optimization

4. DEVICE DEVELOPMENT
   - MHz-GHz field generators
   - Implantable/wearable delivery systems
   - Real-time frequency tuning capability
""")

    print("="*80)
    print("Analysis complete. Spectrum plots saved for each target.")
    print("="*80)

if __name__ == "__main__":
    main()
