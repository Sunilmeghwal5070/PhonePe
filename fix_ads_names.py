with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val adResId = context.resources.getIdentifier("ad${page + 1}", "drawable", context.packageName)',
    'val adResId = context.resources.getIdentifier("ads${page + 1}", "drawable", context.packageName)'
)
content = content.replace(
    'text = "Ad ${page + 1}\\n(Please add ad${page + 1}.png to res/drawable)",',
    'text = "Ad ${page + 1}\\n(Please add ads${page + 1}.png to res/drawable)",'
)
with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
