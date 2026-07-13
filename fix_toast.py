import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace('Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()', 'Toast.makeText(context, "Incorrect UPI PIN (Default is 1234)", Toast.LENGTH_SHORT).show()')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
