with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Dialog warnings" in line:
        print("Found Dialog at", i)
        print("Previous 10 lines:")
        for j in range(max(0, i-10), i):
            print(f"{j}: {lines[j].strip()}")
