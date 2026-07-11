import re

with open('/app/applet/admin_panel.html', 'r') as f:
    content = f.read()

new_script = """    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>
    <script>
        // Replace with your Firebase config
        const firebaseConfig = {
            apiKey: "YOUR_API_KEY",
            authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
            projectId: "YOUR_PROJECT_ID",
            storageBucket: "YOUR_PROJECT_ID.appspot.com",
            messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
            appId: "YOUR_APP_ID"
        };
        
        let db;
        try {
            firebase.initializeApp(firebaseConfig);
            db = firebase.firestore();
        } catch(e) {
            console.error("Firebase init error: ", e);
        }

        // Data Structure for Keys
        let keysDB = [];
        let activityLog = JSON.parse(localStorage.getItem('activity_log')) || [];

        function saveDB() {
            // Firebase handles live updates, but we update UI
            updateDashboardStats();
        }
        
        async function fetchKeysFromFirebase() {
            if (!db) {
                alert("Please configure Firebase first in admin_panel.html!");
                keysDB = JSON.parse(localStorage.getItem('activation_keys')) || [];
                renderTable();
                return;
            }
            db.collection("activation_keys").onSnapshot((snapshot) => {
                keysDB = [];
                snapshot.forEach((doc) => {
                    keysDB.push(doc.data());
                });
                renderTable();
                updateDashboardStats();
            }, (error) => {
                console.error("Error fetching keys:", error);
            });
        }

        function logActivity(key, action) {
            activityLog.unshift({ key, action, time: new Date().toLocaleString() });
            if (activityLog.length > 20) activityLog.pop();
            localStorage.setItem('activity_log', JSON.stringify(activityLog));
            renderActivityLog();
        }

        function generateKeyString(type) {
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            const randomLetters = chars.charAt(Math.floor(Math.random() * 26)) + chars.charAt(Math.floor(Math.random() * 26));
            const randomDigits = Math.floor(1000 + Math.random() * 9000); // 4 digits
            
            // Format: Ph-1299-RK (as requested). If free, append FR
            if (type.startsWith('FREE')) {
                return `Ph-${randomDigits}-FR`;
            }
            return `Ph-${randomDigits}-${randomLetters}`;
        }

        async function generateSingleKey() {
            const type = document.getElementById('single-key-type').value;
            const ref = document.getElementById('single-key-ref').value || 'Manual';
            const keyStr = generateKeyString(type);
            
            const newKey = {
                key: keyStr,
                type: type,
                reference: ref,
                status: 'UNUSED',
                created: new Date().getTime(),
                activatedAt: null,
                expiresAt: null
            };
            
            if (db) {
                await db.collection("activation_keys").doc(keyStr).set(newKey);
            } else {
                keysDB.push(newKey);
                localStorage.setItem('activation_keys', JSON.stringify(keysDB));
            }
            
            logActivity(keyStr, `Generated (${type})`);
            
            const resultDiv = document.getElementById('single-key-result');
            resultDiv.innerText = `Generated Key: ${keyStr}`;
            resultDiv.classList.remove('hidden');
        }

        async function generateBulkKeys() {
            const qty = parseInt(document.getElementById('bulk-quantity').value);
            const type = document.getElementById('bulk-validity').value;
            
            if (qty < 1 || qty > 100) { alert('Please enter quantity between 1 and 100'); return; }
            
            let batch = db ? db.batch() : null;
            let generated = 0;
            for(let i=0; i<qty; i++) {
                const keyStr = generateKeyString(type);
                const newKey = {
                    key: keyStr,
                    type: type,
                    reference: `Bulk Gen #${Date.now().toString().slice(-4)}`,
                    status: 'UNUSED',
                    created: new Date().getTime(),
                    activatedAt: null,
                    expiresAt: null
                };
                
                if (db && batch) {
                    const docRef = db.collection("activation_keys").doc(keyStr);
                    batch.set(docRef, newKey);
                } else {
                    keysDB.push(newKey);
                }
                generated++;
            }
            
            if (db && batch) {
                await batch.commit();
            } else {
                localStorage.setItem('activation_keys', JSON.stringify(keysDB));
            }
            
            logActivity('MULTIPLE', `Bulk Generated ${qty} keys (${type})`);
            alert(`Successfully generated ${qty} keys!`);
            
            switchTab('manage');
        }

        async function changeKeyStatus(keyStr, newStatus) {
            const keyObj = keysDB.find(k => k.key === keyStr);
            if (keyObj) {
                let updates = { status: newStatus };
                
                // Simulate activation for testing
                if (newStatus === 'ACTIVE') {
                    updates.activatedAt = new Date().getTime();
                    let validityHours = 28 * 24; // Default Premium
                    if (keyObj.type === 'FREE_24') validityHours = 24;
                    if (keyObj.type === 'FREE_48') validityHours = 48;
                    updates.expiresAt = updates.activatedAt + (validityHours * 60 * 60 * 1000);
                }
                
                if (db) {
                    await db.collection("activation_keys").doc(keyStr).update(updates);
                } else {
                    Object.assign(keyObj, updates);
                    localStorage.setItem('activation_keys', JSON.stringify(keysDB));
                    renderTable();
                }
                
                logActivity(keyStr, `Status changed to ${newStatus}`);
            }
        }

        async function deleteKey(keyStr) {
            if (confirm(`Are you sure you want to delete ${keyStr}?`)) {
                if (db) {
                    await db.collection("activation_keys").doc(keyStr).delete();
                } else {
                    keysDB = keysDB.filter(k => k.key !== keyStr);
                    localStorage.setItem('activation_keys', JSON.stringify(keysDB));
                    renderTable();
                }
                logActivity(keyStr, 'Deleted');
            }
        }

        function getStatusBadge(status) {
            switch(status) {
                case 'UNUSED': return '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">Unused</span>';
                case 'ACTIVE': return '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Active</span>';
                case 'EXPIRED': return '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">Expired</span>';
                case 'BLOCKED': return '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-800 text-white">Blocked</span>';
                default: return status;
            }
        }

        function renderTable() {
            const tbody = document.getElementById('keys-table');
            const search = document.getElementById('search-key').value.toLowerCase();
            const filter = document.getElementById('filter-status').value;
            
            tbody.innerHTML = '';
            
            // Sort by created desc
            const sorted = [...keysDB].sort((a,b) => b.created - a.created);
            
            sorted.forEach(k => {
                if (filter !== 'ALL' && k.status !== filter) return;
                if (search && !k.key.toLowerCase().includes(search) && !k.reference.toLowerCase().includes(search)) return;
                
                const createdStr = new Date(k.created).toLocaleDateString();
                const expiresStr = k.expiresAt ? new Date(k.expiresAt).toLocaleString() : 'N/A';
                
                let actions = '';
                if (k.status === 'UNUSED') {
                    actions += `<button onclick="changeKeyStatus('${k.key}', 'ACTIVE')" class="text-green-600 hover:text-green-900 mx-1" title="Simulate Activation"><i class="fas fa-play"></i></button>`;
                }
                if (k.status !== 'BLOCKED' && k.status !== 'EXPIRED') {
                    actions += `<button onclick="changeKeyStatus('${k.key}', 'BLOCKED')" class="text-red-600 hover:text-red-900 mx-1" title="Block Key"><i class="fas fa-ban"></i></button>`;
                    actions += `<button onclick="changeKeyStatus('${k.key}', 'EXPIRED')" class="text-orange-600 hover:text-orange-900 mx-1" title="Force Expire"><i class="fas fa-hourglass-end"></i></button>`;
                } else if (k.status === 'BLOCKED') {
                    actions += `<button onclick="changeKeyStatus('${k.key}', 'UNUSED')" class="text-blue-600 hover:text-blue-900 mx-1" title="Unblock"><i class="fas fa-unlock"></i></button>`;
                }
                actions += `<button onclick="deleteKey('${k.key}')" class="text-gray-600 hover:text-gray-900 mx-1" title="Delete"><i class="fas fa-trash"></i></button>`;
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap font-mono font-bold text-gray-800">${k.key}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${k.type}<br><span class="text-xs text-gray-400">${k.reference}</span></td>
                    <td class="px-6 py-4 whitespace-nowrap">${getStatusBadge(k.status)}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${createdStr}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${expiresStr}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">${actions}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function updateDashboardStats() {
            document.getElementById('stat-total').innerText = keysDB.length;
            document.getElementById('stat-active').innerText = keysDB.filter(k => k.status === 'ACTIVE').length;
            document.getElementById('stat-inactive').innerText = keysDB.filter(k => k.status === 'EXPIRED' || k.status === 'BLOCKED').length;
            document.getElementById('stat-trial').innerText = keysDB.filter(k => k.type.startsWith('FREE')).length;
        }

        function renderActivityLog() {
            const tbody = document.getElementById('activity-log');
            tbody.innerHTML = '';
            activityLog.slice(0,10).forEach(log => {
                tbody.innerHTML += `
                    <tr>
                        <td class="px-4 py-2 font-mono text-sm">${log.key}</td>
                        <td class="px-4 py-2 text-sm text-gray-700">${log.action}</td>
                        <td class="px-4 py-2 text-xs text-gray-500">${log.time}</td>
                    </tr>
                `;
            });
        }

        function switchTab(tabId) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
            
            document.getElementById(`view-${tabId}`).classList.remove('hidden');
            document.getElementById(`tab-${tabId}`).classList.add('active');
            
            const titles = {
                'dashboard': 'Dashboard',
                'generate': 'Generate Keys',
                'manage': 'Manage Keys',
                'settings': 'Settings'
            };
            document.getElementById('page-title').innerText = titles[tabId];
            
            if (tabId === 'manage') renderTable();
            if (tabId === 'dashboard') {
                updateDashboardStats();
                renderActivityLog();
            }
        }

        // Initialize
        fetchKeysFromFirebase();
        renderActivityLog();
    </script>"""

content = re.sub(r'<script>.*?</script>', new_script, content, flags=re.DOTALL)

with open('/app/applet/admin_panel.html', 'w') as f:
    f.write(content)
