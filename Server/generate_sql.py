import sys

# Read the data file
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Open output file
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\test.sql', 'w', encoding='utf-8') as out:
    
    # Process each line (skip header)
    for i, line in enumerate(lines):
        if i == 0:  # Skip header
            continue
        
        fields = line.rstrip('\n').split('\t')
        if len(fields) < 16:
            continue
        
        # Extract fields
        human_id = fields[0].replace('-', '')  # Remove dashes from UUID
        last_name = fields[1].replace("'", "''")  # Escape single quotes
        first_name = fields[2].replace("'", "''")
        sex = fields[3]
        age = fields[6]
        birth_date = fields[7]
        birth_date_accuracy = fields[8]
        color = fields[12].replace("'", "''")
        height_cm = fields[11]
        owner_humanid = fields[13] if fields[13].strip() else 'NULL'
        shippingagent_humanid = fields[14] if fields[14].strip() else 'NULL'
        owner2_humanid = fields[15] if fields[15].strip() else 'NULL'
        
        # Write INSERT for humans table
        out.write(f"INSERT INTO `SoldDownTheRiver`.`humans` ")
        out.write(f"(`HumanId`, `FirstName`, `LastName`, `isCompany`, `age_string`, `BirthDate`, `BirthDateAccuracy`, `RacialDescriptor`, `Sex`, `Height_cm`, `DateUpdated`, `isApproved`) ")
        out.write(f"VALUES ('{human_id}', '{first_name}', '{last_name}', 0, '{age}', '{birth_date}', '{birth_date_accuracy}', '{color}', '{sex}', {height_cm}, now(), 0);\n")
        
        # Write INSERT for voyagehumans table
        # We need a VoyageId - this should be provided or we'll use a placeholder
        voyage_id = 'NFNOLA0058'  # Replace with actual VoyageId
        
        out.write(f"INSERT INTO `SoldDownTheRiver`.`voyagehumans` ")
        out.write(f"(`VoyageId`, `HumanId`, `RoleId`, `DateUpdated`, `owner_humanid`, `shippingagent_humanid`, `owner2_humanid`, `collectoragent_humanid`) ")
        
        # Format owner fields - use NULL if empty, otherwise quote them
        owner_val = f"'{owner_humanid}'" if owner_humanid != 'NULL' else 'NULL'
        shipping_val = f"'{shippingagent_humanid}'" if shippingagent_humanid != 'NULL' else 'NULL'
        owner2_val = f"'{owner2_humanid}'" if owner2_humanid != 'NULL' else 'NULL'
        
        out.write(f"VALUES ('{voyage_id}', '{human_id}', 'Enslaved', now(), {owner_val}, {shipping_val}, {owner2_val}, NULL);\n\n")

print('SQL insert statements generated successfully')
