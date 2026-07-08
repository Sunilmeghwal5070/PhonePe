with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    content = f.read()

imports = """import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.filled.PhoneIphone
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.foundation.border"""

if 'import androidx.compose.material.icons.filled.PhoneIphone' not in content:
    content = content.replace('import androidx.compose.ui.text.style.TextOverflow', imports)

index = content.find("@Composable\nfun HistoryItemRow(tx: PrankTransaction, onClick: () -> Unit) {")

replacement_row = """@Composable
fun HistoryItemRow(tx: PrankTransaction, onClick: () -> Unit) {
    val sdfDayMonth = remember { SimpleDateFormat("dd MMM", Locale.getDefault()) }
    val isReceived = tx.type == "RECEIVED"
    val isRecharge = tx.type == "RECHARGE"
    val isFailed = tx.status == "FAILED"
    
    val dateStr = remember(tx.timestamp) { 
        val now = System.currentTimeMillis()
        val diff = now - tx.timestamp
        if (diff < 24 * 60 * 60 * 1000) {
            val hours = diff / (60 * 60 * 1000)
            if (hours > 0) "$hours hours ago" else "Just now"
        } else {
            sdfDayMonth.format(Date(tx.timestamp))
        }
    }
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Icon Box
        Box(
            modifier = Modifier
                .size(44.dp)
                .background(if (isRecharge) Color.Transparent else Color(0xFFF3F4F6), RoundedCornerShape(if(isRecharge) 8.dp else 12.dp))
                .border(if (isRecharge) 1.dp else 0.dp, if(isRecharge) Color.LightGray else Color.Transparent, RoundedCornerShape(8.dp)),
            contentAlignment = Alignment.Center
        ) {
            if (isRecharge) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.PhoneIphone,
                        contentDescription = null,
                        tint = Color.Black,
                        modifier = Modifier.size(28.dp)
                    )
                    Icon(
                        imageVector = Icons.Default.Bolt,
                        contentDescription = null,
                        tint = Color.Black,
                        modifier = Modifier.size(16.dp)
                    )
                }
            } else {
                Icon(
                    imageVector = if (isReceived) Icons.AutoMirrored.Filled.CallReceived else Icons.AutoMirrored.Filled.CallMade,
                    contentDescription = null,
                    tint = Color.Black,
                    modifier = Modifier.size(24.dp)
                )
            }
        }
        
        Spacer(modifier = Modifier.width(16.dp))
        
        // Middle Column
        Column(modifier = Modifier.weight(1f)) {
            Text(
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
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = dateStr,
                color = Color.Gray,
                fontSize = 12.sp
            )
        }
        
        Spacer(modifier = Modifier.width(8.dp))
        
        // Right Column
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = if (isReceived) "+ ₹${tx.amount.toInt()}" else "₹${tx.amount.toInt()}",
                color = if (isReceived) Color(0xFF2E7D32) else Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (isFailed) {
                    Text("Failed", color = Color.Gray, fontSize = 12.sp)
                    Spacer(modifier = Modifier.width(4.dp))
                    Icon(
                        imageVector = Icons.Default.Error, // Red exclamation
                        contentDescription = "Failed",
                        tint = Color(0xFFD32F2F),
                        modifier = Modifier.size(14.dp)
                    )
                } else {
                    Text(
                        text = if (isReceived) "Credited to" else "Debited from",
                        color = Color.Gray,
                        fontSize = 12.sp
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    // Bank Logo
                    com.example.ui.components.BankLogo(bankName = tx.senderBankName, size = 16.dp)
                }
            }
        }
    }
}
"""

content = content[:index] + replacement_row

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(content)

