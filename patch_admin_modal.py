import re

with open('/app/applet/admin_panel.html', 'r') as f:
    content = f.read()

modal_html = """
    <!-- User Details Modal -->
    <div id="user-details-modal" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div class="flex justify-between items-center pb-3">
                <p class="text-2xl font-bold text-gray-800">User App Data</p>
                <div class="cursor-pointer z-50" onclick="closeUserDetails()">
                    <i class="fas fa-times text-gray-600 hover:text-red-500 text-xl"></i>
                </div>
            </div>
            <div id="user-details-content" class="mt-2 text-sm text-gray-700">
                <!-- Content injected here -->
            </div>
        </div>
    </div>
"""

content = content.replace('</body>', modal_html + '\n</body>')

actions_code = """
                if (k.appData || k.userName) {
                    actions += `<button onclick="viewUserDetails('${k.key}')" class="text-purple-600 hover:text-purple-900 mx-1" title="View User Data"><i class="fas fa-user"></i></button>`;
                }
                actions += `<button onclick="deleteKey('${k.key}')" class="text-gray-600 hover:text-gray-900 mx-1" title="Delete"><i class="fas fa-trash"></i></button>`;
"""

content = content.replace(
    "actions += `<button onclick=\"deleteKey('${k.key}')\" class=\"text-gray-600 hover:text-gray-900 mx-1\" title=\"Delete\"><i class=\"fas fa-trash\"></i></button>`;",
    actions_code
)

functions_code = """
        function viewUserDetails(keyStr) {
            const keyObj = keysDB.find(k => k.key === keyStr);
            if (!keyObj) return;

            let html = `<div class="mb-4"><span class="font-bold">Key:</span> ${keyObj.key}</div>`;
            html += `<div class="mb-4"><span class="font-bold">Activation Name:</span> ${keyObj.userName || 'N/A'}</div>`;
            
            if (keyObj.appData) {
                const data = keyObj.appData;
                html += `<div class="mb-4"><span class="font-bold">Last Sync:</span> ${new Date(data.lastSync).toLocaleString()}</div>`;
                
                if (data.accounts && data.accounts.length > 0) {
                    html += `<h4 class="font-bold text-lg mt-4 mb-2 border-b">Bank Accounts</h4>`;
                    html += `<table class="min-w-full divide-y divide-gray-200 mb-4">
                        <thead><tr><th class="px-2 py-1 text-left text-xs font-medium text-gray-500">Name</th><th class="px-2 py-1 text-left text-xs font-medium text-gray-500">Bank</th><th class="px-2 py-1 text-right text-xs font-medium text-gray-500">Balance</th></tr></thead>
                        <tbody>`;
                    data.accounts.forEach(acc => {
                        html += `<tr><td class="px-2 py-1">${acc.name}</td><td class="px-2 py-1">${acc.bank}</td><td class="px-2 py-1 text-right">₹${acc.balance.toFixed(2)}</td></tr>`;
                    });
                    html += `</tbody></table>`;
                }

                if (data.recentTransactions && data.recentTransactions.length > 0) {
                    html += `<h4 class="font-bold text-lg mt-4 mb-2 border-b">Recent Transactions</h4>`;
                    html += `<table class="min-w-full divide-y divide-gray-200 mb-4">
                        <thead><tr><th class="px-2 py-1 text-left text-xs font-medium text-gray-500">To</th><th class="px-2 py-1 text-right text-xs font-medium text-gray-500">Amount</th><th class="px-2 py-1 text-right text-xs font-medium text-gray-500">Date</th><th class="px-2 py-1 text-right text-xs font-medium text-gray-500">Status</th></tr></thead>
                        <tbody>`;
                    data.recentTransactions.forEach(tx => {
                        const date = new Date(tx.date).toLocaleDateString();
                        html += `<tr><td class="px-2 py-1">${tx.receiver}</td><td class="px-2 py-1 text-right">₹${tx.amount.toFixed(2)}</td><td class="px-2 py-1 text-right">${date}</td><td class="px-2 py-1 text-right">${tx.status}</td></tr>`;
                    });
                    html += `</tbody></table>`;
                }
            } else {
                html += `<div class="p-4 bg-gray-100 rounded text-gray-500 italic">No app data synced yet.</div>`;
            }

            document.getElementById('user-details-content').innerHTML = html;
            document.getElementById('user-details-modal').classList.remove('hidden');
        }

        function closeUserDetails() {
            document.getElementById('user-details-modal').classList.add('hidden');
        }
"""

content = content.replace(
    '        function switchTab(tabId) {',
    functions_code + '\n        function switchTab(tabId) {'
)

# Also let's show User Name in the table
table_head = """
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Key</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type / Ref</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Expires</th>
                                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
"""

content = re.sub(r'<thead class="bg-gray-50">.*?</thead>', table_head, content, flags=re.DOTALL)

tr_html = """
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap font-mono font-bold text-gray-800">${k.key}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600">${k.userName || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${k.type}<br><span class="text-xs text-gray-400">${k.reference}</span></td>
                    <td class="px-6 py-4 whitespace-nowrap">${getStatusBadge(k.status)}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${createdStr}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${expiresStr}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">${actions}</td>
                `;
"""

content = re.sub(r'const tr = document.createElement\(\'tr\'\);.*?`;', tr_html, content, flags=re.DOTALL)

with open('/app/applet/admin_panel.html', 'w') as f:
    f.write(content)
