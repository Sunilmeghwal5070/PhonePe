import re

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    content = f.read()

# We need to completely rewrite the UI of HistoryScreen to match the screenshot.
