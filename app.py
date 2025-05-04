from flask import Flask, request, jsonify, render_template
from config import Config
from supabase import create_client, Client
from datetime import datetime
import bcrypt
import google.generativeai as genai

app = Flask(__name__)

# Supabase istemcisi
url: str = Config.SUPABASE_URL
key: str = Config.SUPABASE_KEY
supabase: Client = create_client(url, key)

# Gemini API yapılandırması
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    # Kullanıcı zaten var mı?
    existing = supabase \
        .table('users') \
        .select('id') \
        .or_(f"username.eq.{username},email.eq.{email}") \
        .execute()
    if existing.data:
        return jsonify({'error': 'Kullanıcı adı veya e-posta zaten kayıtlı'}), 400

    # Şifre hash’leme
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    resp = supabase.table('users').insert({
        'username': username,
        'email': email,
        'password_hash': hashed
    }).execute()

    user_id = resp.data[0]['id']
    return jsonify({'message': 'Kayıt başarılı', 'user_id': user_id})

@app.route('/calculate', methods=['POST'])
def calculate_footprint():
    data = request.json
    energy_kwh = float(data['energy_kwh'])
    transport_km = float(data['transport_km'])
    food_type = data['food_type']
    user_id = int(data['user_id'])

    # Kullanıcı kontrolü
    user = supabase.table('users').select('id').eq('id', user_id).single().execute()
    if not user.data:
        return jsonify({'error': 'Kullanıcı bulunamadı'}), 400

    # CO2e hesaplama
    energy_factor = 0.5
    transport_factor = 0.2
    food_factors = {'vegetarian': 2.0, 'meat': 15.0}
    co2e = (energy_kwh * energy_factor) + (transport_km * transport_factor) + food_factors.get(food_type, 2.0)

    # Gemini’den öneri al
    prompt = f"Kullanıcının karbon ayak izi {co2e:.2f} kg CO2e. Azaltmak için 3 öneri sun."
    recommendation = model.generate_content(prompt).text

    # Veritabanına kaydet
    supabase.table('records').insert({
        'user_id': user_id,
        'energy_kwh': energy_kwh,
        'transport_km': transport_km,
        'food_type': food_type,
        'co2e_kg': co2e,
        'recommendation': recommendation
    }).execute()

    return jsonify({'co2e': co2e, 'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)