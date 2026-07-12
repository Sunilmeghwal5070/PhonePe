import re

# Patch RechargeFlowScreens.kt
with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

helper = """
fun getPlanDetails(amount: Double): Pair<String, String> {
    val planAmt = amount.toInt()
    return when(planAmt) {
        299 -> "28 Days" to "1.5 GB/Day"
        479 -> "56 Days" to "1.5 GB/Day"
        719 -> "84 Days" to "1.5 GB/Day"
        29 -> "1 Day" to "2 GB"
        349 -> "28 Days" to "2.5 GB/Day"
        899 -> "90 Days" to "2.5 GB/Day"
        3599 -> "365 Days" to "2.5 GB/Day"
        26 -> "1 Day" to "1.5 GB"
        449 -> "28 Days" to "3 GB/Day"
        901 -> "84 Days" to "3 GB/Day"
        else -> "28 Days" to "1.5 GB/Day"
    }
}
"""

if "fun getPlanDetails" not in text:
    text += helper

# Fix hardcoded plan in RechargeSuccessScreen
plan_target = """                                Text("Validity", color = Color.Gray, fontSize = 13.sp)
                                Text("28 Days", color = Color.Black, fontSize = 14.sp)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("Data", color = Color.Gray, fontSize = 13.sp)
                                Text("1.5GB/Day", color = Color.Black, fontSize = 14.sp)"""

plan_replacement = """                                val details = getPlanDetails(currentTx.amount)
                                Text("Validity", color = Color.Gray, fontSize = 13.sp)
                                Text(details.first, color = Color.Black, fontSize = 14.sp)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("Data", color = Color.Gray, fontSize = 13.sp)
                                Text(details.second, color = Color.Black, fontSize = 14.sp)"""
text = text.replace(plan_target, plan_replacement)

# Fix payment details logic
amt_target = """                                Text("Recharge Amount", color = Color.Gray, fontSize = 14.sp)
                                Text("₹${(currentTx.amount - 3).toInt()}", color = Color.Gray, fontSize = 14.sp)"""
amt_replacement = """                                Text("Recharge Amount", color = Color.Gray, fontSize = 14.sp)
                                Text("₹${currentTx.amount.toInt()}", color = Color.Gray, fontSize = 14.sp)"""
text = text.replace(amt_target, amt_replacement)

plat_target = """                                Text("Platform fee(inclusive of GST)", color = Color.Gray, fontSize = 14.sp)
                                Text("+ ₹3", color = Color.Gray, fontSize = 14.sp)"""
plat_replacement = """                                Text("Platform fee(inclusive of GST)", color = Color.Gray, fontSize = 14.sp)
                                Text("+ ₹0", color = Color.Gray, fontSize = 14.sp)"""
text = text.replace(plat_target, plat_replacement)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)

# Patch HistoryScreen.kt
with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    hist_text = f.read()

hist_helper = """
fun getPlanDetailsHist(amount: Double): Pair<String, String> {
    val planAmt = amount.toInt()
    return when(planAmt) {
        299 -> "28 Days" to "1.5 GB/Day"
        479 -> "56 Days" to "1.5 GB/Day"
        719 -> "84 Days" to "1.5 GB/Day"
        29 -> "1 Day" to "2 GB"
        349 -> "28 Days" to "2.5 GB/Day"
        899 -> "90 Days" to "2.5 GB/Day"
        3599 -> "365 Days" to "2.5 GB/Day"
        26 -> "1 Day" to "1.5 GB"
        449 -> "28 Days" to "3 GB/Day"
        901 -> "84 Days" to "3 GB/Day"
        else -> "28 Days" to "1.5 GB/Day"
    }
}
"""
if "fun getPlanDetailsHist" not in hist_text:
    hist_text += hist_helper

hist_target = """            Text(
                text = if (isRecharge) { if(isFailed) "Mobile recharge for" else "Mobile recharged" } else if (isReceived) "Received from" else "Paid to",
                color = Color.Gray,
                fontSize = 12.sp
            )
            Text(
                text = tx.receiverName,
                color = Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )"""

hist_replacement = """            Text(
                text = if (isRecharge) { 
                    val details = getPlanDetailsHist(tx.amount)
                    if(isFailed) "Recharge failed - ${details.first}, ${details.second}" else "Mobile recharged - ${details.first}, ${details.second}" 
                } else if (isReceived) "Received from" else "Paid to",
                color = Color.Gray,
                fontSize = 12.sp
            )
            Text(
                text = tx.receiverName,
                color = Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )"""

hist_text = hist_text.replace(hist_target, hist_replacement)

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(hist_text)

