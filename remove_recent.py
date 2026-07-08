import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

start_marker = "        // 9. Recent Pranks List / Empty state (History at bottom of home screen)"
end_marker = "        item {\n            // My QR Button Section"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Markers not found: start_idx={start_idx}, end_idx={end_idx}")
    exit(1)

new_content = content[:start_idx] + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(new_content)

print("Recent removed")
