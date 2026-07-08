with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    lines = f.readlines()

out = []
i = 0
while i < len(lines):
    if "if (showRechargeReminder) {" in lines[i]:
        # Skip this block until the closing brace of the if statement
        while not "    }" in lines[i]:
            i += 1
        i += 1
        continue
    out.append(lines[i])
    i += 1

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.writelines(out)
