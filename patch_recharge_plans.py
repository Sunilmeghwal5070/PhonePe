import re

with open("app/src/main/java/com/example/ui/screens/RechargeScreens.kt", "r") as f:
    content = f.read()

# Update PlanCard
old_plancard = """@Composable
fun PlanCard(plan: RechargePlan, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp),
        shape = RoundedCornerShape(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("₹${plan.price}", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Icon(Icons.Default.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
            }
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Validity", color = Color.Gray, fontSize = 12.sp)
                    Text(plan.validity, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text("Data", color = Color.Gray, fontSize = 12.sp)
                    Text(plan.data, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(plan.description, color = Color.Gray, fontSize = 12.sp)
            Spacer(modifier = Modifier.height(8.dp))
            Text("Details", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp)
        }
    }
}"""

new_plancard = """@Composable
fun PlanCard(plan: RechargePlan, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("₹${plan.price}", fontSize = 22.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("VALIDITY", color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(plan.validity, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text("DATA", color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(plan.data, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text("VOICE", color = Color.Gray, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(4.dp))
                    Text("Unlimited", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text("Subscriptions: ${plan.description.take(15)}...", color = Color.Gray, fontSize = 12.sp)
        }
    }
}"""
content = content.replace(old_plancard, new_plancard)
content = content.replace("Icons.Default.KeyboardArrowRight", "Icons.AutoMirrored.Filled.KeyboardArrowRight")

with open("app/src/main/java/com/example/ui/screens/RechargeScreens.kt", "w") as f:
    f.write(content)
