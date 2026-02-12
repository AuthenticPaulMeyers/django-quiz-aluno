import subprocess
import os

# Get pip freeze output
result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
content = result.stdout

# Write to file with UTF-8 (no BOM)
with open('requirements.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(content)

# Verify it's UTF-8
with open('requirements.txt', 'rb') as f:
    first_bytes = f.read(10)
    print(f'First bytes: {first_bytes}')
    print(f'File size: {os.path.getsize("requirements.txt")} bytes')
    
# Verify content
with open('requirements.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    print(f'First 3 lines:')
    for i, line in enumerate(lines[:3]):
        print(f'  {i+1}: {line.strip()}')
