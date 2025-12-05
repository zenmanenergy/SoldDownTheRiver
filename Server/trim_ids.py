import re

# Read the file
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\test.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all HumanIds that are longer than 39 characters
long_ids = set(re.findall(r"'(HUM[a-f0-9\-]{37,})'", content))

print(f"Found {len(long_ids)} unique long HumanIds")

# Replace each long ID by removing dashes
for long_id in long_ids:
    if len(long_id) > 39:
        # Remove all dashes
        no_dash_id = long_id.replace('-', '')
        content = content.replace(f"'{long_id}'", f"'{no_dash_id}'")
        print(f"Removed dashes: {long_id} ({len(long_id)}) -> {no_dash_id} ({len(no_dash_id)})")

# Write back
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\test.sql', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFile updated successfully!")
