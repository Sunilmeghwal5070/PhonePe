import re

with open('app/src/main/java/com/example/ui/screens/ChatScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("it.receiverName.equals(contactName, ignoreCase = true)", "it.receiverName.trim().equals(contactName.trim(), ignoreCase = true)")

with open('app/src/main/java/com/example/ui/screens/ChatScreen.kt', 'w') as f:
    f.write(text)
