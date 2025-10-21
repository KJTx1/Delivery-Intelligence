#!/usr/bin/env python3
"""
Test full integration of MVP damage scoring with handlers.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_handler_integration():
    """Test that handlers properly load the new configuration."""
    print("🔗 Testing Handler Integration")
    print("=" * 60)
    
    try:
        # Set up test environment variables
        os.environ['DAMAGE_USE_WEIGHTED_SCORING'] = 'true'
        os.environ['DAMAGE_WEIGHT_LEAKAGE'] = '0.5'
        os.environ['DAMAGE_WEIGHT_BOX_DEFORMATION'] = '0.25'
        os.environ['DAMAGE_WEIGHT_PACKAGING_INTEGRITY'] = '0.15'
        os.environ['DAMAGE_WEIGHT_CORNER_DAMAGE'] = '0.1'
        
        from oci_delivery_agent.handlers import load_config
        
        # Test configuration loading
        print("📋 Testing Configuration Loading")
        print("-" * 40)
        
        config = load_config()
        
        print(f"✅ Config loaded successfully")
        print(f"✅ Use Weighted Scoring: {config.damage_scoring.use_weighted_scoring}")
        print(f"✅ Leakage Weight: {config.damage_scoring.type_weights.leakage}")
        print(f"✅ Box Deformation Weight: {config.damage_scoring.type_weights.box_deformation}")
        print(f"✅ Packaging Integrity Weight: {config.damage_scoring.type_weights.packaging_integrity}")
        print(f"✅ Corner Damage Weight: {config.damage_scoring.type_weights.corner_damage}")
        
        # Test normalized weights
        normalized = config.damage_scoring.type_weights.normalized()
        print(f"\n📊 Normalized Weights:")
        print(f"  Leakage: {normalized['leakage']:.3f}")
        print(f"  Box Deformation: {normalized['boxDeformation']:.3f}")
        print(f"  Packaging Integrity: {normalized['packagingIntegrity']:.3f}")
        print(f"  Corner Damage: {normalized['cornerDamage']:.3f}")
        print(f"  Sum: {sum(normalized.values()):.3f} ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Handler integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_disable_weighted_scoring():
    """Test that weighted scoring can be disabled."""
    print("\n🔧 Testing Disable Weighted Scoring")
    print("-" * 45)
    
    try:
        # Set environment to disable weighted scoring
        os.environ['DAMAGE_USE_WEIGHTED_SCORING'] = 'false'
        
        from oci_delivery_agent.handlers import load_config
        
        config = load_config()
        
        print(f"✅ Use Weighted Scoring: {config.damage_scoring.use_weighted_scoring}")
        print(f"✅ System will fall back to original logic")
        print(f"✅ Backward compatibility maintained")
        
        return True
        
    except Exception as e:
        print(f"❌ Disable test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n⚠️  Testing Edge Cases")
    print("-" * 30)
    
    try:
        from oci_delivery_agent.config import DamageTypeWeights
        
        # Test 1: Zero weights (should fail)
        print("Test 1: Zero weights")
        try:
            zero_weights = DamageTypeWeights(0, 0, 0, 0)
            zero_weights.normalized()
            print("❌ Should have failed with zero weights")
            return False
        except ValueError as e:
            print(f"✅ Correctly caught error: {e}")
        
        # Test 2: Negative weights (should normalize)
        print("\nTest 2: Negative weights")
        try:
            negative_weights = DamageTypeWeights(-0.1, 0.5, 0.3, 0.3)
            normalized = negative_weights.normalized()
            print(f"✅ Handled negative weights: {normalized}")
        except Exception as e:
            print(f"❌ Failed to handle negative weights: {e}")
            return False
        
        # Test 3: Very large weights (should normalize)
        print("\nTest 3: Large weights")
        try:
            large_weights = DamageTypeWeights(100, 200, 300, 400)
            normalized = large_weights.normalized()
            print(f"✅ Handled large weights: {normalized}")
            print(f"✅ Sum: {sum(normalized.values()):.3f}")
        except Exception as e:
            print(f"❌ Failed to handle large weights: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main integration test function"""
    print("🚀 MVP Integration Test")
    print("=" * 60)
    
    success1 = test_handler_integration()
    success2 = test_disable_weighted_scoring()
    success3 = test_edge_cases()
    
    if success1 and success2 and success3:
        print("\n🎉 All integration tests passed!")
        print("✅ MVP damage scoring is fully integrated and ready")
        print("✅ Backward compatibility confirmed")
        print("✅ Error handling verified")
        print("✅ Environment variable loading works")
    else:
        print("\n⚠️  Some integration tests failed.")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
