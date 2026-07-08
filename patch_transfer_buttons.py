import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Let's remove the old TransferButton and add the new ones.
old_transfer_button = r"""fun TransferButton\(
    icon: ImageVector,
    label: String,
    onClick: \(\) -> Unit
\) \{
    Column\(
        horizontalAlignment = Alignment\.CenterHorizontally,
        modifier = Modifier
            \.width\(80\.dp\)
            \.clickable \{ onClick\(\) \}
    \) \{
        Box\(
            modifier = Modifier
                \.size\(48\.dp\)
                \.clip\(CircleShape\)
                \.background\(PhonePePurple\),
            contentAlignment = Alignment\.Center
        \) \{
            Icon\(
                imageVector = icon,
                contentDescription = null,
                tint = Color\.White,
                modifier = Modifier\.size\(24\.dp\)
            \)
        \}
        Spacer\(modifier = Modifier\.height\(6\.dp\)\)
        Text\(
            text = label,
            fontSize = 11\.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign\.Center,
            lineHeight = 14\.sp,
            fontWeight = FontWeight\.Medium
        \)
    \}
\}"""

new_transfer_button = """fun TransferButton(
    iconContent: @Composable () -> Unit,
    label: String,
    onClick: () -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .width(85.dp)
            .clickable { onClick() }
    ) {
        iconContent()
        Spacer(modifier = Modifier.height(10.dp))
        Text(
            text = label,
            fontSize = 12.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign.Center,
            lineHeight = 16.sp,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
fun ToMobileIcon() {
    Box(
        modifier = Modifier.size(60.dp)
    ) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple)
                .align(Alignment.Center),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(26.dp, 36.dp)
                    .border(2.dp, Color.White, RoundedCornerShape(6.dp))
                    .clip(RoundedCornerShape(6.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(16.dp).offset(y = (-4).dp)
                )
                Icon(
                    imageVector = Icons.Default.Phone,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(12.dp).offset(y = 6.dp)
                )
            }
        }
        // Green badge
        Box(
            modifier = Modifier
                .size(14.dp)
                .align(Alignment.TopEnd)
                .offset(x = (-4).dp, y = 4.dp)
                .background(PhonePeSuccessGreen, CircleShape)
                .border(2.dp, Color.White, CircleShape)
        )
    }
}

@Composable
fun ToBankIcon() {
    Box(modifier = Modifier.size(60.dp), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.AccountBalance,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(32.dp)
            )
        }
    }
}

@Composable
fun PhonePeWalletIcon() {
    Box(modifier = Modifier.size(60.dp)) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple)
                .align(Alignment.Center),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.AccountBalanceWallet,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(32.dp).offset(x = (-2).dp, y = 2.dp)
            )
            Text("₹", color = PhonePePurple, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.offset(x = 1.dp, y = 2.dp))
        }
        // Badge
        Box(
            modifier = Modifier
                .align(Alignment.TopCenter)
                .background(Color(0xFFD32F2F), RoundedCornerShape(4.dp))
                .padding(horizontal = 4.dp, vertical = 2.dp)
        ) {
            Text("2% back", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun CheckBalanceIcon() {
    Box(modifier = Modifier.size(60.dp), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(24.dp, 32.dp)
                    .background(Color.White, RoundedCornerShape(4.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text("₹", color = PhonePePurple, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}"""

content = re.sub(old_transfer_button, new_transfer_button, content)

# Now we must update the calls to TransferButton inside HomeScreen.kt

old_transfer_calls = r"""                        TransferButton\(
                            icon = Icons\.Default\.PhoneAndroid,
                            label = "To Mobile\nNumber",
                            onClick = onNavigateToContactList
                        \)
                        TransferButton\(
                            icon = Icons\.Default\.AccountBalance,
                            label = "To Bank &\nSelf A/c",
                            onClick = onCreatePrank
                        \)
                        // PhonePe Wallet with "2% back" badge!
                        Box\(modifier = Modifier\.width\(80\.dp\)\) \{
                            TransferButton\(
                                icon = Icons\.Default\.AccountBalanceWallet,
                                label = "PhonePe\nWallet",
                                onClick = \{\}
                            \)
                            Box\(
                                modifier = Modifier
                                    \.align\(Alignment\.TopCenter\)
                                    \.offset\(y = \(-8\)\.dp\)
                                    \.background\(Color\(0xFFD32F2F\), RoundedCornerShape\(4\.dp\)\)
                                    \.padding\(horizontal = 4\.dp, vertical = 2\.dp\)
                            \) \{
                                Text\("2% back", color = Color\.White, fontSize = 8\.sp, fontWeight = FontWeight\.Bold\)
                            \}
                        \}
                        TransferButton\(
                            icon = Icons\.Default\.CurrencyRupee,
                            label = "Check\nBalance",
                            onClick = onNavigateToCheckBalance
                        \)"""

new_transfer_calls = """                        TransferButton(
                            iconContent = { ToMobileIcon() },
                            label = "To Mobile\nNumber",
                            onClick = onNavigateToContactList
                        )
                        TransferButton(
                            iconContent = { ToBankIcon() },
                            label = "To Bank &\nSelf A/c",
                            onClick = onCreatePrank
                        )
                        TransferButton(
                            iconContent = { PhonePeWalletIcon() },
                            label = "PhonePe\nWallet",
                            onClick = {}
                        )
                        TransferButton(
                            iconContent = { CheckBalanceIcon() },
                            label = "Check\nBalance",
                            onClick = onNavigateToCheckBalance
                        )"""

content = re.sub(old_transfer_calls, new_transfer_calls, content)

# Remove the Card wrapper for Money Transfers to make it full width white block
old_card_wrapper = r"""        // 3\. Money Transfers Grid
        item \{
            Card\(
                colors = CardDefaults\.cardColors\(containerColor = Color\.White\),
                shape = RoundedCornerShape\(12\.dp\),
                elevation = CardDefaults\.cardElevation\(1\.dp\),
                modifier = Modifier
                    \.fillMaxWidth\(\)
                    \.padding\(12\.dp\)
            \) \{
                Column\(modifier = Modifier\.padding\(14\.dp\)\) \{"""

new_card_wrapper = """        // 3. Money Transfers Grid
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(vertical = 16.dp, horizontal = 12.dp)
            ) {"""

# And replace the ending brace of the Card block
old_card_end = r"""                        \)
                    \}
                \}
            \}
        \}"""

new_card_end = """                        )
                    }
                }
            }
        }"""

content = re.sub(old_card_wrapper, new_card_wrapper, content)
content = re.sub(old_card_end, new_card_end, content)


with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
