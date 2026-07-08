def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Change it.name to it.receiverName
    content = content.replace('it.name', 'it.receiverName')
    # Except we have tx.name, which we also need to change to tx.receiverName
    content = content.replace('tx.name', 'tx.receiverName')
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('/app/applet/app/src/main/java/com/example/ui/screens/ChatScreen.kt')
fix_file('/app/applet/app/src/main/java/com/example/ui/screens/SendMoneyScreen.kt')
