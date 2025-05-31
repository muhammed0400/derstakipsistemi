from flask import Flask, render_template, redirect, url_for, session, request, flash
from veritabani_erisim import VeritabaniErisim

app = Flask(__name__, template_folder='templates')
app.secret_key = 'gizli_anahtar'
db = VeritabaniErisim()

# Veritabanı bağlantısını başlat
if not db.baglan():
    raise RuntimeError("Veritabanına bağlanılamadı!")

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/admin_giris', methods=['GET', 'POST'])
def admin_giris():
    if request.method == 'POST':
        kullanici_adi = request.form['kullanici_adi']
        sifre = request.form['sifre']
        
        # Admin kontrolü yapılacak
        if kullanici_adi == 'admin' and sifre == 'admin123':
            session.clear()
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('admin_giris.html', hata='Geçersiz kimlik bilgileri')
    return render_template('admin_giris.html')

@app.route('/dashboard')
def dashboard():
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    hocalar = db.tum_hocalari_getir()
    ogrenciler = db.tum_ogrencileri_getir()
    dersler = db.tum_dersleri_getir()
    return render_template('index.html', 
                         hocalar=hocalar,
                         ogrenciler=ogrenciler,
                         dersler=dersler)

@app.route('/hoca/<int:hoca_id>', methods=['GET', 'POST'])
def hoca_detay(hoca_id):
    if request.method == 'POST':
        ders_adi = request.form['ders_adi']
        result = db.ders_ekle(hoca_id, ders_adi)
        if result['status']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        return redirect(url_for('hoca_detay', hoca_id=hoca_id))
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    hoca = db.hoca_getir(hoca_id)
    hoca_dersleri = db.hocanin_verdigi_dersler(hoca_id)
    return render_template('hoca.html', 
                         dersler=hoca_dersleri,
                         hoca_id=hoca_id,
                         hoca=hoca)

@app.route('/ogrenci/<int:ogr_id>')
def ogrenci_detay(ogr_id):
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    ogrenci = db.ogrenci_getir(ogr_id)
    ogrenci_dersleri = db.ogrencinin_aldigi_dersler(ogr_id)
    tum_dersler = db.tum_dersleri_getir()
    return render_template('ogrenci.html', 
                         ogrenci=ogrenci,
                         dersler=ogrenci_dersleri,
                         tum_dersler=tum_dersler,
                         ogr_id=ogr_id)

@app.route('/ogrenci/ders_sec', methods=['POST'])
def ogrenci_ders_sec():
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    ogr_id = session['kullanici_id']
    secilen_dersler = request.form.getlist('dersler')
    
    if not secilen_dersler:
        flash('Lütfen en az bir ders seçiniz', 'error')
        return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))
    
    # Mevcut ders sayısını kontrol et
    mevcut_dersler = db.ogrencinin_aldigi_dersler(ogr_id)
    if len(mevcut_dersler) + len(secilen_dersler) > 8:
        flash('En fazla 8 ders seçebilirsiniz. Şu anda ' + str(len(mevcut_dersler)) + ' dersiniz var.', 'error')
        return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))
    
    basarili_dersler = []
    hatali_dersler = []
    
    for ders_id in secilen_dersler:
        result = db.ders_sec(ogr_id, ders_id)
        if result['status']:
            basarili_dersler.append(ders_id)
        else:
            hatali_dersler.append({'ders_id': ders_id, 'mesaj': result['message']})
    
    if basarili_dersler:
        if len(basarili_dersler) == len(secilen_dersler):
            flash('Tüm dersler başarıyla eklendi', 'success')
        else:
            flash(f'{len(basarili_dersler)} ders başarıyla eklendi', 'success')
    
    if hatali_dersler:
        for hata in hatali_dersler:
            ders = db.ders_getir(hata['ders_id'])
            if ders:
                flash(f"{ders['ders_adi']}: {hata['mesaj']}", 'error')
    
    return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))

@app.route('/ogrenci/ders_geri_al', methods=['POST'])
def ogrenci_ders_geri_al():
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    ogr_id = session['kullanici_id']
    ders_id = request.form.get('ders_id')
    
    if not ders_id:
        flash('Ders seçimi yapılmadı', 'error')
        return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))
    
    # Dersi kontrol et
    ders = db.ders_getir(ders_id)
    if not ders:
        flash('Ders bulunamadı', 'error')
        return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))
    
    result = db.ders_geri_al(ogr_id, ders_id)
    if result['status']:
        flash(f"{ders['ders_adi']} dersi başarıyla geri alındı", 'success')
    else:
        flash(f"{ders['ders_adi']}: {result['message']}", 'error')
    
    return redirect(url_for('ogrenci_detay', ogr_id=ogr_id))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/hoca_giris', methods=['GET', 'POST'])
def hoca_giris():
    if request.method == 'POST':
        email = request.form['email']
        sifre = request.form['sifre']
        hoca = db.hoca_giris_dogrula(email, sifre)
        if hoca:
            session['kullanici_id'] = hoca['hoca_id']
            session['kullanici_turu'] = 'hoca'
            return redirect(url_for('hoca_detay', hoca_id=session['kullanici_id']))
        return render_template('hoca_giris.html', hata='Geçersiz kimlik bilgileri')
    return render_template('hoca_giris.html')

@app.route('/ogrenci_giris', methods=['GET', 'POST'])
def ogrenci_giris():
    if request.method == 'POST':
        ogr_no = request.form['ogr_no']
        sifre = request.form['sifre']
        ogrenci = db.ogrenci_giris_dogrula(ogr_no, sifre)
        if ogrenci:
            session['kullanici_id'] = ogrenci['ogr_id']
            session['kullanici_turu'] = 'ogrenci'
            return redirect(url_for('ogrenci_detay', ogr_id=session['kullanici_id']))
        return render_template('ogrenci_giris.html', hata='Geçersiz kimlik bilgileri')
    return render_template('ogrenci_giris.html')

@app.route('/cikis')
def cikis():
    session.clear()
    return redirect(url_for('login'))

@app.route('/hoca/<int:hoca_id>/ders/<int:ders_id>/ogrenciler')
def ders_ogrencileri(hoca_id, ders_id):
    ogrenciler = db.dersi_alan_ogrenciler(ders_id, hoca_id)
    ders = db.ders_getir(ders_id)
    return render_template('ogrenci_listesi.html',
                         ogrenciler=ogrenciler,
                         hoca_id=hoca_id,
                         ders_id=ders_id,
                         ders=ders)

@app.route('/hoca/<int:hoca_id>/ders/<int:ders_id>/sil', methods=['POST'])
def ders_sil(hoca_id, ders_id):
    if 'kullanici_id' not in session and not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    result = db.ders_sil(hoca_id, ders_id)
    if result['status']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('hoca_detay', hoca_id=hoca_id))

if __name__ == '__main__':
    app.run(debug=True)