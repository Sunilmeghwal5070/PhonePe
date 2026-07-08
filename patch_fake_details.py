import os
import re

files = [
    '/app/applet/app/src/main/java/com/example/ui/screens/EditDetailsScreen.kt',
    '/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt',
    '/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt',
    '/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt'
]

replacements = {
    "Yashwant Meghwal": "John Doe",
    "Sunil": "John",
    "6367512667": "9876543210",
    "sunilmeghwal6541@gmail.com": "johndoe@example.com",
    "NIMBAHERA": "MUMBAI MAIN",
    "UBIN0918610": "UBIN0000000",
    "sunilmeghwal6367": "johndoe123"
}

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        with open(filepath, 'w') as f:
            f.write(content)
