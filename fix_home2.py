with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "if (showRechargeReminder) {" in line:
        skip = True
    if not skip:
        new_lines.append(line)

new_lines.append("}\n") # Wait, actually the original file ended with } from PrankItemRow

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.writelines(new_lines)
