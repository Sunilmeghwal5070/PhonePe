import re

with open('public/generate_key.html', 'r') as f:
    content = f.read()

# 1. Add Timer UI HTML
html_to_add = """
        <div id="timer-container" class="hidden mt-6 bg-purple-50 p-4 rounded-xl border border-purple-100">
            <p class="text-sm text-purple-800 font-semibold mb-1">Next free key available in:</p>
            <div id="countdown" class="text-2xl font-mono font-bold text-purple-600">24:00:00</div>
        </div>
        
        <div id="error-container" class="hidden text-red-500 mt-4 p-4 bg-red-50 rounded-lg">"""

content = content.replace(
    '        <div id="error-container" class="hidden text-red-500 mt-4 p-4 bg-red-50 rounded-lg">',
    html_to_add
)

# 2. Add Timer Logic JS
js_logic_old = """        let db;
        try {
            firebase.initializeApp(firebaseConfig);
            db = firebase.firestore();
            generateFreeKey();
        } catch(e) {
            showError(e.message);
        }

        async function generateFreeKey() {"""

js_logic_new = """        let db;
        try {
            firebase.initializeApp(firebaseConfig);
            db = firebase.firestore();
            checkAndGenerateKey();
        } catch(e) {
            showError(e.message);
        }

        let timerInterval;

        function checkAndGenerateKey() {
            const lastGenTime = localStorage.getItem('phonepe_free_key_time');
            const lastGenKey = localStorage.getItem('phonepe_free_key_value');
            const now = new Date().getTime();
            const cooldown = 24 * 60 * 60 * 1000;

            if (lastGenTime && lastGenKey && (now - parseInt(lastGenTime)) < cooldown) {
                document.getElementById('loading').classList.add('hidden');
                document.getElementById('generated-key').innerText = lastGenKey;
                document.getElementById('key-container').classList.remove('hidden');
                document.getElementById('timer-container').classList.remove('hidden');
                startTimer(parseInt(lastGenTime), cooldown);
            } else {
                generateFreeKey();
            }
        }

        function startTimer(startTime, cooldown) {
            if (timerInterval) clearInterval(timerInterval);
            
            function updateTimer() {
                const now = new Date().getTime();
                const diff = cooldown - (now - startTime);
                
                if (diff <= 0) {
                    clearInterval(timerInterval);
                    document.getElementById('countdown').innerText = "00:00:00";
                    localStorage.removeItem('phonepe_free_key_time');
                    localStorage.removeItem('phonepe_free_key_value');
                    location.reload();
                    return;
                }
                
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);
                
                document.getElementById('countdown').innerText = 
                    String(hours).padStart(2, '0') + ':' + 
                    String(minutes).padStart(2, '0') + ':' + 
                    String(seconds).padStart(2, '0');
            }
            
            updateTimer();
            timerInterval = setInterval(updateTimer, 1000);
        }

        async function generateFreeKey() {"""

content = content.replace(js_logic_old, js_logic_new)

# 3. Save state when key is generated
gen_success_old = """                document.getElementById('loading').classList.add('hidden');
                document.getElementById('generated-key').innerText = keyStr;
                document.getElementById('key-container').classList.remove('hidden');
            } catch(error) {"""

gen_success_new = """                document.getElementById('loading').classList.add('hidden');
                document.getElementById('generated-key').innerText = keyStr;
                document.getElementById('key-container').classList.remove('hidden');
                
                const now = new Date().getTime();
                localStorage.setItem('phonepe_free_key_time', now.toString());
                localStorage.setItem('phonepe_free_key_value', keyStr);
                document.getElementById('timer-container').classList.remove('hidden');
                startTimer(now, 24 * 60 * 60 * 1000);
            } catch(error) {"""

content = content.replace(gen_success_old, gen_success_new)

with open('public/generate_key.html', 'w') as f:
    f.write(content)
