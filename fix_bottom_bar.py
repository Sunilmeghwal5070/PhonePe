import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

target = """            if (currentRoute in listOf("home", "search", "qr", "alerts", "history")) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(64.dp)
                        .background(Color.White),
                    horizontalArrangement = Arrangement.SpaceAround,
                    verticalAlignment = Alignment.CenterVertically
                ) {"""

replacement = """            if (currentRoute in listOf("home", "search", "qr", "alerts", "history")) {
                Column(modifier = Modifier.background(Color.White).navigationBarsPadding()) {
                    Divider(color = Color(0xFFEEEEEE), thickness = 1.dp)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(64.dp)
                            .background(Color.White),
                        horizontalArrangement = Arrangement.SpaceAround,
                        verticalAlignment = Alignment.CenterVertically
                    ) {"""

text = text.replace(target, replacement)

target2 = """                        }
                    }
                }
            }
        }
    ) { innerPadding ->"""

replacement2 = """                        }
                    }
                }
                } // End Column for navigation bars padding
            }
        }
    ) { innerPadding ->"""

text = text.replace(target2, replacement2)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
