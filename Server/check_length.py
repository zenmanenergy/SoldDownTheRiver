with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\test.sql', 'r', encoding='utf-8') as f:
    content = f.read()
    
import re
# Find all HumanId values in the file
all_ids = re.findall(r"'(HUM[^']+)'", content)

print(f"Total HumanId values found: {len(all_ids)}")
print("\nChecking all HumanId values:")
long_ids = []
for humanid in set(all_ids):  # Use set to avoid duplicates
    if len(humanid) > 39:
        long_ids.append(humanid)
        print(f'Length {len(humanid)}: {humanid}')

if not long_ids:
    print("No HumanIds longer than 39 characters found")
else:
    print(f"\nTotal unique long IDs: {len(long_ids)}")
