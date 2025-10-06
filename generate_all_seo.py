#!/usr/bin/env python3
"""
Master SEO Generator for MarketWizardry.org

Automatically runs all SEO generators to maintain:
- Gallery pages with JSON-LD ImageGallery schema
- Root pages with appropriate JSON-LD schema types
- Blog posts with Article schema
- All pages maintain CSP compliance (external JSON-LD scripts)

Usage:
    python3 generate_all_seo.py
"""

import subprocess
import sys
import os


def run_generator(script_name, description):
    """Run a generator script and report results"""
    print(f"\n{'=' * 70}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'=' * 70}")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode != 0:
            print(f"⚠️  {script_name} exited with code {result.returncode}")
            return False

        return True

    except subprocess.TimeoutExpired:
        print(f"❌ {script_name} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False


def main():
    """Run all SEO generators in sequence"""
    print("=" * 70)
    print("MarketWizardry.org - Master SEO Generator")
    print("=" * 70)
    print("This script maintains all SEO/JSON-LD schemas across the site")
    print("All generated content is CSP-compliant (external scripts only)")
    print()

    os.chdir('/home/typhoon/git/MarketWizardry.org')

    generators = [
        ('generate_gallery.py', 'NFT Gallery Pages (106+ pages with ImageGallery schema)'),
        ('generate_root_pages_seo.py', 'Root Pages (Explorer tools, blog index, etc.)'),
        ('generate_blog_seo.py', 'Blog Posts (Article schema for all blog posts)'),
    ]

    results = {}

    for script, description in generators:
        if not os.path.exists(script):
            print(f"⚠️  Script not found: {script}")
            results[script] = False
            continue

        results[script] = run_generator(script, description)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    for script, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} - {script}")

    print(f"\n{success_count}/{total_count} generators completed successfully")

    if success_count == total_count:
        print("\n🎉 All SEO generators completed successfully!")
        print("Site is fully optimized with JSON-LD structured data")
        return 0
    else:
        print("\n⚠️  Some generators failed - please check output above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
