with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'modifier = Modifier.align(Alignment.Center),' in line:
        new_lines.append('                            text = "Ad ${page + 1}\\n(Please add ad${page + 1}.png to res/drawable)",\n')
        new_lines.append(line)
    else:
        new_lines.append(line)

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.writelines(new_lines)
