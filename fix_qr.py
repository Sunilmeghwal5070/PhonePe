with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("This is your prank QR code!", "This is your QR code!")

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(content)
