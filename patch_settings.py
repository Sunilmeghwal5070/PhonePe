import re

with open('/app/applet/admin_panel.html', 'r') as f:
    content = f.read()

settings_view = """
                <!-- Settings View -->
                <div id="view-settings" class="view-section hidden">
                    <div class="bg-white rounded-lg shadow p-6 max-w-2xl">
                        <h3 class="text-lg font-bold text-gray-800 mb-4">App Settings</h3>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Free Trial URL (e.g. gplinks)</label>
                            <input type="text" id="setting-free-url" placeholder="https://gplinks.com/..." class="w-full border-gray-300 rounded-md shadow-sm p-2 border focus:border-[#5f259f] focus:ring focus:ring-[#5f259f]/20">
                        </div>
                        <div>
                            <button onclick="saveSettings()" class="bg-[#5f259f] text-white font-bold py-2 px-6 rounded-md hover:bg-purple-800 transition">
                                Save Settings
                            </button>
                        </div>
                        <div id="settings-result" class="mt-4 text-green-600 hidden font-medium">Settings saved successfully!</div>
                    </div>
                </div>
            </main>
"""

content = content.replace('            </main>', settings_view)

script_additions = """
        // Settings logic
        async function fetchSettings() {
            if (db) {
                try {
                    const doc = await db.collection("app_settings").doc("urls").get();
                    if (doc.exists) {
                        const data = doc.data();
                        if (data.freeTrialUrl) {
                            document.getElementById('setting-free-url').value = data.freeTrialUrl;
                        }
                    }
                } catch(e) {
                    console.error("Error fetching settings:", e);
                }
            } else {
                const url = localStorage.getItem('freeTrialUrl');
                if (url) document.getElementById('setting-free-url').value = url;
            }
        }

        async function saveSettings() {
            const url = document.getElementById('setting-free-url').value;
            if (db) {
                try {
                    await db.collection("app_settings").doc("urls").set({ freeTrialUrl: url }, { merge: true });
                    showSettingsSuccess();
                } catch(e) {
                    console.error("Error saving settings:", e);
                    alert("Error saving settings.");
                }
            } else {
                localStorage.setItem('freeTrialUrl', url);
                showSettingsSuccess();
            }
        }

        function showSettingsSuccess() {
            const res = document.getElementById('settings-result');
            res.classList.remove('hidden');
            setTimeout(() => res.classList.add('hidden'), 3000);
        }

        // Add to initialization
"""

content = content.replace('        // Initialize', script_additions + '        // Initialize\n        fetchSettings();')

with open('/app/applet/admin_panel.html', 'w') as f:
    f.write(content)
