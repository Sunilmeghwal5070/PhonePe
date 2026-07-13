import re
with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    text = f.read()

text = re.sub(r'if \(selectedBank != null && finalAmount > selectedBank!!.balance\) \{.*?return@PinEntryScreen\n\s+\}', '', text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(text)
