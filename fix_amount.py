import re

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "val finalAmount = amount.toDoubleOrNull() ?: 100.0" in line:
        if any("val finalAmount" in l for l in new_lines[-5:]): # if we just added it recently
            continue
    if "showWrongPinScreen = true" in line and "return" not in line:
        new_lines.append(line)
        new_lines.append("                        return@PinEntryScreen\n")
        continue
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.writelines(new_lines)
