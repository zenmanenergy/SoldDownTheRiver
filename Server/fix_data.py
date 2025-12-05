import uuid
import datetime

# Read the data file
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Transaction date
trans_date = datetime.datetime(1825, 9, 24)

# Open output file
with open(r'c:\Apache24\htdocs\personalProjects\SoldDownTheRiver\Server\data.txt', 'w', encoding='utf-8') as out:
    
    # Process each line
    for i, line in enumerate(lines):
        if i == 0:  # Header - keep as is
            out.write(line)
            continue
        
        fields = line.rstrip('\n').split('\t')
        if len(fields) < 16:
            out.write(line)
            continue
        
        # 1) Generate 39 character HumanId (HUM + UUID without dashes = 3 + 32 = 35 chars, pad to 39)
        uuid_str = str(uuid.uuid4()).replace('-', '')  # 32 characters
        fields[0] = 'HUM' + uuid_str[:36]  # HUM (3) + 36 chars = 39 total
        
        # 2) Calculate BirthDate from Age
        try:
            age = float(fields[6])
            birth_date = trans_date - datetime.timedelta(days=age*365.25)
            fields[7] = birth_date.strftime('%Y-%m-%d')
        except:
            pass
        
        # 3) Calculate Height_cm from feet and inches
        try:
            feet = int(fields[9])
            inches_str = fields[10].strip()
            
            if ' ' in inches_str:
                parts = inches_str.split()
                whole = int(parts[0])
                if '/' in parts[1]:
                    num, den = parts[1].split('/')
                    frac_val = float(num) / float(den)
                else:
                    frac_val = 0
                total_inches = whole + frac_val
            elif '/' in inches_str:
                num, den = inches_str.split('/')
                total_inches = float(num) / float(den)
            else:
                total_inches = float(inches_str) if inches_str else 0
            
            height_cm = round((feet * 12 + total_inches) * 2.54, 2)
            fields[11] = str(height_cm)
        except:
            pass
        
        # Also ensure owner/shipping/owner2 humanids are 39 chars or less by removing dashes
        if fields[13].strip() and len(fields[13]) > 39:
            fields[13] = fields[13].replace('-', '')[:39]
        if fields[14].strip() and len(fields[14]) > 39:
            fields[14] = fields[14].replace('-', '')[:39]
        if fields[15].strip() and len(fields[15]) > 39:
            fields[15] = fields[15].replace('-', '')[:39]
        
        out.write('\t'.join(fields) + '\n')

print('Data file updated successfully!')
print('- Generated 39 character HumanIds')
print('- Calculated birth dates from ages')
print('- Calculated heights in cm')
