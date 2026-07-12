import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

# Fix case insensitive upi
text = text.replace('if (url.startsWith("upi://pay"))', 'if (url.lowercase().startsWith("upi://pay"))')

# Remove the Simulate Scan text button to avoid accidental clicks
pattern = re.compile(r'// Fake Scanner button.*?Text\(\s*"Simulate Scan".*?\.padding\(bottom = 24\.dp\)\s*\)', re.DOTALL)
text = pattern.sub('', text)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)

