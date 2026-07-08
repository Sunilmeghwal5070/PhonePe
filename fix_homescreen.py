with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    lines = f.readlines()

# find indices
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "// 3. Money Transfers Grid" in line:
        start_idx = i
    if "// 4. Two Capsule Ads Side-by-Side" in line:
        end_idx = i
        break
    if "// 4. Promo Capsules" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_block = """        // 3. Money Transfers Grid
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(vertical = 16.dp, horizontal = 12.dp)
            ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Money Transfers",
                            fontWeight = FontWeight.Bold,
                            color = PhonePeTextDark,
                            fontSize = 14.sp
                        )
                        
                        // Refer -> ₹200 bubble
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFFFF3E0))
                                .clickable {
                                    showDialogTitle = "Referral Bonus 💰"
                                    showDialogText = "Share the link of this app with your friends and get ₹200! 🤑🔥"
                                }
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.MonetizationOn,
                                contentDescription = null,
                                tint = Color(0xFFFF9800),
                                modifier = Modifier.size(14.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = "Refer → ₹200",
                                color = Color(0xFFE65100),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(18.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        TransferButton(
                            iconContent = { ToMobileIcon() },
                            label = "To Mobile\\nNumber",
                            onClick = onNavigateToContactList
                        )
                        TransferButton(
                            iconContent = { ToBankIcon() },
                            label = "To Bank &\\nSelf A/c",
                            onClick = onCreatePrank
                        )
                        TransferButton(
                            iconContent = { PhonePeWalletIcon() },
                            label = "PhonePe\\nWallet",
                            onClick = {}
                        )
                        TransferButton(
                            iconContent = { CheckBalanceIcon() },
                            label = "Check\\nBalance",
                            onClick = onNavigateToCheckBalance
                        )
                    }
                }
            }

"""
    lines[start_idx:end_idx] = [new_block]
    print("Replaced Money Transfers block!")

start_fn_idx = -1
end_fn_idx = -1
for i, line in enumerate(lines):
    if "fun TransferButton(" in line:
        start_fn_idx = i - 1  # include @Composable
    if start_fn_idx != -1 and i > start_fn_idx and line.strip() == "}":
        end_fn_idx = i + 1
        break

if start_fn_idx != -1 and end_fn_idx != -1:
    new_fn = """@Composable
fun TransferButton(
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
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = label,
            fontSize = 11.5.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign.Center,
            lineHeight = 15.sp,
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
                .offset(x = (-2).dp, y = 2.dp)
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
}
"""
    lines[start_fn_idx:end_fn_idx] = [new_fn]
    print("Replaced TransferButton function!")
    
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.writelines(lines)
