#!/usr/bin/env python
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker.settings')
import django
django.setup()

import easyocr
from expenses.views import extract_amount_from_text, extract_date_from_text, extract_vendor_from_text
from pathlib import Path

receipts = list(Path('receipts.png').glob('*.png'))
print(f'Found {len(receipts)} receipts')

if receipts:
    for i, receipt_path in enumerate(receipts, 1):
        print(f'\n{"="*60}')
        print(f'Receipt {i}: {receipt_path.name}')
        print("="*60)
        
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(str(receipt_path))
        extracted_text = '\n'.join([detection[1] for detection in result])
        
        print('EXTRACTED TEXT:')
        print(extracted_text[:500])
        print()
        
        amount = extract_amount_from_text(extracted_text)
        date = extract_date_from_text(extracted_text)
        vendor = extract_vendor_from_text(extracted_text)
        
        print('PARSED DATA:')
        print(f'Amount: {amount}')
        print(f'Date: {date}')
        print(f'Vendor: {vendor}')
