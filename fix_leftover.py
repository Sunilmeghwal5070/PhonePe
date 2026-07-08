with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

leftover = """        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = label,
            fontSize = 11.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign.Center,
            lineHeight = 13.sp
        )
    }
}
"""

if leftover in content:
    content = content.replace(leftover, "")
    print("Removed leftover lines!")
else:
    print("Leftover lines not found exactly. Let's use regex.")
    import re
    leftover_regex = r"""        Spacer\(modifier = Modifier\.height\(6\.dp\)\)
        Text\(
            text = label,
            fontSize = 11\.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign\.Center,
            lineHeight = 1[34]\.sp
        \)
    \}
\}"""
    if re.search(leftover_regex, content):
        content = re.sub(leftover_regex, "", content)
        print("Removed leftover lines with regex!")
    else:
        print("Still not found.")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
