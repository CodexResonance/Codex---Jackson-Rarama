#!/usr/bin/env python3
"""
CODEX FRAMEWORK: MERCURY & PLASMA DYNAMICS ANALYZER
====================================================

Models collective dynamics in mercury, rotating plasmas, and continuous power systems.
Applies Codex principles to predict resonances, dynamo onset, and coherent states.

Key Features:
1. Mercury collective mode calculation
2. Dynamo onset prediction
3. THz resonance frequency analysis
4. Rotating plasma simulation
5. Inertial mass reduction hypothesis testing

Author: Codex Framework Advanced Physics Team
Date: October 29, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Universal constants
C_LIGHT = 2.998e8  # m/s - Speed of light
H_PLANCK = 6.626e-34  # J·s - Planck's constant
H_BAR = H_PLANCK / (2 * np.pi)  # Reduced Planck constant
K_B = 1.381e-23  # J/K - Boltzmann constant
MU_0 = 4 * np.pi * 1e-7  # H/m - Vacuum permeability
EPSILON_0 = 8.854e-12  # F/m - Vacuum permittivity

# Codex Framework constant
CODEX_VELOCITY = 54.27  # m/s - Wet structural relaxation velocity
CODEX_CONSTANT = 542.7  # GHz·Å - Resonance principle

# Mercury properties
HG_ATOMIC_MASS = 200.59  # amu
HG_DENSITY = 13534  # kg/m³ at 20°C
HG_RESISTIVITY = 961e-9  # Ω·m at 20°C
HG_BULK_SOUND_SPEED = 1450  # m/s
HG_ATOMIC_SPACING = 3.0e-10  # m (3 Angstroms)
HG_MELTING_POINT = 234.32  # K (-38.8°C)
HG_BOILING_POINT = 629.88  # K (356.7°C)
HG_TC_SUPERCONDUCTOR = 4.15  # K - Critical temperature

# Plasma parameters
ELECTRON_MASS = 9.109e-31  # kg
ELECTRON_CHARGE = 1.602e-19  # C
PROTON_MASS = 1.673e-27  # kg

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class SystemState(Enum):
    """System operational states"""
    INACTIVE = "Inactive"
    INITIALIZING = "Initializing"
    DYNAMO_ONSET = "Dynamo Onset"
    COHERENT = "Coherent State"
    SELF_SUSTAINING = "Self-Sustaining"

@dataclass
class MercuryProperties:
    """Physical properties of mercury"""
    temperature: float  # K
    density: float  # kg/m³
    resistivity: float  # Ω·m
    sound_speed: float  # m/s
    viscosity: float  # Pa·s
    is_superconducting: bool = False

@dataclass
class PlasmaParameters:
    """Plasma state parameters"""
    electron_density: float  # m⁻³
    ion_density: float  # m⁻³
    temperature_e: float  # K (electron temperature)
    temperature_i: float  # K (ion temperature)
    magnetic_field: float  # T (Tesla)
    debye_length: float  # m

@dataclass
class DynamoConditions:
    """Rotating system dynamo parameters"""
    rotation_speed: float  # RPM
    radius: float  # m
    magnetic_field: float  # T
    conductivity: float  # S/m
    reynolds_magnetic: float  # Dimensionless
    is_self_sustaining: bool = False

@dataclass
class CodexResonance:
    """THz resonance analysis"""
    length_scale: float  # m
    frequency_thz: float  # THz
    wavelength: float  # m
    energy_ev: float  # eV
    coupling_strength: float  # Dimensionless (0-1)

# ============================================================================
# MERCURY ANALYSIS
# ============================================================================

class MercuryAnalyzer:
    """
    Analyzes collective dynamics in liquid mercury.
    Applies Codex Framework to predict resonances and coherent modes.
    """

    @staticmethod
    def calculate_properties(temperature: float) -> MercuryProperties:
        """Calculate temperature-dependent mercury properties"""

        # Density (slight temperature dependence)
        density = HG_DENSITY * (1 - 1.81e-4 * (temperature - 293.15))

        # Resistivity (linear with temperature above melting point)
        if temperature < HG_MELTING_POINT:
            # Solid state (not applicable for our purposes)
            resistivity = 1e-6
        else:
            # Liquid state
            T_rel = temperature - HG_MELTING_POINT
            resistivity = HG_RESISTIVITY * (1 + 0.0009 * T_rel)

        # Sound speed (slight temperature dependence)
        sound_speed = HG_BULK_SOUND_SPEED * (1 - 0.0002 * (temperature - 293.15))

        # Viscosity (Arrhenius-like)
        viscosity = 1.526e-3 * np.exp(365 / temperature)

        # Superconducting state
        is_superconducting = temperature < HG_TC_SUPERCONDUCTOR

        return MercuryProperties(
            temperature=temperature,
            density=density,
            resistivity=resistivity,
            sound_speed=sound_speed,
            viscosity=viscosity,
            is_superconducting=is_superconducting
        )

    @staticmethod
    def codex_collective_velocity(temperature: float) -> float:
        """
        Predict collective reorganization velocity in mercury using Codex principles.

        Similar to water: structured water has soliton velocity ~54 m/s
        For mercury: heavier atoms, but still collective modes

        Hypothesis: Mercury collective velocity ~ 50-200 m/s (THz domain)
        """
        props = MercuryAnalyzer.calculate_properties(temperature)

        # Estimate collective velocity from:
        # 1. Atomic mass (heavier = slower)
        # 2. Density (structure)
        # 3. Temperature (thermal energy disrupts coherence)

        # Base velocity (Codex constant)
        v_base = CODEX_VELOCITY

        # Mass correction (mercury is 11× heavier than water molecule)
        mass_ratio = HG_ATOMIC_MASS / 18.0  # vs H2O
        mass_factor = 1.0 / np.sqrt(mass_ratio)

        # Temperature factor (coherence decreases with temperature)
        T_ref = 293.15  # K (room temp)
        temp_factor = np.exp(-0.001 * (temperature - T_ref))

        # Predicted collective velocity
        v_collective = v_base * mass_factor * temp_factor

        return v_collective

    @staticmethod
    def thz_resonance(length_scale: float = HG_ATOMIC_SPACING) -> CodexResonance:
        """
        Calculate THz resonance frequency for mercury.

        Uses Codex principle: f × d = 542.7 GHz·Å
        """
        # Convert length to Angstroms
        length_angstroms = length_scale * 1e10

        # Codex resonance frequency
        freq_ghz = CODEX_CONSTANT / length_angstroms
        freq_hz = freq_ghz * 1e9
        freq_thz = freq_hz / 1e12

        # Wavelength
        wavelength = C_LIGHT / freq_hz

        # Photon energy
        energy_j = H_PLANCK * freq_hz
        energy_ev = energy_j / ELECTRON_CHARGE

        # Coupling strength (estimated based on mercury properties)
        # High density + free electrons = strong coupling
        coupling = 0.75  # High coupling for liquid metal

        return CodexResonance(
            length_scale=length_scale,
            frequency_thz=freq_thz,
            wavelength=wavelength,
            energy_ev=energy_ev,
            coupling_strength=coupling
        )

    @staticmethod
    def collective_mode_spectrum(temperature: float,
                                 q_range: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate collective mode dispersion relation E(q).

        For liquid mercury:
        - Acoustic-like modes (phonons)
        - Electronic modes (plasmons)

        Returns: (energy_array_eV, damping_array)
        """
        v_collective = MercuryAnalyzer.codex_collective_velocity(temperature)

        # Dispersion relation: E = ℏ v q (linear, like phonons)
        energy_j = H_BAR * v_collective * q_range
        energy_ev = energy_j / ELECTRON_CHARGE

        # Damping (higher q = more damping)
        damping = 0.01 + 0.1 * (q_range / q_range.max())**2

        return energy_ev, damping

# ============================================================================
# PLASMA ANALYSIS
# ============================================================================

class PlasmaAnalyzer:
    """
    Analyzes mercury plasma properties and collective behavior.
    """

    @staticmethod
    def calculate_plasma_parameters(electron_density: float,
                                     temperature_ev: float,
                                     magnetic_field: float = 0.0) -> PlasmaParameters:
        """
        Calculate fundamental plasma parameters.

        Args:
            electron_density: m⁻³
            temperature_ev: eV
            magnetic_field: Tesla
        """
        # Convert temperature to Kelvin
        temperature_k = temperature_ev * 11604.5

        # Debye length
        debye_length = np.sqrt(EPSILON_0 * temperature_ev * ELECTRON_CHARGE /
                               (electron_density * ELECTRON_CHARGE**2))

        # Ion density (quasi-neutral plasma)
        ion_density = electron_density

        return PlasmaParameters(
            electron_density=electron_density,
            ion_density=ion_density,
            temperature_e=temperature_k,
            temperature_i=temperature_k * 0.5,  # Ions typically cooler
            magnetic_field=magnetic_field,
            debye_length=debye_length
        )

    @staticmethod
    def plasma_frequency(electron_density: float) -> float:
        """
        Calculate electron plasma frequency (rad/s).

        ω_pe = sqrt(n_e * e² / (m_e * ε₀))
        """
        omega_pe = np.sqrt(electron_density * ELECTRON_CHARGE**2 /
                          (ELECTRON_MASS * EPSILON_0))
        return omega_pe

    @staticmethod
    def cyclotron_frequency(magnetic_field: float) -> Tuple[float, float]:
        """
        Calculate cyclotron frequencies for electrons and ions.

        ω_ce = e B / m_e  (electrons)
        ω_ci = e B / m_i  (ions)

        Returns: (omega_ce, omega_ci) in rad/s
        """
        omega_ce = ELECTRON_CHARGE * magnetic_field / ELECTRON_MASS

        # For mercury ions (singly ionized Hg⁺)
        m_ion = HG_ATOMIC_MASS * 1.66054e-27  # Convert amu to kg
        omega_ci = ELECTRON_CHARGE * magnetic_field / m_ion

        return omega_ce, omega_ci

    @staticmethod
    def codex_plasma_resonance(plasma_params: PlasmaParameters) -> CodexResonance:
        """
        Apply Codex Framework to predict resonance in mercury plasma.

        Length scale: Debye length (typical plasma length scale)
        """
        return MercuryAnalyzer.thz_resonance(plasma_params.debye_length)

# ============================================================================
# DYNAMO ANALYSIS
# ============================================================================

class DynamoAnalyzer:
    """
    Analyzes rotating mercury dynamo systems.
    Predicts onset of self-sustaining magnetic field generation.
    """

    @staticmethod
    def calculate_dynamo_conditions(rotation_rpm: float,
                                     radius: float,
                                     temperature: float = 293.15,
                                     seed_field: float = 1e-4) -> DynamoConditions:
        """
        Calculate conditions for dynamo action in rotating mercury.

        Args:
            rotation_rpm: Rotations per minute
            radius: Sphere/cylinder radius (m)
            temperature: Mercury temperature (K)
            seed_field: Initial magnetic field (T)
        """
        # Mercury properties
        props = MercuryAnalyzer.calculate_properties(temperature)

        # Rotation velocity at radius
        omega = rotation_rpm * 2 * np.pi / 60  # rad/s
        v_rotation = omega * radius

        # Conductivity (inverse of resistivity)
        conductivity = 1.0 / props.resistivity

        # Magnetic Reynolds number (dimensionless)
        # R_m = μ₀ σ v L
        # where L is characteristic length scale
        reynolds_magnetic = MU_0 * conductivity * v_rotation * radius

        # Critical Reynolds number for dynamo onset: R_m > 10 (approximate)
        is_self_sustaining = reynolds_magnetic > 10.0

        return DynamoConditions(
            rotation_speed=rotation_rpm,
            radius=radius,
            magnetic_field=seed_field,
            conductivity=conductivity,
            reynolds_magnetic=reynolds_magnetic,
            is_self_sustaining=is_self_sustaining
        )

    @staticmethod
    def critical_rotation_speed(radius: float,
                                temperature: float = 293.15) -> float:
        """
        Calculate critical rotation speed for dynamo onset.

        Based on R_m = 10 threshold.
        """
        props = MercuryAnalyzer.calculate_properties(temperature)
        conductivity = 1.0 / props.resistivity

        # R_m = μ₀ σ v L = 10
        # v = 10 / (μ₀ σ L)
        v_critical = 10.0 / (MU_0 * conductivity * radius)

        # Convert to RPM
        omega_critical = v_critical / radius
        rpm_critical = omega_critical * 60 / (2 * np.pi)

        return rpm_critical

    @staticmethod
    def codex_dynamo_prediction(radius: float,
                                temperature: float = 293.15) -> Dict:
        """
        Predict dynamo behavior using Codex velocity principle.

        Hypothesis: Dynamo onset when v_rotation ~ v_codex_collective
        """
        v_collective = MercuryAnalyzer.codex_collective_velocity(temperature)

        # Rotation speed to achieve codex velocity at radius
        omega_codex = v_collective / radius
        rpm_codex = omega_codex * 60 / (2 * np.pi)

        # Standard critical RPM
        rpm_critical_standard = DynamoAnalyzer.critical_rotation_speed(radius, temperature)

        return {
            'codex_velocity': v_collective,
            'codex_rpm': rpm_codex,
            'standard_critical_rpm': rpm_critical_standard,
            'ratio': rpm_codex / rpm_critical_standard,
            'prediction': 'Codex predicts enhanced dynamo effect' if rpm_codex < rpm_critical_standard else 'Standard theory predicts onset first'
        }

# ============================================================================
# INERTIAL EFFECTS (SPECULATIVE)
# ============================================================================

class InertialAnalyzer:
    """
    HIGHLY SPECULATIVE: Models hypothetical inertial mass reduction.
    Based on Pais patents and vacuum engineering concepts.
    """

    @staticmethod
    def vacuum_energy_density(frequency_hz: float) -> float:
        """
        Zero-point energy density at given frequency.

        ρ_vac = (ℏ ω³) / (2 π² c³)
        """
        omega = 2 * np.pi * frequency_hz
        rho = (H_BAR * omega**3) / (2 * np.pi**2 * C_LIGHT**3)
        return rho

    @staticmethod
    def pais_mass_reduction_factor(field_strength_vm: float,
                                   frequency_hz: float,
                                   interaction_volume: float) -> float:
        """
        Estimate mass reduction factor from Pais mechanism (SPECULATIVE).

        Assumptions:
        - High-frequency EM field creates polarization of vacuum
        - Local modification of Higgs field VEV
        - Reduction factor ε = (field energy) / (vacuum energy)

        Args:
            field_strength_vm: V/m (electric field)
            frequency_hz: Hz (THz range expected)
            interaction_volume: m³

        Returns:
            epsilon: Mass reduction factor (0 = no effect, 1 = complete reduction)
        """
        # Field energy density
        E_field = 0.5 * EPSILON_0 * field_strength_vm**2

        # Vacuum energy density at this frequency
        E_vacuum = InertialAnalyzer.vacuum_energy_density(frequency_hz)

        # Total field energy
        total_field_energy = E_field * interaction_volume

        # Interaction strength (wildly speculative)
        # Assume coupling ~ 10⁻²⁰ (extremely weak)
        coupling = 1e-20

        # Mass reduction factor (capped at reasonable limit)
        epsilon = coupling * total_field_energy / (E_vacuum * interaction_volume)
        epsilon = min(epsilon, 0.1)  # Cap at 10% reduction (even this is absurd)

        return epsilon

# ============================================================================
# VISUALIZATION
# ============================================================================

class SystemVisualizer:
    """Generate visualizations of mercury/plasma systems"""

    @staticmethod
    def plot_mercury_collective_spectrum(temperature: float = 293.15,
                                         filename: str = "mercury_collective_modes.png"):
        """Plot collective mode spectrum for mercury"""

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Mercury Collective Dynamics (Codex Framework Analysis)',
                    fontsize=14, fontweight='bold')

        # 1. Collective velocity vs temperature
        ax = axes[0, 0]
        temps = np.linspace(250, 400, 50)
        velocities = [MercuryAnalyzer.codex_collective_velocity(T) for T in temps]

        ax.plot(temps, velocities, linewidth=2, color='darkblue')
        ax.axhline(CODEX_VELOCITY, color='red', linestyle='--', label='Water Codex Velocity')
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Collective Velocity (m/s)')
        ax.set_title('Predicted Collective Reorganization Velocity')
        ax.legend()
        ax.grid(alpha=0.3)

        # 2. THz resonance spectrum
        ax = axes[0, 1]
        length_scales = np.linspace(2e-10, 10e-10, 50)  # 2-10 Angstroms
        frequencies = [MercuryAnalyzer.thz_resonance(L).frequency_thz for L in length_scales]

        ax.plot(length_scales * 1e10, frequencies, linewidth=2, color='purple')
        ax.set_xlabel('Length Scale (Å)')
        ax.set_ylabel('Resonance Frequency (THz)')
        ax.set_title('THz Resonance (f × d = 542.7 GHz·Å)')
        ax.grid(alpha=0.3)

        # 3. Dispersion relation
        ax = axes[1, 0]
        q_range = np.linspace(1e9, 1e11, 100)  # m⁻¹
        energies, damping = MercuryAnalyzer.collective_mode_spectrum(temperature, q_range)

        ax.plot(q_range / 1e9, energies * 1000, linewidth=2, label='Collective Mode')
        ax.set_xlabel('Wavevector q (nm⁻¹)')
        ax.set_ylabel('Energy (meV)')
        ax.set_title('Collective Mode Dispersion E(q)')
        ax.legend()
        ax.grid(alpha=0.3)

        # 4. Properties vs temperature
        ax = axes[1, 1]
        temps = np.linspace(250, 600, 100)
        resistivities = []
        sound_speeds = []

        for T in temps:
            props = MercuryAnalyzer.calculate_properties(T)
            resistivities.append(props.resistivity * 1e9)  # nΩ·m
            sound_speeds.append(props.sound_speed)

        ax2 = ax.twinx()
        l1 = ax.plot(temps, resistivities, 'b-', linewidth=2, label='Resistivity')
        l2 = ax2.plot(temps, sound_speeds, 'r-', linewidth=2, label='Sound Speed')

        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Resistivity (nΩ·m)', color='b')
        ax2.set_ylabel('Sound Speed (m/s)', color='r')
        ax.set_title('Mercury Properties vs Temperature')
        ax.tick_params(axis='y', labelcolor='b')
        ax2.tick_params(axis='y', labelcolor='r')
        ax.grid(alpha=0.3)

        # Combine legends
        lns = l1 + l2
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc='upper left')

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {filename}")
        plt.close()

    @staticmethod
    def plot_dynamo_onset(radius: float = 0.15,
                         filename: str = "dynamo_onset.png"):
        """Plot dynamo onset conditions"""

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Rotating Mercury Dynamo Analysis (R = {radius*100:.1f} cm)',
                    fontsize=14, fontweight='bold')

        # 1. Magnetic Reynolds number vs RPM
        ax = axes[0, 0]
        rpms = np.linspace(100, 5000, 100)
        reynolds = []
        for rpm in rpms:
            cond = DynamoAnalyzer.calculate_dynamo_conditions(rpm, radius)
            reynolds.append(cond.reynolds_magnetic)

        ax.plot(rpms, reynolds, linewidth=2, color='darkgreen')
        ax.axhline(10, color='red', linestyle='--', label='Critical R_m = 10')
        ax.fill_between(rpms, 10, max(reynolds), alpha=0.2, color='green',
                        label='Self-Sustaining Region')
        ax.set_xlabel('Rotation Speed (RPM)')
        ax.set_ylabel('Magnetic Reynolds Number')
        ax.set_title('Dynamo Onset Criterion')
        ax.legend()
        ax.grid(alpha=0.3)
        ax.set_yscale('log')

        # 2. Critical RPM vs radius
        ax = axes[0, 1]
        radii = np.linspace(0.05, 0.5, 50)  # 5 cm to 50 cm
        critical_rpms = [DynamoAnalyzer.critical_rotation_speed(r) for r in radii]
        codex_rpms = [DynamoAnalyzer.codex_dynamo_prediction(r)['codex_rpm'] for r in radii]

        ax.plot(radii * 100, critical_rpms, linewidth=2, label='Standard Theory', color='blue')
        ax.plot(radii * 100, codex_rpms, linewidth=2, label='Codex Prediction', color='red',
               linestyle='--')
        ax.set_xlabel('Radius (cm)')
        ax.set_ylabel('Critical RPM')
        ax.set_title('Dynamo Onset Speed vs System Size')
        ax.legend()
        ax.grid(alpha=0.3)
        ax.set_yscale('log')

        # 3. Velocity profile
        ax = axes[1, 0]
        rpm_test = 3000
        r_range = np.linspace(0, radius, 50)
        omega = rpm_test * 2 * np.pi / 60
        v_profile = omega * r_range

        v_codex = MercuryAnalyzer.codex_collective_velocity(293.15)

        ax.plot(r_range * 100, v_profile, linewidth=2, color='darkblue', label=f'{rpm_test} RPM')
        ax.axhline(v_codex, color='red', linestyle='--', label=f'Codex Velocity ({v_codex:.1f} m/s)')
        ax.fill_between(r_range * 100, 0, v_codex, alpha=0.2, color='red',
                        label='Codex Resonance Zone')
        ax.set_xlabel('Radius (cm)')
        ax.set_ylabel('Tangential Velocity (m/s)')
        ax.set_title('Velocity Profile in Rotating Mercury')
        ax.legend()
        ax.grid(alpha=0.3)

        # 4. Codex vs Standard comparison
        ax = axes[1, 1]
        radii_test = [0.10, 0.15, 0.20, 0.30]
        labels = [f'{r*100:.0f} cm' for r in radii_test]
        x = np.arange(len(radii_test))
        width = 0.35

        standard_rpms = [DynamoAnalyzer.critical_rotation_speed(r) for r in radii_test]
        codex_rpms = [DynamoAnalyzer.codex_dynamo_prediction(r)['codex_rpm'] for r in radii_test]

        ax.bar(x - width/2, standard_rpms, width, label='Standard Theory', alpha=0.8)
        ax.bar(x + width/2, codex_rpms, width, label='Codex Prediction', alpha=0.8)

        ax.set_xlabel('System Radius')
        ax.set_ylabel('Critical RPM')
        ax.set_title('Onset Speed Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {filename}")
        plt.close()

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    """Run complete mercury/plasma analysis"""

    print("\n" + "="*80)
    print("CODEX FRAMEWORK: MERCURY & PLASMA DYNAMICS ANALYSIS")
    print("="*80 + "\n")

    # ========== MERCURY COLLECTIVE DYNAMICS ==========
    print("=" * 80)
    print("PART 1: MERCURY COLLECTIVE DYNAMICS")
    print("=" * 80 + "\n")

    T_room = 293.15  # K
    props = MercuryAnalyzer.calculate_properties(T_room)
    v_collective = MercuryAnalyzer.codex_collective_velocity(T_room)
    resonance = MercuryAnalyzer.thz_resonance()

    print(f"Mercury Properties at {T_room:.1f} K:")
    print(f"  Density:            {props.density:.1f} kg/m³")
    print(f"  Resistivity:        {props.resistivity*1e9:.1f} nΩ·m")
    print(f"  Sound Speed:        {props.sound_speed:.1f} m/s")
    print(f"  Viscosity:          {props.viscosity*1000:.2f} mPa·s")
    print()
    print(f"Codex Framework Predictions:")
    print(f"  Collective Velocity: {v_collective:.2f} m/s")
    print(f"  (Compare: Water Codex velocity = {CODEX_VELOCITY:.2f} m/s)")
    print(f"  THz Resonance:       {resonance.frequency_thz:.3f} THz ({resonance.frequency_thz*1000:.1f} GHz)")
    print(f"  Photon Energy:       {resonance.energy_ev:.3f} eV")
    print(f"  Coupling Strength:   {resonance.coupling_strength:.2f}")
    print()

    # ========== DYNAMO ANALYSIS ==========
    print("=" * 80)
    print("PART 2: ROTATING MERCURY DYNAMO")
    print("=" * 80 + "\n")

    radius = 0.15  # m (15 cm sphere)

    print(f"System: Rotating sphere, radius = {radius*100:.1f} cm\n")

    # Test different RPMs
    test_rpms = [1000, 2000, 3000, 4000, 5000]
    print(f"{'RPM':<10} {'R_m':<12} {'v_tip (m/s)':<15} {'Status':<20}")
    print("-" * 80)

    for rpm in test_rpms:
        cond = DynamoAnalyzer.calculate_dynamo_conditions(rpm, radius, T_room)
        omega = rpm * 2 * np.pi / 60
        v_tip = omega * radius
        status = "🟢 SELF-SUSTAINING" if cond.is_self_sustaining else "🔴 Sub-critical"
        print(f"{rpm:<10} {cond.reynolds_magnetic:<12.2f} {v_tip:<15.2f} {status:<20}")

    print()

    # Codex prediction
    codex_pred = DynamoAnalyzer.codex_dynamo_prediction(radius, T_room)
    print("Codex Framework Prediction:")
    print(f"  Codex Collective Velocity: {codex_pred['codex_velocity']:.2f} m/s")
    print(f"  Predicted Onset RPM:       {codex_pred['codex_rpm']:.0f} RPM")
    print(f"  Standard Theory RPM:       {codex_pred['standard_critical_rpm']:.0f} RPM")
    print(f"  Ratio (Codex/Standard):    {codex_pred['ratio']:.2f}")
    print(f"  Interpretation:            {codex_pred['prediction']}")
    print()

    # ========== PLASMA ANALYSIS ==========
    print("=" * 80)
    print("PART 3: MERCURY PLASMA")
    print("=" * 80 + "\n")

    # Typical mercury vapor plasma (low pressure discharge)
    n_e = 1e18  # m⁻³ (10¹⁸ electrons/m³)
    T_ev = 1.0  # eV (electron temperature)
    B_field = 0.1  # T (0.1 Tesla applied field)

    plasma = PlasmaAnalyzer.calculate_plasma_parameters(n_e, T_ev, B_field)
    omega_pe = PlasmaAnalyzer.plasma_frequency(n_e)
    omega_ce, omega_ci = PlasmaAnalyzer.cyclotron_frequency(B_field)
    plasma_resonance = PlasmaAnalyzer.codex_plasma_resonance(plasma)

    print(f"Mercury Plasma Parameters:")
    print(f"  Electron Density:     {plasma.electron_density:.2e} m⁻³")
    print(f"  Temperature:          {T_ev:.1f} eV ({plasma.temperature_e:.0f} K)")
    print(f"  Debye Length:         {plasma.debye_length*1e6:.2f} μm")
    print(f"  Magnetic Field:       {B_field:.2f} T")
    print()
    print(f"Characteristic Frequencies:")
    print(f"  Plasma Frequency:     {omega_pe/(2*np.pi*1e9):.2f} GHz")
    print(f"  Electron Cyclotron:   {omega_ce/(2*np.pi*1e9):.2f} GHz")
    print(f"  Ion Cyclotron:        {omega_ci/(2*np.pi*1e6):.2f} MHz")
    print()
    print(f"Codex Resonance (based on Debye length):")
    print(f"  Frequency:            {plasma_resonance.frequency_thz:.3f} THz")
    print(f"  Energy:               {plasma_resonance.energy_ev:.3f} eV")
    print()

    # ========== INERTIAL EFFECTS (SPECULATIVE) ==========
    print("=" * 80)
    print("PART 4: INERTIAL MASS REDUCTION (SPECULATIVE)")
    print("=" * 80 + "\n")

    print("⚠️  WARNING: Highly speculative, based on Pais patents\n")

    # Test conditions
    E_field = 1e6  # V/m (very high field)
    freq_thz = 0.3e12  # Hz (0.3 THz)
    volume = 0.001  # m³ (1 liter)

    epsilon = InertialAnalyzer.pais_mass_reduction_factor(E_field, freq_thz, volume)

    print(f"Hypothetical Test Conditions:")
    print(f"  Electric Field:       {E_field:.2e} V/m")
    print(f"  Frequency:            {freq_thz/1e12:.1f} THz")
    print(f"  Interaction Volume:   {volume*1000:.1f} liters")
    print()
    print(f"Predicted Mass Reduction:")
    print(f"  Factor ε:             {epsilon:.2e}")
    print(f"  Percentage:           {epsilon*100:.6f}%")
    print()
    print("Interpretation:")
    if epsilon < 1e-10:
        print("  → Effect is NEGLIGIBLE (below any measurable threshold)")
    elif epsilon < 1e-5:
        print("  → Effect is TINY (would require ultra-precise measurement)")
    elif epsilon < 1e-3:
        print("  → Effect is SMALL (detectable with high-precision instruments)")
    else:
        print("  → Effect is SIGNIFICANT (if real, would be revolutionary)")
    print()

    # ========== GENERATE VISUALIZATIONS ==========
    print("=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80 + "\n")

    SystemVisualizer.plot_mercury_collective_spectrum(T_room)
    SystemVisualizer.plot_dynamo_onset(radius)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nKey Findings:")
    print("  1. Mercury collective velocity predicted: {:.1f} m/s (Codex-based)".format(v_collective))
    print("  2. THz resonance: {:.3f} THz (testable with spectroscopy)".format(resonance.frequency_thz))
    print("  3. Dynamo onset: ~{:.0f} RPM for {:.0f} cm radius".format(
        codex_pred['codex_rpm'], radius*100))
    print("  4. Plasma resonance: {:.3f} THz (Debye length-based)".format(
        plasma_resonance.frequency_thz))
    print("\nNext Steps:")
    print("  → THz spectroscopy of liquid mercury (validates Codex frequency)")
    print("  → Lab-scale dynamo experiment (tests onset prediction)")
    print("  → Mercury plasma THz response (tests coherent state hypothesis)")
    print("\n✨ FRAMEWORK EXTENDS TO LIQUID METALS AND PLASMAS\n")

if __name__ == "__main__":
    main()
