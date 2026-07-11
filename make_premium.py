import re

with open('/app/applet/admin_panel.html', 'r') as f:
    content = f.read()

# Extract JavaScript
script_match = re.search(r'<script>\s*(// Replace with your Firebase config.*?)\s*</script>', content, flags=re.DOTALL)
js_logic = script_match.group(1) if script_match else ""

# Premium HTML structure
new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Admin Panel - Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
        
        .glass-sidebar {{
            background: linear-gradient(135deg, #4c1d95 0%, #3b0764 100%);
            box-shadow: 4px 0 15px rgba(0,0,0,0.1);
        }}
        
        .sidebar-item {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .sidebar-item:hover, .sidebar-item.active {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            padding-left: 1rem;
        }}
        
        .sidebar-item.active::before {{
            content: '';
            position: absolute;
            left: -0.5rem;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 20px;
            background: #fff;
            border-radius: 0 4px 4px 0;
        }}
        
        .view-section {{
            animation: fadeIn 0.4s ease-out forwards;
            opacity: 0;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            border-radius: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.1);
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
            transition: all 0.3s;
        }}
        .btn-primary:hover {{
            background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(109, 40, 217, 0.3);
        }}

        .modal {{ display: none; }}
        .modal.active {{ display: flex; animation: fadeInModal 0.3s ease-out; }}
        
        @keyframes fadeInModal {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    </style>
</head>
<body class="text-gray-800 antialiased h-screen overflow-hidden flex">

    <!-- Sidebar -->
    <aside class="w-72 glass-sidebar text-white flex flex-col z-20">
        <div class="p-8 flex items-center space-x-4">
            <div class="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center backdrop-blur-sm">
                <i class="fas fa-shield-alt text-2xl"></i>
            </div>
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Admin<span class="font-light">Pro</span></h1>
                <p class="text-xs text-white/60 font-medium tracking-wider uppercase mt-1">Control Center</p>
            </div>
        </div>
        
        <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            <a href="#" onclick="switchTab('dashboard')" id="tab-dashboard" class="sidebar-item active flex items-center py-3.5 px-4 text-sm font-medium rounded-lg">
                <i class="fas fa-chart-pie w-8 text-lg opacity-80"></i> 
                <span>Dashboard</span>
            </a>
            <a href="#" onclick="switchTab('generate')" id="tab-generate" class="sidebar-item flex items-center py-3.5 px-4 text-sm font-medium rounded-lg">
                <i class="fas fa-key w-8 text-lg opacity-80"></i> 
                <span>Generate Keys</span>
            </a>
            <a href="#" onclick="switchTab('manage')" id="tab-manage" class="sidebar-item flex items-center py-3.5 px-4 text-sm font-medium rounded-lg">
                <i class="fas fa-layer-group w-8 text-lg opacity-80"></i> 
                <span>Manage Keys</span>
            </a>
            <a href="#" onclick="switchTab('settings')" id="tab-settings" class="sidebar-item flex items-center py-3.5 px-4 text-sm font-medium rounded-lg">
                <i class="fas fa-sliders-h w-8 text-lg opacity-80"></i> 
                <span>Settings</span>
            </a>
        </nav>
        
        <div class="p-6">
            <div class="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                <div class="flex items-center space-x-3 mb-2">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-400 to-pink-500 flex items-center justify-center shadow-lg">
                        <i class="fas fa-user text-xs"></i>
                    </div>
                    <div>
                        <p class="text-sm font-bold">Admin User</p>
                        <p class="text-xs text-white/60">System Admin</p>
                    </div>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
        
        <!-- Header -->
        <header class="bg-white/80 backdrop-blur-md shadow-sm z-10 px-8 py-5 flex justify-between items-center border-b border-gray-100">
            <h2 id="page-title" class="text-2xl font-bold text-gray-800 tracking-tight">Dashboard</h2>
            <div class="flex items-center space-x-5">
                <button class="text-gray-400 hover:text-purple-600 transition">
                    <i class="fas fa-bell text-xl"></i>
                </button>
                <button class="text-gray-400 hover:text-purple-600 transition">
                    <i class="fas fa-search text-xl"></i>
                </button>
            </div>
        </header>

        <!-- Content Area -->
        <main class="flex-1 overflow-x-hidden overflow-y-auto p-8 relative z-0">
            
            <!-- Dashboard View -->
            <div id="view-dashboard" class="view-section">
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <!-- Stat Card 1 -->
                    <div class="glass-card p-6 flex items-center justify-between">
                        <div>
                            <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Total Keys</p>
                            <h3 class="text-3xl font-bold text-gray-800" id="stat-total">0</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 shadow-inner">
                            <i class="fas fa-key text-xl"></i>
                        </div>
                    </div>
                    <!-- Stat Card 2 -->
                    <div class="glass-card p-6 flex items-center justify-between">
                        <div>
                            <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Active Keys</p>
                            <h3 class="text-3xl font-bold text-green-600" id="stat-active">0</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 shadow-inner">
                            <i class="fas fa-check-circle text-xl"></i>
                        </div>
                    </div>
                    <!-- Stat Card 3 -->
                    <div class="glass-card p-6 flex items-center justify-between">
                        <div>
                            <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Inactive/Blocked</p>
                            <h3 class="text-3xl font-bold text-red-500" id="stat-inactive">0</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center text-red-500 shadow-inner">
                            <i class="fas fa-ban text-xl"></i>
                        </div>
                    </div>
                    <!-- Stat Card 4 -->
                    <div class="glass-card p-6 flex items-center justify-between">
                        <div>
                            <p class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Trial Keys</p>
                            <h3 class="text-3xl font-bold text-blue-600" id="stat-trial">0</h3>
                        </div>
                        <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shadow-inner">
                            <i class="fas fa-gift text-xl"></i>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div class="lg:col-span-2 glass-card p-0 overflow-hidden">
                        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
                            <h3 class="text-lg font-bold text-gray-800">Recent Activity</h3>
                            <button onclick="switchTab('manage')" class="text-sm text-purple-600 font-medium hover:text-purple-800">View All</button>
                        </div>
                        <div class="p-0">
                            <table class="min-w-full divide-y divide-gray-100">
                                <thead class="bg-gray-50/50">
                                    <tr>
                                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Key</th>
                                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Action</th>
                                        <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Time</th>
                                    </tr>
                                </thead>
                                <tbody id="activity-log" class="divide-y divide-gray-50 bg-white/50">
                                    <!-- Activity injected here -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="glass-card p-6">
                        <h3 class="text-lg font-bold text-gray-800 mb-6">Quick Actions</h3>
                        <div class="space-y-4">
                            <button onclick="switchTab('generate')" class="w-full flex items-center justify-between p-4 rounded-xl border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition group">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center text-purple-600 group-hover:bg-purple-200 transition">
                                        <i class="fas fa-plus"></i>
                                    </div>
                                    <span class="font-semibold text-gray-700 group-hover:text-purple-700">Generate New Key</span>
                                </div>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                            </button>
                            <button onclick="switchTab('settings')" class="w-full flex items-center justify-between p-4 rounded-xl border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition group">
                                <div class="flex items-center space-x-3">
                                    <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center text-blue-600 group-hover:bg-blue-200 transition">
                                        <i class="fas fa-link"></i>
                                    </div>
                                    <span class="font-semibold text-gray-700 group-hover:text-blue-700">Update URLs</span>
                                </div>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Generate View -->
            <div id="view-generate" class="view-section hidden">
                <div class="glass-card p-8 max-w-2xl mx-auto">
                    <div class="text-center mb-8">
                        <div class="w-16 h-16 rounded-2xl bg-purple-100 flex items-center justify-center text-purple-600 mx-auto mb-4 shadow-inner">
                            <i class="fas fa-magic text-2xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-800">Generate Activation Key</h3>
                        <p class="text-gray-500 mt-2">Create new keys for users to access the application.</p>
                    </div>
                    
                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Key Validity Type</label>
                            <select id="key-type" class="w-full border-gray-200 rounded-xl shadow-sm p-3.5 border focus:border-purple-500 focus:ring focus:ring-purple-200 transition bg-white/50">
                                <option value="PREMIUM_MONTH">Premium - 28 Days</option>
                                <option value="FREE_24">Free Trial - 24 Hours</option>
                                <option value="FREE_48">Free Trial - 48 Hours</option>
                                <option value="PREMIUM_YEAR">Premium - 365 Days</option>
                            </select>
                        </div>
                        <div class="pt-2">
                            <button onclick="generateKey()" class="w-full btn-primary text-white font-bold py-4 px-6 rounded-xl shadow-lg flex justify-center items-center space-x-2">
                                <span>Generate Key</span>
                                <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                        
                        <div id="generated-result" class="hidden mt-8 p-6 bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-100 rounded-2xl text-center shadow-sm">
                            <p class="text-sm font-semibold text-purple-800 mb-2 uppercase tracking-wide">Success! New Key:</p>
                            <div class="flex items-center justify-center space-x-4">
                                <p id="new-key-display" class="text-3xl font-mono font-bold text-gray-900 tracking-wider bg-white px-4 py-2 rounded-lg shadow-inner"></p>
                                <button onclick="copyGeneratedKey()" class="w-12 h-12 bg-white rounded-lg shadow-sm border border-gray-200 hover:bg-gray-50 flex items-center justify-center text-gray-600 hover:text-purple-600 transition" title="Copy">
                                    <i class="fas fa-copy text-xl"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Manage View -->
            <div id="view-manage" class="view-section hidden">
                <div class="glass-card p-0 overflow-hidden flex flex-col h-[calc(100vh-140px)]">
                    
                    <div class="p-6 border-b border-gray-100 bg-white/50 flex flex-col md:flex-row justify-between items-center gap-4">
                        <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                            <i class="fas fa-database text-purple-500"></i> Key Database
                        </h3>
                        
                        <div class="flex flex-col md:flex-row gap-4 w-full md:w-auto">
                            <div class="relative">
                                <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                                <input type="text" id="search-key" placeholder="Search key or name..." oninput="renderTable()" class="pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl shadow-sm focus:border-purple-500 focus:ring focus:ring-purple-200 w-full md:w-64 transition bg-white/80">
                            </div>
                            <select id="filter-status" onchange="renderTable()" class="py-2.5 px-4 border border-gray-200 rounded-xl shadow-sm focus:border-purple-500 focus:ring focus:ring-purple-200 bg-white/80 transition">
                                <option value="ALL">All Status</option>
                                <option value="ACTIVE">Active</option>
                                <option value="UNUSED">Unused</option>
                                <option value="EXPIRED">Expired</option>
                                <option value="BLOCKED">Blocked</option>
                            </select>
                            <button onclick="fetchKeysFromFirebase()" class="bg-white border border-gray-200 text-gray-600 hover:text-purple-600 hover:border-purple-300 font-bold py-2.5 px-4 rounded-xl shadow-sm transition flex items-center gap-2">
                                <i class="fas fa-sync-alt"></i> Refresh
                            </button>
                        </div>
                    </div>
                    
                    <div class="overflow-x-auto flex-1 p-0">
                        <table class="min-w-full divide-y divide-gray-100">
                            <thead class="bg-gray-50/80 sticky top-0 backdrop-blur-sm z-10">
                                <tr>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Key</th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">User</th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Type / Ref</th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Created</th>
                                    <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Expires</th>
                                    <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="keys-table" class="divide-y divide-gray-50 bg-white/40">
                                <!-- Data injected here -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Settings View -->
            <div id="view-settings" class="view-section hidden">
                <div class="glass-card p-8 max-w-2xl mx-auto">
                    <div class="flex items-center gap-4 mb-8">
                        <div class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center text-gray-600">
                            <i class="fas fa-cog text-xl"></i>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-gray-800">App Settings</h3>
                            <p class="text-gray-500 text-sm">Configure global application parameters.</p>
                        </div>
                    </div>
                    
                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-semibold text-gray-700 mb-2">Free Trial Generation URL (e.g. gplinks)</label>
                            <div class="relative">
                                <i class="fas fa-link absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                                <input type="text" id="setting-free-url" placeholder="https://gplinks.com/..." class="pl-10 w-full border-gray-200 rounded-xl shadow-sm p-3 border focus:border-purple-500 focus:ring focus:ring-purple-200 transition bg-white/80">
                            </div>
                            <p class="text-xs text-gray-500 mt-2"><i class="fas fa-info-circle"></i> This URL is opened when users click "Get Free 24-Hour Trial Key" in the app.</p>
                        </div>
                        
                        <div class="pt-4 border-t border-gray-100">
                            <button onclick="saveSettings()" class="w-full btn-primary text-white font-bold py-3.5 px-6 rounded-xl shadow-lg flex justify-center items-center gap-2">
                                <i class="fas fa-save"></i> Save Configuration
                            </button>
                        </div>
                        
                        <div id="settings-result" class="hidden mt-4 bg-green-50 text-green-700 p-4 rounded-xl border border-green-200 flex items-center gap-3 font-medium">
                            <i class="fas fa-check-circle text-xl"></i> Settings saved successfully!
                        </div>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- User Details Modal -->
    <div id="user-details-modal" class="modal fixed inset-0 bg-gray-900/40 backdrop-blur-sm hidden items-center justify-center z-50 p-4">
        <div class="glass-card w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden animate-[fadeIn_0.3s_ease-out]">
            <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-white/50">
                <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                    <i class="fas fa-user-circle text-purple-600"></i> User App Data
                </h3>
                <button class="text-gray-400 hover:text-red-500 transition p-2" onclick="closeUserDetails()">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div id="user-details-content" class="p-6 overflow-y-auto flex-1 bg-white/30 text-sm text-gray-700">
                <!-- Content injected here -->
            </div>
        </div>
    </div>

    <script>
{js_logic}
    </script>
</body>
</html>
"""

# Let's fix the getStatusBadge in JS logic to match the new UI
js_logic = js_logic.replace(
    "case 'UNUSED': return '<span class=\"px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800\">Unused</span>';",
    "case 'UNUSED': return '<span class=\"px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-gray-100 text-gray-600 shadow-sm border border-gray-200\">Unused</span>';"
)
js_logic = js_logic.replace(
    "case 'ACTIVE': return '<span class=\"px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800\">Active</span>';",
    "case 'ACTIVE': return '<span class=\"px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-green-100 text-green-700 shadow-sm border border-green-200\">Active</span>';"
)
js_logic = js_logic.replace(
    "case 'EXPIRED': return '<span class=\"px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800\">Expired</span>';",
    "case 'EXPIRED': return '<span class=\"px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-orange-100 text-orange-700 shadow-sm border border-orange-200\">Expired</span>';"
)
js_logic = js_logic.replace(
    "case 'BLOCKED': return '<span class=\"px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-800 text-white\">Blocked</span>';",
    "case 'BLOCKED': return '<span class=\"px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-red-100 text-red-700 shadow-sm border border-red-200\">Blocked</span>';"
)

new_html = new_html.replace("{js_logic}", js_logic)

with open('/app/applet/admin_panel.html', 'w') as f:
    f.write(new_html)
