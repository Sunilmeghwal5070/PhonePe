import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

def replace_func(func_name, new_body):
    global text
    # This is a basic regex to replace a composable function that ends with a single brace (be careful with nested braces)
    # Since these are simple, let's just find them by index and replace.
    start_idx = text.find(f"fun {func_name}() {{")
    if start_idx != -1:
        # find the matching closing brace
        brace_count = 0
        end_idx = start_idx
        found_first = False
        for i in range(start_idx, len(text)):
            if text[i] == '{':
                brace_count += 1
                found_first = True
            elif text[i] == '}':
                brace_count -= 1
            
            if found_first and brace_count == 0:
                end_idx = i
                break
        
        old_code = text[start_idx:end_idx+1]
        text = text.replace(old_code, new_body)

new_to_mobile = """fun ToMobileIcon() {
    Box(
        modifier = Modifier.size(56.dp).clip(CircleShape).background(PhonePePurple),
        contentAlignment = Alignment.Center
    ) {
        Icon(imageVector = Icons.Default.ContactPhone, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
    }
}"""

new_to_bank = """fun ToBankIcon() {
    Box(
        modifier = Modifier.size(56.dp).clip(CircleShape).background(PhonePePurple),
        contentAlignment = Alignment.Center
    ) {
        Icon(imageVector = Icons.Default.AccountBalance, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
    }
}"""

new_wallet = """fun PhonePeWalletIcon() {
    Box(modifier = Modifier.size(60.dp), contentAlignment = Alignment.TopCenter) {
        Box(
            modifier = Modifier.size(56.dp).clip(CircleShape).background(PhonePePurple).align(Alignment.BottomCenter),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
        }
        Box(
            modifier = Modifier
                .background(Color(0xFFE65100), RoundedCornerShape(4.dp))
                .padding(horizontal = 4.dp, vertical = 2.dp)
        ) {
            Text("Cashback", color = Color.White, fontSize = 8.sp, fontWeight = FontWeight.Bold)
        }
    }
}"""

new_balance = """fun CheckBalanceIcon() {
    Box(
        modifier = Modifier.size(56.dp).clip(CircleShape).background(PhonePePurple),
        contentAlignment = Alignment.Center
    ) {
        Icon(imageVector = Icons.Default.AccountBalanceWallet, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
        // using wallet again, or currency rupee
    }
}"""

replace_func("ToMobileIcon", new_to_mobile)
replace_func("ToBankIcon", new_to_bank)
replace_func("PhonePeWalletIcon", new_wallet)
replace_func("CheckBalanceIcon", new_balance)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

print("Icons replaced")

