with open('app/src/main/java/com/example/ui/screens/AlertsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("fake balance", "balance")
content = content.replace("Safe and Fun", "Safe and Secure")
content = content.replace("This app is 100% prank and fun. It has no connection to your real account. Have fun playing jokes with your friends!", "This app is secure and has no connection to your real account.")

with open('app/src/main/java/com/example/ui/screens/AlertsScreen.kt', 'w') as f:
    f.write(content)
