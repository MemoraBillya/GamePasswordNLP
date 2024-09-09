from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = [
    {"username": "user1", "created_at": "2024-09-09 12:00"},
    {"username": "user2", "created_at": "2024-09-09 13:00"}
]

# Regex untuk validasi
def validate_password(password):
    conditions = []

    # 1. Setidaknya mengandung 5 karakter
    conditions.append(("Password harus memiliki setidaknya 5 karakter", len(password) >= 5))

    # 2. Mengandung angka
    conditions.append(("Password harus mengandung angka", bool(re.search(r'\d', password))))

    # 3. Mengandung huruf kapital
    conditions.append(("Password harus mengandung huruf kapital", bool(re.search(r'[A-Z]', password))))

    # 4. Mengandung karakter spesial
    conditions.append(("Password harus mengandung karakter spesial", bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))))

    # 5. Angka dalam password jika dijumlah harus 25
    digit_sum = sum(int(char) for char in password if char.isdigit())
    conditions.append(("Angka dalam password jika dijumlah harus lebih dari sama dengan dengan 25", digit_sum >= 25))

    # 6. Angka tidak boleh berdempetan
    conditions.append(("Angka tidak boleh berdempetan", not bool(re.search(r'\d{2,}', password))))

    # 7. Mengandung nama hari pada hari ini
    day_name = datetime.now().strftime('%A').lower()
    conditions.append((f"Password harus mengandung nama hari ini dalam bahasa inggris", day_name in password.lower()))

    # 8. Mengandung bulan dies natalis Unair (November/Nopember)
    conditions.append(("Password harus mengandung bulan dies natalis UNAIR", 'november' in password.lower() or 'nopember' in password.lower()))

    # 9. Akronim fakultas
    conditions.append(("Password harus mengandung akronim fakultas ini!", bool(re.search(r'FKM', password, re.IGNORECASE))))

    # 10. Mengandung dua huruf lambang unsur kimia
    conditions.append(("Password harus mengandung lambang unsur kimia dua huruf dari glolongan 1A", bool(re.search(r'(Li|Na|Rb|Cs|Fr)', password, re.IGNORECASE))))

    # 11. Mengandung emoji kucing
    conditions.append(("Ini Coco, jaga coco dengan memasukkannya ke dalam password 🐈", '🐈' in password))

    # 12. Mengandung kode hex warna (misalnya #FFFFFF)
    conditions.append(("Password harus mengandung kode hex warna", bool(re.search(r'#(?:[0-9a-fA-F]{3}){1,2}', password, re.IGNORECASE))))

    # 13. Mengandung mata uang negara Jepang (Yen)
    conditions.append(("Apa mata uang negara Jepang?", 'yen' in password.lower()))

    # 14. Mengandung captcha
    conditions.append(("Password harus mengandung jawaban captcha ini!", 'HJ9PV' in password))

    return conditions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validasi password
        all_conditions = validate_password(password)
        conditions_to_show = []

        # Cek hingga syarat tidak terpenuhi pertama kali
        for condition, met in all_conditions:
            conditions_to_show.append((condition, met))
            if not met:
                break
        
        all_conditions_met = all([cond[1] for cond in conditions_to_show])
        
        if not all_conditions_met:
            return render_template('index.html', username=username, password=password, conditions=conditions_to_show)
        else:
            # Simpan data pengguna
            users.append({"username": username, "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            flash('Akun berhasil dibuat!')
            return redirect(url_for('confirmation', username=username, password=password))
    
    return render_template('index.html', conditions=[])

@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'POST':
        confirm = request.form['confirm']
        if confirm == 'yes':
            flash('Akun berhasil dibuat!')
            return redirect(url_for('list_users'))
        else:
            return redirect(url_for('index'))
    
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('confirmation.html', username=username, password=password)

@app.route('/list')
def list_users():
    total_accounts = len(users)
    return render_template('list.html', users=users, total_accounts=total_accounts)

if __name__ == '__main__':
    app.run(debug=True)
