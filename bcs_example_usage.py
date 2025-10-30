#!/usr/bin/env python3
"""
BCS ALGORITHM - EXAMPLE USAGE
==============================
Demonstrates how to analyze custom compounds using the BCS framework

Author: Codex Framework Team
Date: October 2025
"""

from codex_biocompatibility_screening import *

# =============================================================================
# EXAMPLE 1: Analyze a single custom compound
# =============================================================================

def example_1_single_compound():
    """Analyze a custom antioxidant compound"""

    print("\n" + "="*80)
    print("EXAMPLE 1: Single Compound Analysis - Custom Antioxidant")
    print("="*80 + "\n")

    # Define compound
    vitamin_c = CompoundData(
        name="Vitamin C (Ascorbic Acid)",
        formula="C₆H₈O₆",
        functional_groups=FunctionalGroupCount(
            hydroxyl=4,  # Multiple -OH groups
            ether=1,     # Ring oxygen
            carbonyl=1,  # C=O
            carboxyl=0,  # Not ionized form
        ),
        properties=MolecularProperties(
            molecular_weight=176.1,
            water_solubility=333.0,  # Highly water-soluble (333 mg/mL)
            charged_groups=0,
            is_natural=True,
            has_polymer_structure=False,
        ),
        regulatory=RegulatoryStatus(
            fda_status="GRAS",
            is_banned=False,
            is_carcinogen=False,
            has_warnings=False,
        ),
        description="Essential vitamin, powerful antioxidant",
        known_effects=[
            "Potent antioxidant - scavenges free radicals",
            "Essential for collagen synthesis",
            "Supports immune function",
            "Enhances iron absorption"
        ]
    )

    # Analyze
    analysis = BCSAnalyzer.analyze_compound(vitamin_c)

    # Print report
    BCSReportGenerator.print_analysis(analysis, vitamin_c)

    # Generate visualization
    BCSVisualizer.plot_score_breakdown(analysis, "example_vitamin_c_bcs.png")

    # Export JSON
    BCSReportGenerator.export_json(analysis, vitamin_c, "example_vitamin_c_bcs.json")

    print(f"\n✅ Vitamin C Analysis: {analysis.verdict.value} (BCS Score: {analysis.final_bcs_score:.3f})")

# =============================================================================
# EXAMPLE 2: Batch analysis of multiple compounds
# =============================================================================

def example_2_batch_analysis():
    """Compare multiple food additives"""

    print("\n" + "="*80)
    print("EXAMPLE 2: Batch Analysis - Food Additive Comparison")
    print("="*80 + "\n")

    # Define compounds
    compounds = []

    # Sodium benzoate (preservative)
    compounds.append(CompoundData(
        name="Sodium Benzoate",
        formula="C₇H₅NaO₂",
        functional_groups=FunctionalGroupCount(
            hydroxyl=0,
            carboxylate=1,  # Ionized -COO⁻
        ),
        properties=MolecularProperties(
            molecular_weight=144.1,
            water_solubility=660.0,  # Highly soluble
            charged_groups=1,
            is_natural=False,
        ),
        regulatory=RegulatoryStatus(
            fda_status="GRAS",
            is_banned=False,
            is_carcinogen=False,
            has_warnings=True,
            warning_text="Can form benzene with vitamin C; chronic exposure concerns"
        ),
        description="Synthetic preservative",
        known_effects=["Preservative", "May cause allergic reactions in sensitive individuals"]
    ))

    # Citric acid (natural)
    compounds.append(CompoundData(
        name="Citric Acid",
        formula="C₆H₈O₇",
        functional_groups=FunctionalGroupCount(
            hydroxyl=1,
            carboxyl=3,  # Three carboxylic acid groups
        ),
        properties=MolecularProperties(
            molecular_weight=192.1,
            water_solubility=1330.0,  # Very soluble
            charged_groups=0,  # Depends on pH
            is_natural=True,
        ),
        regulatory=RegulatoryStatus(
            fda_status="GRAS",
            is_banned=False,
            is_carcinogen=False,
        ),
        description="Natural acidulant from citrus fruits",
        known_effects=["Antioxidant", "Flavor enhancer", "Natural metabolite"]
    ))

    # Analyze all
    analyses = []
    for compound in compounds:
        analysis = BCSAnalyzer.analyze_compound(compound)
        analyses.append(analysis)
        print(f"\n   Analyzed: {compound.name}")
        print(f"   BCS Score: {analysis.final_bcs_score:.3f}")
        print(f"   Verdict: {analysis.verdict.value}")

    # Create comparison
    BCSVisualizer.plot_compound_comparison(analyses, compounds, "example_batch_comparison.png")

    print("\n✅ Batch analysis complete. Comparison plot saved.")

# =============================================================================
# EXAMPLE 3: Screen a problematic compound
# =============================================================================

def example_3_red_flag_detection():
    """Demonstrate red flag detection on a problematic compound"""

    print("\n" + "="*80)
    print("EXAMPLE 3: Red Flag Detection - Titanium Dioxide Nanoparticles")
    print("="*80 + "\n")

    # TiO2 nanoparticles (E171 - banned in EU as of 2022)
    tio2_nano = CompoundData(
        name="Titanium Dioxide (Nanoparticle)",
        formula="TiO₂",
        functional_groups=FunctionalGroupCount(
            # Inorganic, no typical organic functional groups
            hydroxyl=0,
        ),
        properties=MolecularProperties(
            molecular_weight=79.9,  # Single unit
            water_solubility=0.0001,  # Essentially insoluble
            charged_groups=0,
            is_natural=False,
            has_polymer_structure=True,  # Nanoparticle aggregate
            polymer_units=1000,  # Estimated - large aggregate
            dynamic_timescale=10.0  # Very slow dynamics
        ),
        regulatory=RegulatoryStatus(
            fda_status="Approved in US, Banned in EU (2022)",
            is_banned=False,  # In US
            is_carcinogen=False,
            has_warnings=True,
            warning_text="EU banned due to genotoxicity concerns; cannot rule out cancer risk"
        ),
        description="White pigment, food colorant (E171) - nanoparticle form",
        known_effects=[
            "Nanoparticles can cross intestinal barrier",
            "Accumulation in liver, spleen, kidneys",
            "Potential genotoxicity and inflammatory effects",
            "Scale mismatch - nanoparticle vs cellular dynamics"
        ]
    )

    # Analyze
    analysis = BCSAnalyzer.analyze_compound(tio2_nano)

    # Print report
    BCSReportGenerator.print_analysis(analysis, tio2_nano)

    # Highlight red flags
    print("\n🚨 RED FLAGS DETECTED:")
    for flag in analysis.red_flags:
        print(f"   {flag}")

    print(f"\n⚠️  Final Assessment: {analysis.verdict.value}")
    print(f"   BCS Score: {analysis.final_bcs_score:.3f}")
    print(f"\n   This demonstrates BCS's ability to flag compounds with scale mismatch issues")
    print(f"   even when they have minimal traditional 'functional groups'.")

# =============================================================================
# EXAMPLE 4: Retrieve and modify validation compounds
# =============================================================================

def example_4_database_access():
    """Access the built-in compound database"""

    print("\n" + "="*80)
    print("EXAMPLE 4: Database Access - Retrieve Validation Compounds")
    print("="*80 + "\n")

    # Get all validation compounds
    all_compounds = CompoundDatabase.get_validation_compounds()

    print(f"📚 Database contains {len(all_compounds)} validation compounds:\n")

    for compound in all_compounds:
        print(f"   • {compound.name}")
        print(f"     Formula: {compound.formula}")
        print(f"     Status: {compound.regulatory.fda_status}")
        print()

    # Retrieve specific compound
    stevia = CompoundDatabase.get_compound_by_name("stevia")

    if stevia:
        print(f"\n🔍 Retrieved: {stevia.name}")
        print(f"   Description: {stevia.description}")
        print(f"   MW: {stevia.properties.molecular_weight} Da")
        print(f"   Water Solubility: {stevia.properties.water_solubility} mg/mL")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run all examples"""

    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "BCS ALGORITHM - EXAMPLE USAGE GUIDE".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")

    # Run examples
    example_1_single_compound()
    example_2_batch_analysis()
    example_3_red_flag_detection()
    example_4_database_access()

    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)

    print("""
📊 Generated Files:
   • example_vitamin_c_bcs.png
   • example_vitamin_c_bcs.json
   • example_batch_comparison.png

💡 Next Steps:
   1. Modify the examples above for your own compounds
   2. Run the full validation suite: python codex_biocompatibility_screening.py
   3. Read BCS_README.md for detailed documentation
   4. Integrate BCS scoring into your existing workflows

🔬 Key Takeaways:
   • High water-compatible groups (-OH, -NH₂) → Higher BCS scores
   • Water-disruptive groups (sulfonate, halogenation) → Lower BCS scores
   • Three pillars must all pass for full biocompatibility
   • Red flags can override high scores (see Aspartame example)

For questions or contributions: dustinhansmade@gmail.com
""")

if __name__ == "__main__":
    main()
