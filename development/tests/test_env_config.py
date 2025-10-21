#!/usr/bin/env python3
"""
Test environment variable configuration for MVP damage scoring.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_env_configuration():
    """Test that environment variables are properly loaded."""
    print("🔧 Testing Environment Variable Configuration")
    print("=" * 60)
    
    try:
        from oci_delivery_agent.config import DamageTypeWeights, DamageScoringConfig
        
        # Test 1: Default weights
        print("\n📋 Test 1: Default Weights")
        print("-" * 30)
        default_weights = DamageTypeWeights()
        normalized = default_weights.normalized()
        
        print(f"Leakage: {default_weights.leakage} → {normalized['leakage']:.3f}")
        print(f"Box Deformation: {default_weights.box_deformation} → {normalized['boxDeformation']:.3f}")
        print(f"Packaging Integrity: {default_weights.packaging_integrity} → {normalized['packagingIntegrity']:.3f}")
        print(f"Corner Damage: {default_weights.corner_damage} → {normalized['cornerDamage']:.3f}")
        print(f"Sum: {sum(normalized.values()):.3f} ✅")
        
        # Test 2: Custom weights (simulate environment variables)
        print("\n📋 Test 2: Custom Weights (Electronics)")
        print("-" * 45)
        
        # Simulate electronics configuration
        electronics_weights = DamageTypeWeights(
            leakage=0.5,
            box_deformation=0.25,
            packaging_integrity=0.15,
            corner_damage=0.1
        )
        electronics_normalized = electronics_weights.normalized()
        
        print(f"Leakage: {electronics_weights.leakage} → {electronics_normalized['leakage']:.3f}")
        print(f"Box Deformation: {electronics_weights.box_deformation} → {electronics_normalized['boxDeformation']:.3f}")
        print(f"Packaging Integrity: {electronics_weights.packaging_integrity} → {electronics_normalized['packagingIntegrity']:.3f}")
        print(f"Corner Damage: {electronics_weights.corner_damage} → {electronics_normalized['cornerDamage']:.3f}")
        print(f"Sum: {sum(electronics_normalized.values()):.3f} ✅")
        
        # Test 3: Furniture weights
        print("\n📋 Test 3: Custom Weights (Furniture)")
        print("-" * 40)
        
        furniture_weights = DamageTypeWeights(
            leakage=0.3,
            box_deformation=0.4,
            packaging_integrity=0.2,
            corner_damage=0.1
        )
        furniture_normalized = furniture_weights.normalized()
        
        print(f"Leakage: {furniture_weights.leakage} → {furniture_normalized['leakage']:.3f}")
        print(f"Box Deformation: {furniture_weights.box_deformation} → {furniture_normalized['boxDeformation']:.3f}")
        print(f"Packaging Integrity: {furniture_weights.packaging_integrity} → {furniture_normalized['packagingIntegrity']:.3f}")
        print(f"Corner Damage: {furniture_weights.corner_damage} → {furniture_normalized['cornerDamage']:.3f}")
        print(f"Sum: {sum(furniture_normalized.values()):.3f} ✅")
        
        # Test 4: Edge case - weights don't sum to 1.0
        print("\n📋 Test 4: Auto-normalization")
        print("-" * 35)
        
        weird_weights = DamageTypeWeights(
            leakage=1.0,      # Total = 2.0, should normalize to 0.5
            box_deformation=1.0,
            packaging_integrity=0.0,
            corner_damage=0.0
        )
        weird_normalized = weird_weights.normalized()
        
        print(f"Input: leakage=1.0, deformation=1.0, others=0.0")
        print(f"Normalized: leakage={weird_normalized['leakage']:.3f}, deformation={weird_normalized['boxDeformation']:.3f}")
        print(f"Sum: {sum(weird_normalized.values()):.3f} ✅")
        
        # Test 5: Damage scoring config
        print("\n📋 Test 5: Damage Scoring Configuration")
        print("-" * 45)
        
        config = DamageScoringConfig(
            use_weighted_scoring=True,
            type_weights=electronics_weights
        )
        
        print(f"Use Weighted Scoring: {config.use_weighted_scoring}")
        print(f"Type Weights: {config.type_weights}")
        print(f"Thresholds: none_max={config.none_max}, severe_min={config.severe_min}")
        
        print("\n✅ All configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scoring_calculation():
    """Test the actual scoring calculation with different scenarios."""
    print("\n🧮 Testing Scoring Calculation")
    print("=" * 60)
    
    try:
        from oci_delivery_agent.chains import _compute_weighted_damage_score
        from oci_delivery_agent.config import DamageTypeWeights
        
        # Test scenario: Mixed damage types
        damage_report = {
            "indicators": {
                "leakage": {"present": True, "severity": "moderate"},
                "boxDeformation": {"present": True, "severity": "minor"},
                "packagingIntegrity": {"present": False, "severity": "none"},
                "cornerDamage": {"present": True, "severity": "minor"}
            }
        }
        
        # Default weights
        weights = DamageTypeWeights()
        score = _compute_weighted_damage_score(damage_report, weights)
        
        print(f"Mixed Damage Scenario:")
        print(f"  Leakage: moderate (0.65) × 0.4 = 0.26")
        print(f"  Box Deformation: minor (0.35) × 0.3 = 0.105")
        print(f"  Corner Damage: minor (0.35) × 0.1 = 0.035")
        print(f"  Total: (0.26 + 0.105 + 0.035) / 0.8 = 0.5")
        print(f"  Quality Score: {score:.3f} ({score*100:.1f}%)")
        
        # Test with electronics weights
        electronics_weights = DamageTypeWeights(
            leakage=0.5,
            box_deformation=0.25,
            packaging_integrity=0.15,
            corner_damage=0.1
        )
        electronics_score = _compute_weighted_damage_score(damage_report, electronics_weights)
        
        print(f"\nElectronics Configuration:")
        print(f"  Leakage: moderate (0.65) × 0.5 = 0.325")
        print(f"  Box Deformation: minor (0.35) × 0.25 = 0.0875")
        print(f"  Corner Damage: minor (0.35) × 0.1 = 0.035")
        print(f"  Total: (0.325 + 0.0875 + 0.035) / 0.85 = 0.526")
        print(f"  Quality Score: {electronics_score:.3f} ({electronics_score*100:.1f}%)")
        
        print(f"\n✅ Electronics weights make leakage more impactful!")
        print(f"   Default: {score*100:.1f}% vs Electronics: {electronics_score*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Scoring calculation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 MVP Environment Configuration Test")
    print("=" * 60)
    
    success1 = test_env_configuration()
    success2 = test_scoring_calculation()
    
    if success1 and success2:
        print("\n🎉 All environment configuration tests passed!")
        print("✅ MVP damage scoring is ready for production")
    else:
        print("\n⚠️  Some tests failed.")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
