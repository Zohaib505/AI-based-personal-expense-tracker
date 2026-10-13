"""
Test Receipt OCR Extraction
============================
This script tests the receipt OCR scanning without going through the web interface.
Use this to debug extraction issues with your demo receipts.

Usage:
  python test_receipt_ocr.py
  Enter receipt image path when prompted
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
django.setup()

try:
    import easyocr
    print("✅ EasyOCR is installed")
except ImportError:
    print("❌ EasyOCR not installed. Run: pip install easyocr")
    sys.exit(1)

# Import extraction functions from views
from expenses.views import extract_amount_from_text, extract_date_from_text, extract_vendor_from_text

def test_ocr_on_receipt(image_path):
    """Test OCR extraction on a receipt image"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"\n📷 Testing OCR on: {image_path}")
    print("=" * 70)
    
    try:
        # Initialize OCR reader
        print("📖 Loading OCR model (first time may take 30-60 seconds)...")
        reader = easyocr.Reader(['en'], gpu=False)
        
        # Read text from image
        print("🔍 Scanning receipt...")
        result = reader.readtext(image_path)
        
        # Extract text
        extracted_text = '\n'.join([detection[1] for detection in result])
        
        print("\n" + "=" * 70)
        print("📄 EXTRACTED TEXT FROM RECEIPT:")
        print("=" * 70)
        print(extracted_text)
        
        # Test extraction functions
        print("\n" + "=" * 70)
        print("🔎 PARSED DATA:")
        print("=" * 70)
        
        amount = extract_amount_from_text(extracted_text)
        date = extract_date_from_text(extracted_text)
        vendor = extract_vendor_from_text(extracted_text)
        
        print(f"💰 Amount: {amount} PKR" if amount else "💰 Amount: NOT FOUND")
        print(f"📅 Date: {date}" if date else "📅 Date: NOT FOUND (using today)")
        print(f"🏪 Vendor: {vendor}")
        
        print("\n" + "=" * 70)
        print("✅ TEST COMPLETE")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("Receipt OCR Extraction Tester")
    print("=" * 70)
    print("This tool helps debug receipt scanning issues")
    print()
    
    # Check for demo receipts in common locations
    demo_locations = [
        Path("receipt.jpg"),
        Path("receipt.png"),
        Path("demo_receipt.jpg"),
        Path("demo_receipt.png"),
        Path("./receipts/"),
        Path("./receipts.png/"),
        Path("./demo_receipts/"),
    ]
    
    print("Searching for demo receipts...")
    found_receipts = []
    
    for location in demo_locations:
        if location.is_file() and location.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            found_receipts.append(str(location))
            print(f"  ✓ Found: {location}")
        elif location.is_dir():
            for img_file in location.glob('*.*'):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                    found_receipts.append(str(img_file))
                    print(f"  ✓ Found: {img_file}")
    
    if found_receipts:
        print(f"\nFound {len(found_receipts)} receipts. Testing first one...")
        test_ocr_on_receipt(found_receipts[0])
    else:
        print("\n❌ No demo receipts found in current directory")
        print("\nTo test, place receipt images in one of these locations:")
        for loc in demo_locations:
            print(f"  • {loc}")
        
        # Ask for manual path
        print()
        image_path = input("Enter receipt image path (or 'exit' to quit): ").strip()
        if image_path.lower() != 'exit':
            test_ocr_on_receipt(image_path)

if __name__ == '__main__':
    main()
