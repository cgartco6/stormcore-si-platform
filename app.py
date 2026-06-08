import os
import io
import zipfile
import json
import uuid
import datetime
import hashlib
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pypdf import PdfReader
from openai import OpenAI

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "STORMCORE_SOVEREIGN_2026_MASTERKEY_X")

# Instantiate official 2026 modern OpenAI Engine Client layout
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "mock-key"))

# Core Mock System Data Tables Mapping
SYSTEM_DB = {
    "users": {
        "cust_1": {"role": "customer", "name": "John Doe", "tier": "free", "cv_text": "", "job_description": "", "optimized_cv": "", "cover_letter": "", "qa_prep": [], "usage_count": 0},
        "admin_1": {"role": "admin", "name": "System Administrator"},
        "owner_1": {"role": "owner", "name": "Stormcore Director"}
    },
    "transactions": [],
    "marketing_metrics": {"daily_signups_basic": 48, "total_ad_spend_zar": 12450.00, "conversions_today": 48, "impulse_clicks": 1420},
    "financial_ledgers": {"owner_standard_bank_total_zar": 125000.00, "admin_african_bank_total_zar": 25000.00, "company_registration_pool_zar": 4850.00, "hosting_fees_pool_zar": 0.00, "system_upgrades_pool_zar": 75000.00},
    "store_products": [
        {"id": "prod_1", "name": "Premium High-Trust Resume Rewrite Template Pack", "price": 150.00, "type": "once_off", "tier": "basic"},
        {"id": "prod_2", "name": "Pro Master Portfolio & LinkedIn Matrix Layouts", "price": 350.00, "type": "once_off", "tier": "pro"},
        {"id": "prod_3", "name": "Enterprise Career Launch Blueprint Suite", "price": 600.00, "type": "once_off", "tier": "enterprise"},
        {"id": "sub_1", "name": "Basic Career Tracker Subscription", "price": 120.00, "type": "subscription", "tier": "basic"},
        {"id": "sub_2", "name": "Pro Network Engagement Engine Subscription", "price": 300.00, "type": "subscription", "tier": "pro"},
        {"id": "sub_3", "name": "Enterprise Autopilot Executive Placement Subscription", "price": 550.00, "type": "subscription", "tier": "enterprise"},
        {"id": "sub_4", "name": "Sovereign Real-Time 2026 AI Coach Access Pack", "price": 450.00, "type": "subscription", "tier": "tutor"}
    ]
}

def get_session_user():
    if "user_id" not in session:
        session["user_id"] = "cust_1"
    uid = session["user_id"]
    return SYSTEM_DB["users"].get(uid, SYSTEM_DB["users"]["cust_1"])

def extract_text_from_pdf(file_bytes):
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = "".join([page.extract_text() or "" for page in reader.pages])
        return text.strip()
    except Exception as e:
        return f"PDF Extraction Error: {str(e)}"

def generate_pdf_bytes(title, content):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, leading=22, spaceAfter=12)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)
    story = [Paragraph(title, title_style), Spacer(1, 10)]
    for line in content.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

def generate_docx_bytes(title, content):
    doc = Document()
    doc.add_heading(title, level=1)
    for line in content.split('\n'):
        if line.strip():
            doc.add_paragraph(line.strip())
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out.getvalue()

def execute_ledger_split(amount_zar):
    ledger = SYSTEM_DB["financial_ledgers"]
    ledger["owner_standard_bank_total_zar"] += amount_zar * 0.50
    ledger["admin_african_bank_total_zar"] += amount_zar * 0.10
    ledger["system_upgrades_pool_zar"] += amount_zar * 0.30
    
    split_reg_or_hosting = amount_zar * 0.10
    if ledger["company_registration_pool_zar"] < 5000.00:
        ledger["company_registration_pool_zar"] += split_reg_or_hosting
        if ledger["company_registration_pool_zar"] > 5000.00:
            overflow = ledger["company_registration_pool_zar"] - 5000.00
            ledger["company_registration_pool_zar"] = 5000.00
            ledger["hosting_fees_pool_zar"] += overflow
    else:
        ledger["hosting_fees_pool_zar"] += split_reg_or_hosting

# --- Core UI Templates Navigation Routing Systems ---
@app.route('/')
def index(): return render_template('index.html', user=get_session_user())

@app.route('/store')
def store(): return render_template('store.html', products=SYSTEM_DB["store_products"], user=get_session_user())

@app.route('/cart')
def cart():
    if "cart" not in session: session["cart"] = []
    cart_items = [p for p in SYSTEM_DB["store_products"] if p["id"] in session["cart"]]
    return render_template('cart.html', cart=cart_items, total=sum(i["price"] for i in cart_items), user=get_session_user())

@app.route('/dashboard/customer')
def dashboard_customer(): return render_template('dashboard_customer.html', user=get_session_user())

@app.route('/dashboard/admin')
def dashboard_admin(): return render_template('dashboard_admin.html', user=get_session_user(), metrics=SYSTEM_DB["marketing_metrics"])

@app.route('/dashboard/owner')
def dashboard_owner(): return render_template('dashboard_owner.html', user=get_session_user(), ledgers=SYSTEM_DB["financial_ledgers"])

@app.route('/tutor')
def tutor(): return render_template('tutor.html', user=get_session_user())

@app.route('/payment')
def payment(): return render_template('payment.html', user=get_session_user())

@app.route('/marketing')
def marketing(): return render_template('marketing.html', user=get_session_user())

@app.route('/api/switch_role/<role>')
def switch_role(role):
    session["user_id"] = "admin_1" if role == "admin" else ("owner_1" if role == "owner" else "cust_1")
    return redirect('/')

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    pid = request.json.get("product_id")
    if "cart" not in session: session["cart"] = []
    if pid not in session["cart"]: session["cart"].append(pid)
    return jsonify({"status": "success", "cart_count": len(session["cart"])})

@app.route('/api/cart/clear')
def clear_cart():
    session["cart"] = []
    return redirect('/cart')

@app.route('/api/payment/checkout', methods=['POST'])
def api_checkout_process():
    gateway = request.json.get("gateway", "direct_eft")
    amount = float(request.json.get("amount", 0.00))
    tier_upgrade = request.json.get("tier", "free")
    
    if amount <= 0:
        return jsonify({"status": "error", "message": "Transaction requirements frame missing valid pricing parameter value."}), 400
        
    tx_id = f"STORMCORE-TX-{uuid.uuid4().hex[:10].upper()}"
    execute_ledger_split(amount)
    
    if get_session_user()["role"] == "customer":
        SYSTEM_DB["users"]["cust_1"]["tier"] = tier_upgrade
    
    if gateway == "payfast":
        pf_url = f"https://sandbox.payfast.co.za/eng/process?merchant_id=10000100&merchant_key=46f0cd694add8&amount={amount:.2f}&item_name=Stormcore_Access_Pack"
        session["cart"] = []
        return jsonify({"status": "redirect", "url": pf_url})
    elif gateway == "ozow":
        ozow_url = f"https://pay.ozow.com/?siteCode=STORMCORE01&BankReference={tx_id}&Amount={amount:.2f}&CurrencyCode=ZAR"
        session["cart"] = []
        return jsonify({"status": "redirect", "url": ozow_url})

    SYSTEM_DB["transactions"].append({"tx_id": tx_id, "amount": amount, "gateway": gateway, "timestamp": datetime.datetime.now().isoformat()})
    session["cart"] = []
    return jsonify({"status": "success", "message": "Payment recorded.", "tx_id": tx_id})

@app.route('/api/upload', methods=['POST'])
def api_upload():
    user = get_session_user()
    cv_text = request.form.get("cv_text", "").strip()
    job_desc = request.form.get("job_description", "").strip()
    
    if 'cv_file' in request.files:
        uploaded_file = request.files['cv_file']
        if uploaded_file.filename != '':
            ext = os.path.splitext(uploaded_file.filename)[1].lower()
            fb = uploaded_file.read()
            if ext == '.pdf': cv_text = extract_text_from_pdf(fb)
            elif ext in ['.txt', '.csv']: cv_text = fb.decode('utf-8', errors='ignore').strip()
            elif ext == '.docx':
                doc = Document(io.BytesIO(fb))
                cv_text = "\n".join([p.text for p in doc.paragraphs]).strip()

    if not cv_text or not job_desc:
        return jsonify({"status": "error", "message": "Please supply full text profiles or file sheets for both inputs."}), 400
        
    user["cv_text"] = cv_text
    user["job_description"] = job_desc
    return jsonify({"status": "success", "message": "Verification stream loaded successfully."})

# --- Real AI Implementation Layer with Structured Output Schemas ---
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    user = get_session_user()
    if not user["cv_text"] or not user["job_description"]:
        return jsonify({"status": "error", "message": "Data stream parameters incomplete."}), 400
        
    if user["tier"] == "free" and user["usage_count"] >= 1:
        return jsonify({"status": "error", "message": "Free tier limit reached. Upgrade to clear restrictions."}), 403

    # Define exact validation JSON schemas to force strict model outputs
    analysis_schema = {
        "name": "career_analysis_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "ats_score": {"type": "integer"},
                "optimized_cv": {"type": "string"},
                "cover_letter": {"type": "string"},
                "qa_prep": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"}
                        },
                        "required": ["question", "answer"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["ats_score", "optimized_cv", "cover_letter", "qa_prep"],
            "additionalProperties": False
        }
    }

    try:
        if os.environ.get("OPENAI_API_KEY") is None or os.environ.get("OPENAI_API_KEY") == "mock-key":
            # Fallback logic to protect local development loops safely
            mock_res = {"ats_score": 96, "optimized_cv": "Optimized Core Content", "cover_letter": "Cover Letter Text Content", "qa_prep": [{"question": "What is your main asset?", "answer": "Systems deployment."}]}
            user.update(mock_res)
            return jsonify(mock_res)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an automated corporate ATS processing parser. Read inputs and return compliant optimization frameworks strictly matching the provided JSON schema design format."},
                {"role": "user", "content": f"CV Content:\n{user['cv_text']}\n\nJob Target Specifications:\n{user['job_description']}"}
            ],
            response_format={"type": "json_schema", "json_schema": analysis_schema},
            temperature=0.2
        )
        parsed = json.loads(response.choices[0].message.content)
        user.update(parsed)
        if user["tier"] == "free": user["usage_count"] += 1
        return jsonify(parsed)
    except Exception as e:
        return jsonify({"status": "error", "message": f"AI Parsing Core Error: {str(e)}"}), 500

@app.route('/api/tutor/chat', methods=['POST'])
def api_tutor_chat():
    user = get_session_user()
    if user["tier"] == "free":
        return jsonify({"response": "The Live AI Interview Room requires an active premium system tier or subscription. Navigate to the store front grid node to update access parameters."})
        
    msg = request.json.get("message", "").strip()
    try:
        if os.environ.get("OPENAI_API_KEY") is None or os.environ.get("OPENAI_API_KEY") == "mock-key":
            return jsonify({"response": "[Mock AI Verification] To survive modern corporate tracking metrics, explain how you handle high-pressure scaling tasks within serverless application limits."})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a rigorous executive interviewer in 2026. Evaluate this candidate's inputs based on their resume profile context: {user.get('cv_text')} relative to this job profile description: {user.get('job_description')}. Be direct, point out any weaknesses in their responses, and present demanding subsequent questions."},
                {"role": "user", "content": msg}
            ],
            temperature=0.7
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download/<fmt>')
def download_compiled_file(fmt):
    user = get_session_user()
    cv_data = user.get("optimized_cv", "Run platform optimization cycle first.")
    cl_data = user.get("cover_letter", "Run platform optimization cycle first.")
    qa_data = "\n\n".join([f"Q: {i['question']}\nA: {i['answer']}" for i in user.get("qa_prep", [])])
    manifest = f"STORMCORE MASTER RECORD\n\n=== RESUME ===\n{cv_data}\n\n=== COVER LETTER ===\n{cl_data}\n\n=== PRACTICE ===\n{qa_data}"
    
    if fmt == "txt": return send_file(io.BytesIO(manifest.encode('utf-8')), mimetype='text/plain', as_attachment=True, download_name='Stormcore_Pack.txt')
    elif fmt == "csv": return send_file(io.BytesIO(f"Section,Data\n\"CV\",\"{cv_data}\"".encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='Stormcore_Data.csv')
    elif fmt == "pdf": return send_file(io.BytesIO(generate_pdf_bytes("Stormcore Build Export", manifest)), mimetype='application/pdf', as_attachment=True, download_name='Stormcore_Pack.pdf')
    elif fmt == "docx": return send_file(io.BytesIO(generate_docx_bytes("Stormcore Build Export", manifest)), mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name='Stormcore_Pack.docx')
    return jsonify({"status": "error", "message": "Invalid multi-format argument selection."}), 400

@app.route('/api/marketing/generate', methods=['POST'])
def api_generate_ads():
    platform = request.json.get("platform", "linkedin")
    tier = request.json.get("tier", "basic")
    
    marketing_schema = {
        "name": "ad_creative_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "ad_headline": {"type": "string"},
                "ad_body_text": {"type": "string"},
                "landing_page_title": {"type": "string"}
            },
            "required": ["ad_headline", "ad_body_text", "landing_page_title"],
            "additionalProperties": False
        }
    }

    try:
        if os.environ.get("OPENAI_API_KEY") is None or os.environ.get("OPENAI_API_KEY") == "mock-key":
            return jsonify({"ad_headline": "Direct Access Ad Header", "ad_body_text": "Compliant conversion ad text copy body blocks.", "landing_page_title": "Lander Title"})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Generate compliant high-converting ad variants for platform target: {platform.upper()} tailored specifically for market tier level: {tier.upper()} access profiles. Enforce compliance parameters strictly with zero false scarcity clocks."}],
            response_format={"type": "json_schema", "json_schema": marketing_schema},
            temperature=0.4
        )
        return jsonify(json.loads(response.choices[0].message.content))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
