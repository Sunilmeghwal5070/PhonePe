import re
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# find Dialog warnings
parts = text.split('// Dialog warnings/pranks')

# We know the first part ends with too many or too few `}`.
# The structure of HomeScreen:
# fun HomeScreen(...) {
#   ...
#   LazyColumn(...) {
#       ...
#   } // end of LazyColumn
#   // Dialog warnings
#   if (...) {
#       AlertDialog(...)
#   }
# } // end of HomeScreen

# Let's count { and } in the first part
first_part = parts[0]
first_part = re.sub(r'\}\s*$', '', first_part) # remove trailing brackets
first_part = re.sub(r'\}\s*$', '', first_part)
first_part = re.sub(r'\}\s*$', '', first_part)
first_part = re.sub(r'\}\s*$', '', first_part)
first_part = re.sub(r'\}\s*$', '', first_part)
# now let's just append `    }\n\n    `
# wait, how many brackets to close the last `item { ... }` ?
# The last item was `item { Spacer(...) }` which we replaced maybe?
# The last item before we removed was:
#        item {
#            Spacer(modifier = Modifier.height(32.dp))
#        }

# Let's just find the last `}` in the first part and make sure it closes LazyColumn.
# Then we can just format properly.
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text) # Just to test python runs
