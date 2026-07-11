import re

with open('/app/applet/admin_panel.html', 'r') as f:
    content = f.read()

new_config = """const firebaseConfig = {
            apiKey: "AIzaSyAXw6__Llt1JYyPz3qv2hNx3VJ33pjhk64",
            authDomain: "phonepe-keys.firebaseapp.com",
            projectId: "phonepe-keys",
            storageBucket: "phonepe-keys.firebasestorage.app",
            messagingSenderId: "660537578846",
            appId: "1:660537578846:web:4d8e4aa8648f2670c46bcf",
            measurementId: "G-HWGB3SBX0H"
        };"""

content = re.sub(r'const firebaseConfig = \{.*?\};', new_config, content, flags=re.DOTALL)

with open('/app/applet/admin_panel.html', 'w') as f:
    f.write(content)
