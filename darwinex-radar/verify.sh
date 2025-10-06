#!/bin/bash
# Verification script for Darwinex RADAR v2.0.0

echo "════════════════════════════════════════════════════════"
echo "Darwinex RADAR v2.0.0 - Verification Script"
echo "════════════════════════════════════════════════════════"
echo

# Check Python scripts exist
echo "1. Checking Python scripts..."
if [ -f "symbol_tracker.py" ] && [ -f "generate_radar_html.py" ]; then
    echo "   ✅ Python scripts found"
else
    echo "   ❌ Python scripts missing"
    exit 1
fi

# Check radar reports exist
echo "2. Checking radar reports..."
if [ -f "stocks-radar.txt" ] && [ -f "futures-radar.txt" ] && [ -f "cfd-radar.txt" ] && [ -f "crypto-radar.txt" ]; then
    echo "   ✅ All radar reports found"
else
    echo "   ⚠️  Some radar reports missing (run: python3 symbol_tracker.py --all)"
fi

# Check HTML exists
echo "3. Checking HTML output..."
if [ -f "../darwinex-radar.html" ]; then
    echo "   ✅ HTML file found"
else
    echo "   ❌ HTML file missing (run: python3 generate_radar_html.py)"
    exit 1
fi

# Check for CSP violations
echo "4. Checking CSP compliance..."
violations=$(grep -n 'style=\|onclick=' ../darwinex-radar.html | grep -v 'src=' | wc -l)
if [ "$violations" -eq 0 ]; then
    echo "   ✅ No CSP violations found"
else
    echo "   ❌ Found $violations CSP violations"
    exit 1
fi

# Check for spec changes section
echo "5. Checking new features..."
if grep -q "SPECIFICATION CHANGES" stocks-radar.txt; then
    echo "   ✅ Spec changes section present"
else
    echo "   ❌ Spec changes section missing"
    exit 1
fi

if grep -q "Close-only does NOT count as delisted" stocks-radar.txt; then
    echo "   ✅ Close-only clarification present"
else
    echo "   ❌ Close-only clarification missing"
    exit 1
fi

# Check documentation
echo "6. Checking documentation..."
docs=("README.md" "CHANGELOG.md" "IMPLEMENTATION_SUMMARY.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc found"
    else
        echo "   ⚠️  $doc missing"
    fi
done

echo
echo "════════════════════════════════════════════════════════"
echo "✅ Verification Complete!"
echo "════════════════════════════════════════════════════════"
echo
echo "Quick Stats:"
echo "  - Stocks symbols tracked: $(grep 'Symbols on 2025.10.03:' stocks-radar.txt | awk '{print $4}')"
echo "  - Close-only changes: $(grep 'Total Close-Only Changes:' stocks-radar.txt | awk '{print $4}')"
echo "  - HTML file size: $(du -h ../darwinex-radar.html | awk '{print $1}')"
