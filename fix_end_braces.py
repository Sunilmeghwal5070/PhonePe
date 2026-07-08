def remove_extra_brace(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    depth = 0
    for i, line in enumerate(lines):
        depth += line.count('{') - line.count('}')
        if depth < 0:
            print(f"File {filepath} went negative at line {i+1}")
            # we should remove this line's closing brace or something.
            
    if depth < 0:
        # Just remove the last abs(depth) closing braces from the end of the file
        removed = 0
        for i in range(len(lines)-1, -1, -1):
            if '}' in lines[i]:
                lines[i] = lines[i].replace('}', '', 1)
                removed += 1
                if removed == abs(depth):
                    break
        with open(filepath, "w") as f:
            f.writelines(lines)
        print(f"Fixed {filepath} by removing {removed} extra closing braces at the end.")
    elif depth > 0:
        print(f"File {filepath} is missing {depth} closing braces!")
        lines.append('}' * depth + '\n')
        with open(filepath, "w") as f:
            f.writelines(lines)
    else:
        print(f"File {filepath} is perfectly balanced.")

remove_extra_brace("app/src/main/java/com/example/ui/screens/HomeScreen.kt")
remove_extra_brace("app/src/main/java/com/example/MainActivity.kt")
