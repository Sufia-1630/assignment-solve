import json
import re
from collections import defaultdict

# Initialize counters and regular expression
null_counts = defaultdict(int)
lake_view_results = []

# Regular expression to detect "lake view" (case-insensitive)
lake_view_pattern = re.compile(r'\blake view\b', re.IGNORECASE)

# Open the JSON file line by line
with open('data.json', 'r') as file:
    for line in file:
        # Parse each JSON line
        property_data = json.loads(line)

        # 1. Identify Nullable Fields
        for key, value in property_data.items():
            if value is None:
                null_counts[key] += 1

        # 2. Identify 'Lake View' Properties
        has_lake_view = False

        # Check 'PublicRemarks'
        public_remarks = property_data.get('PublicRemarks', '')
        if isinstance(public_remarks, str) and lake_view_pattern.search(public_remarks):
            has_lake_view = True

        # Check 'WaterfrontFeatures[]'
        waterfront_features = property_data.get('WaterfrontFeatures', [])
        if isinstance(waterfront_features, list):
            for feature in waterfront_features:
                if isinstance(feature, str) and lake_view_pattern.search(feature):
                    has_lake_view = True
                    break

        # Check 'View[]'
        view_features = property_data.get('View', [])
        if isinstance(view_features, list):
            for view in view_features:
                if isinstance(view, str) and lake_view_pattern.search(view):
                    has_lake_view = True
                    break

        # Append the result for this property
        lake_view_results.append({'PropertyID': property_data.get('PropertyID'), 'LakeView': has_lake_view})

# Display Results

# 1. Output nullable fields and their null counts
print("Nullable Fields and Null Counts:")
for field, count in null_counts.items():
    print(f"{field}: {count}")

# 2. Output Lake View properties
print("\nProperties with Lake View:")
for result in lake_view_results:
    print(f"PropertyID: {result['PropertyID']}, LakeView: {result['LakeView']}")
