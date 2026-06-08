import os
import io
import uuid
from flask import Flask, request, send_file, redirect, url_for, render_template_string

# ==========================================
# 1. CORE SYSTEM INITIALIZATION
# ==========================================
app = Flask(__name__)
application = app  # Explicit WSGI entry pointer alignment for Vercel

# ==========================================
# 2. STATELESS STATIC DATA LAYER
# ==========================================
# Keeps data entirely in memory to prevent read-only filesystem faults
MOCK_USER_PAYLOAD = {
    "name": "Applicant Core Profile",
    "optimized_cv": "=== PROFESSIONAL EXPERIENCE ===\n- Managed high-end server configurations across infrastructure lines.\n- Handled enterprise operational targets smoothly.\n=== CORE EXPERTISE MATRIX ===\n- Project Scaling\n- Financial Risk Allocation Control"
}

# ==========================================
# 3. DIRECT EMBEDDED FRONTEND UI MATRIX
# ==========================================
# By rendering the UI strings directly from memory, we eliminate the 
# risk of Flask failing to locate or compile external HTML templates on Vercel.
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stormcore Career Suite</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen antialiased">

    <nav class="border-b border-slate-900 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="h-8 w-8 rounded-lg bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center font-black text-slate-950 tracking-tighter">S</div>
                <div>
                    <span class="text-sm font-black text-white tracking-tight uppercase block">Stormcore-SI</span>
                    <span class="text-[10px] text-slate-500 font-mono block">SYSTEM RUNNING // LIVE</span>
                </div>
            </div>
            <div class="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-full px-3 py-1 text-[11px] font-mono text-emerald-400">
                <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                Production Mode
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <div class="lg:col-span-2 space-y-6">
            <div class="bg-slate-900/40 border border-slate-900 rounded-2xl p-6 backdrop-blur-md shadow-xl space-y-4">
                <div class="flex items-center justify-between border-b border-slate-800/60 pb-3">
                    <div>
                        <h2 class="text-xs font-bold uppercase tracking-wider text-slate-400">Optimized Workspace</h2>
                        <h1 class="text-xl font-bold text-white tracking-tight mt-0.5">{{ user_data.name }}</h1>
                    </div>
                </div>

                <div class="bg-slate-950 rounded-xl p-5 border border-slate-900 font-mono text-xs text-slate-300 leading-relaxed max-h-[60vh] overflow-y-auto whitespace-pre-wrap">{{ user_data.optimized_cv }}</div>
            </div>
        </div>

        <div class="space-y-6">
            <div class="bg-slate-900/40 border border-slate-900 rounded-2xl p-6 space-y-6 backdrop-blur-md shadow-xl">
                <div>
                    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Visual Layout Stylist</h3>
                    <p class="text-[11px] text-slate-500 mt-0.5">Select alignment properties prior to compilation download.</p>
                </div>
                
                <div class="space-y-2.5">
                    <label class="flex items-center gap-3.5 p-3.5 bg-slate-950 border border-slate-900 rounded-xl cursor-pointer hover:border-slate-800 transition group">
                        <input type="radio" name="visual_style" value="professional" class="h-4 w-4 accent-emerald-500" checked>
                        <div>
                            <span class="text-xs font-bold text-slate-200 block">Corporate Professional</span>
                            <span class="text-[10px] text-slate-500 font-mono block">Executive Navy Layout</span>
                        </div>
                    </label>

                    <label class="flex items-center gap-3.5 p-3.5 bg-slate-950 border border-slate-900 rounded-xl cursor-pointer hover:border-slate-800 transition group">
                        <input type="radio" name="visual_style" value="modern" class="h-4 w-4 accent-emerald-500">
                        <div>
                            <span class="text-xs font-bold text-slate-200 block">Sleek Modern Slate</span>
                            <span class="text-[10px] text-slate-500 font-mono block">Emerald Green Accents</span>
                        </div>
                    </label>
                </div>

                <hr class="border-slate-900">

                <div>
                    <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">Asset Exporter</h3>
                    <p class="text-[11px] text-slate-500 mt-0.5">Natively compile and download structured text documents.</p>
                </div>
                
                <div class="space-y-2 text-xs font-semibold">
                    <button onclick="triggerDownload()" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-center text-slate-950 block rounded-xl transition-all font-black shadow-lg">
                        Export Text Layout (.txt)
                    </button>
                </div>
            </div>
        </div>
    </main>

    <script>
        function triggerDownload() {
            const selectedStyle = document.querySelector('input[name="visual_style"]:checked').value;
            window.location.href = `/api/download?style=${selectedStyle}`;
        }
    </script>
</body>
</html>
"""

# ==========================================
# 4. PRODUCTION ENDPOINTS
# ==========================================
@app.route('/')
@app.route('/dashboard/customer')
def customer_dashboard():
    # Renders string directly from application memory space safely
    return render_template_string(UI_TEMPLATE, user_data=MOCK_USER_PAYLOAD)

@app.route('/api/download')
def download_compiled_file():
    style_selection = request.args.get("style", "professional")
    
    # Creates raw structured layout text completely in-memory (0% disk tracking dependencies)
    output_text = f"STORMCORE COMPILED CV EXPORT\n"
    output_text += f"STYLE MATRIX MATCH: {style_selection.upper()}\n"
    output_text += f"==========================================\n\n"
    output_text += f"NAME: {MOCK_USER_PAYLOAD['name']}\n\n"
    output_text += MOCK_USER_PAYLOAD['optimized_cv']
    
    buffer = io.BytesIO()
    buffer.write(output_text.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"Stormcore_{style_selection}_Layout.txt"
    )

# Local diagnostic execution thread link
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
