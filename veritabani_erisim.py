import getpass
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class VeritabaniErisim:
    def __init__(self):
        self.engine = None
        self.connection = None
    
    # Hoca giriş doğrulama metodu eklendi
    def hoca_giris_dogrula(self, email, sifre):
        try:
            sorgu = text("SELECT * FROM hocalar WHERE email = :email AND sifre = :sifre")
            result = self.connection.execute(sorgu, {"email": email, "sifre": sifre})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Hoca giriş sorgu hatası: {err}")
            return None
    
    # Öğrenci giriş doğrulama metodu eklendi        
    def ogrenci_giris_dogrula(self, ogr_no, sifre):
        try:
            sorgu = text("SELECT * FROM ogrenciler WHERE ogr_no = :ogr_no AND sifre = :sifre")
            result = self.connection.execute(sorgu, {"ogr_no": ogr_no, "sifre": sifre})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Öğrenci giriş sorgu hatası: {err}")
            return None

    def ogrenci_getir(self, ogr_id):
        try:
            sorgu = text("SELECT * FROM ogrenciler WHERE ogr_id = :ogr_id")
            result = self.connection.execute(sorgu, {"ogr_id": ogr_id})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Öğrenci sorgulama hatası: {err}")
            return None

    def admin_giris_dogrula(self, email, sifre):
        try:
            sorgu = text("SELECT * FROM admin WHERE ad_mail = :email AND ad_sifre = :sifre")
            result = self.connection.execute(sorgu, {"email": email, "sifre": sifre})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Admin giriş sorgu hatası: {err}")
            return None

    def baglan(self, host='localhost', kullanici='root', sifre=None, veritabani='proje'):
        try:
            if sifre is None:
                sifre = getpass.getpass("MySQL sifrenizi girin: ")
            
            DATABASE_URI = f'mysql+pymysql://{kullanici}:{sifre}@{host}:3306/{veritabani}'
            self.engine = create_engine(DATABASE_URI)
            self.connection = self.engine.connect()
            print(f"'{veritabani}' veritabanina baglandi!")
            return True
        except SQLAlchemyError as err:
            print(f"Baglanti hatasi: {err}")
            return False
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            return False
    
    def baglanti_kapat(self):
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
            print("Veritabanı bağlantısı kapatıldı.")
    
    def tum_hocalari_getir(self):
        try:
            result = self.connection.execute(text("SELECT * FROM hocalar"))
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
    
    def tum_ogrencileri_getir(self):
        try:
            result = self.connection.execute(text("SELECT * FROM ogrenciler"))
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
    
    def tum_dersleri_getir(self):
        try:
            sorgu = text("""
            SELECT d.*, h.isim as hoca_adi, h.soyisim as hoca_soyisim
            FROM dersler d
            LEFT JOIN hocalar_ders hd ON d.ders_id = hd.ders_id
            LEFT JOIN hocalar h ON hd.hoca_id = h.hoca_id
            """)
            result = self.connection.execute(sorgu)
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
    
    def hocanin_verdigi_dersler(self, hoca_id):
        try:
            sorgu = text("""
            SELECT d.ders_id, d.ders_adi 
            FROM dersler d
            JOIN hocalar_ders hd ON d.ders_id = hd.ders_id
            WHERE hd.hoca_id = :hoca_id
            """)
            result = self.connection.execute(sorgu, {"hoca_id": hoca_id})
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
    
    def ders_ekle(self, hoca_id, ders_adi):
        try:
            transaction = self.connection.begin()
            
            # Ders ekleme
            self.connection.execute(text("INSERT INTO dersler (ders_adi) VALUES (:ders_adi)"),
                                  {'ders_adi': ders_adi})
            
            # Yeni ders ID'sini al
            yeni_ders_id = self.connection.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            
            # Hoca-ders ilişkisini ekle
            self.connection.execute(text("INSERT INTO hocalar_ders (hoca_id, ders_id) VALUES (:hoca_id, :ders_id)"),
                                  {'hoca_id': hoca_id, 'ders_id': yeni_ders_id})
            
            transaction.commit()
            return {'status': True, 'message': 'Ders başarıyla eklendi', 'ders_id': yeni_ders_id}
        except SQLAlchemyError as err:
            transaction.rollback()
            print(f"Ders ekleme hatası: {err}")
            return {'status': False, 'message': 'Veritabanı hatası: ' + str(err)}
        except Exception as e:
            transaction.rollback()
            print(f"Beklenmeyen hata: {e}")
            return {'status': False, 'message': 'Beklenmeyen hata oluştu'}

    def ogrencinin_aldigi_dersler(self, ogr_id):
        try:
            sorgu = text("""
            SELECT d.ders_id, d.ders_adi,
                   h.isim as hoca_adi,
                   h.soyisim as hoca_soyisim
            FROM dersler d
            JOIN ogrenciler_ders od ON d.ders_id = od.ders_id
            LEFT JOIN hocalar_ders hd ON d.ders_id = hd.ders_id
            LEFT JOIN hocalar h ON hd.hoca_id = h.hoca_id
            WHERE od.ogr_id = :ogr_id
            """)
            result = self.connection.execute(sorgu, {"ogr_id": ogr_id})
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []

    def ders_sec(self, ogr_id, ders_id):
        try:
            transaction = self.connection.begin()
            
            # Öğrencinin mevcut ders sayısını kontrol et
            mevcut_ders_sayisi = self.connection.execute(
                text("SELECT COUNT(*) FROM ogrenciler_ders WHERE ogr_id=:o"),
                {"o": ogr_id}
            ).scalar()
            
            if mevcut_ders_sayisi >= 8:
                return {'status': False, 'message': 'En fazla 8 ders seçebilirsiniz'}
            
            # Daha önce kayıt kontrolü
            kontrol = self.connection.execute(
                text("SELECT * FROM ogrenciler_ders WHERE ogr_id=:o AND ders_id=:d"),
                {"o": ogr_id, "d": ders_id}
            ).fetchone()
            
            if kontrol:
                return {'status': False, 'message': 'Bu derse zaten kayıtlısınız'}
            
            # Dersin kontenjan kontrolü
            ders_kontrol = self.connection.execute(
                text("""
                SELECT d.*, COUNT(od.ogr_id) as ogrenci_sayisi 
                FROM dersler d 
                LEFT JOIN ogrenciler_ders od ON d.ders_id = od.ders_id 
                WHERE d.ders_id = :d 
                GROUP BY d.ders_id
                """),
                {"d": ders_id}
            ).mappings().first()
            
            if ders_kontrol and ders_kontrol['ogrenci_sayisi'] >= 20:
                return {'status': False, 'message': 'Bu dersin kontenjanı dolmuştur'}
            
            # Dersin mevcut hocasını bul
            hoca_sorgu = text("""
                SELECT h.hoca_id, h.isim, h.soyisim
                FROM hocalar h
                JOIN hocalar_ders hd ON h.hoca_id = hd.hoca_id
                WHERE hd.ders_id = :ders_id
            """)
            hoca = self.connection.execute(hoca_sorgu, {"ders_id": ders_id}).mappings().first()
            
            # Öğrenci-ders kaydını yap ve hoca bilgisini sakla
            if hoca:
                self.connection.execute(
                    text("INSERT INTO ogrenciler_ders (ogr_id, ders_id, hoca_id, hoca_adi, hoca_soyisim) VALUES (:o, :d, :h_id, :h_ad, :h_soyad)"),
                    {"o": ogr_id, "d": ders_id, "h_id": hoca['hoca_id'], "h_ad": hoca['isim'], "h_soyad": hoca['soyisim']}
                )
            else:
                self.connection.execute(
                    text("INSERT INTO ogrenciler_ders (ogr_id, ders_id) VALUES (:o, :d)"),
                    {"o": ogr_id, "d": ders_id}
                )
            
            transaction.commit()
            return {'status': True, 'message': 'Ders seçimi başarılı'}
        except SQLAlchemyError as err:
            transaction.rollback()
            print(f"Ders seçme hatası: {err}")
            return {'status': False, 'message': 'Veritabanı hatası: ' + str(err)}

    def ders_geri_al(self, ogr_id, ders_id):
        try:
            transaction = self.connection.begin()
            
            # Ders ve öğrenci bilgilerini kontrol et
            kayit_kontrol = self.connection.execute(
                text("""
                SELECT od.*, d.ders_adi, o.isim as ogr_adi, o.ogr_soyisim
                FROM ogrenciler_ders od
                JOIN dersler d ON od.ders_id = d.ders_id
                JOIN ogrenciler o ON od.ogr_id = o.ogr_id
                WHERE od.ogr_id=:o AND od.ders_id=:d
                """),
                {"o": ogr_id, "d": ders_id}
            ).mappings().first()
            
            if not kayit_kontrol:
                return {'status': False, 'message': 'Ders kaydı bulunamadı'}
            
            # Öğrencinin toplam ders sayısını kontrol et
            ders_sayisi = self.connection.execute(
                text("SELECT COUNT(*) FROM ogrenciler_ders WHERE ogr_id=:o"),
                {"o": ogr_id}
            ).scalar()
            
            if ders_sayisi <= 1:
                return {'status': False, 'message': 'En az bir ders almak zorundasınız'}
            
            # Dersi bırak
            result = self.connection.execute(
                text("DELETE FROM ogrenciler_ders WHERE ogr_id=:o AND ders_id=:d"),
                {"o": ogr_id, "d": ders_id}
            )
            
            if result.rowcount == 0:
                return {'status': False, 'message': 'Ders kaydı silinemedi'}
            
            transaction.commit()
            return {
                'status': True,
                'message': f'{kayit_kontrol["ders_adi"]} dersi başarıyla bırakıldı',
                'ders_adi': kayit_kontrol['ders_adi'],
                'kalan_ders_sayisi': ders_sayisi - 1
            }
        except SQLAlchemyError as err:
            transaction.rollback()
            print(f"Ders geri alma hatası: {err}")
            return {'status': False, 'message': 'Veritabanı hatası: ' + str(err)}

    def ders_getir(self, ders_id):
        try:
            sorgu = text("SELECT * FROM dersler WHERE ders_id = :ders_id")
            result = self.connection.execute(sorgu, {"ders_id": ders_id})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Ders sorgulama hatası: {err}")
            return None

    def hoca_getir(self, hoca_id):
        try:
            sorgu = text("SELECT * FROM hocalar WHERE hoca_id = :hoca_id")
            result = self.connection.execute(sorgu, {"hoca_id": hoca_id})
            row = result.mappings().first()
            return dict(row) if row else None
        except SQLAlchemyError as err:
            print(f"Hoca sorgulama hatası: {err}")
            return None
                

    
    def dersi_alan_ogrenciler(self, ders_id, hoca_id):
        try:
            sorgu = text("""
            SELECT o.ogr_no, o.isim, o.ogr_soyisim, o.ogr_email
            FROM ogrenciler o
            JOIN ogrenciler_ders od ON o.ogr_id = od.ogr_id
            JOIN hocalar_ders hd ON od.ders_id = hd.ders_id AND hd.hoca_id = :hoca_id
            WHERE od.ders_id = :ders_id
            """)
            result = self.connection.execute(sorgu, {"ders_id": ders_id, "hoca_id": hoca_id})
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
    
    def dersi_veren_hoca(self, ders_id):
        try:
            sorgu = text("""
            SELECT h.hoca_id, h.isim, h.soyisim, h.email
            FROM hocalar h
            JOIN hocalar_ders hd ON h.hoca_id = hd.hoca_id
            WHERE hd.ders_id = :ders_id
            """)
            result = self.connection.execute(sorgu, {"ders_id": ders_id})
            rows = result.mappings().fetchall()
            return [dict(row) for row in rows]
        except SQLAlchemyError as err:
            print(f"Sorgu hatası: {err}")
            return []
            
    def ders_sil(self, hoca_id, ders_id):
        try:
            transaction = self.connection.begin()
            
            # Önce öğrenci-ders ilişkilerini sil
            self.connection.execute(
                text("DELETE FROM ogrenciler_ders WHERE ders_id = :ders_id"),
                {"ders_id": ders_id}
            )
            
            # Sonra hoca-ders ilişkisini sil
            result = self.connection.execute(
                text("DELETE FROM hocalar_ders WHERE hoca_id = :hoca_id AND ders_id = :ders_id"),
                {"hoca_id": hoca_id, "ders_id": ders_id}
            )
            
            if result.rowcount == 0:
                transaction.rollback()
                return {"status": False, "message": "Ders bulunamadı"}
            
            # En son dersi sil
            self.connection.execute(
                text("DELETE FROM dersler WHERE ders_id = :ders_id"),
                {"ders_id": ders_id}
            )
            
            transaction.commit()
            return {"status": True, "message": "Ders başarıyla silindi"}
        except SQLAlchemyError as err:
            transaction.rollback()
            print(f"Ders silme hatası: {err}")
            return {"status": False, "message": "Veritabanı hatası: " + str(err)}
        except Exception as e:
            transaction.rollback()
            print(f"Beklenmeyen hata: {e}")
            return {"status": False, "message": "Beklenmeyen hata oluştu"}

def main():
    db = VeritabaniErisim()

    if not db.baglan():
        print("Program sonlandırılıyor...")
        sys.exit(1)

    logged_in = False
    user_type = None
    user_info = None

    while not logged_in:
        print("\n--- Giriş Yap ---")
        print("1. Admin Girişi")
        print("2. Hoca Girişi")
        print("3. Öğrenci Girişi")
        print("0. Çıkış")
        secim = input("Seçiminiz (0-3): ")

        if secim == "0":
            print("Çıkış yapılıyor...")
            sys.exit()
        elif secim == "1":
            email = input("Email: ")
            sifre = getpass.getpass("Şifre: ")
            user_info = db.admin_giris_dogrula(email, sifre)
            if user_info:
                logged_in = True
                user_type = "admin"
            else:
                print("Giriş başarısız. Lütfen tekrar deneyin.")
        elif secim == "2":
            email = input("Email: ")
            sifre = getpass.getpass("Şifre: ")
            user_info = db.hoca_giris_dogrula(email, sifre)
            if user_info:
                logged_in = True
                user_type = "hoca"
            else:
                print("Giriş başarısız. Lütfen tekrar deneyin.")
        elif secim == "3":
            ogr_no = input("Öğrenci No: ")
            sifre = getpass.getpass("Şifre: ")
            user_info = db.ogrenci_giris_dogrula(ogr_no, sifre)
            if user_info:
                logged_in = True
                user_type = "öğrenci"
            else:
                print("Giriş başarısız. Lütfen tekrar deneyin.")
        else:
            print("Geçersiz seçim!")

    while True:
        print("\n--- PROJE Veritabanı Erişim Programı ---")
        print("1. Tüm hocaları listele")
        print("2. Tüm öğrencileri listele")
        print("3. Tüm dersleri listele")
        print("4. Bir hocanın verdiği dersleri listele")
        print("5. Bir öğrencinin aldığı dersleri listele")
        print("6. Bir dersi alan öğrencileri listele")
        print("7. Bir dersi veren hocayı göster")
        print("0. Çıkış")
        
        secim = input("\nSeçiminiz (0-7): ")
        
        if secim == "0":
            break
        elif secim == "1":
            hocalar = db.tum_hocalari_getir()
            print("\n--- Tüm Hocalar ---")
            for hoca in hocalar:
                print(f"ID: {hoca['hoca_id']}, {hoca['isim']} {hoca['soyisim']}, Email: {hoca['email']}")
        elif secim == "2":
            ogrenciler = db.tum_ogrencileri_getir()
            print("\n--- Tüm Öğrenciler ---")
            for ogrenci in ogrenciler:
                print(f"ID: {ogrenci['ogr_id']}, {ogrenci['ogr_isim']} {ogrenci['ogr_soyisim']}, Email: {ogrenci['ogr_email']}")
        elif secim == "3":
            dersler = db.tum_dersleri_getir()
            print("\n--- Tüm Dersler ---")
            for ders in dersler:
                print(f"ID: {ders['ders_id']}, Ders Adı: {ders['ders_adi']}")
        elif secim == "4":
            hoca_id = input("Hoca ID'sini girin: ")
            dersler = db.hocanin_verdigi_dersler(hoca_id)
            print(f"\n--- Hoca ID: {hoca_id} için Dersler ---")
            if dersler:
                for ders in dersler:
                    print(f"Ders ID: {ders['ders_id']}, Ders Adı: {ders['ders_adi']}")
            else:
                print("Bu hoca için ders bulunamadı veya hoca ID'si geçersiz.")
        elif secim == "5":
            ogr_id = input("Öğrenci ID'sini girin: ")
            dersler = db.ogrencinin_aldigi_dersler(ogr_id)
            print(f"\n--- Öğrenci ID: {ogr_id} için Dersler ---")
            if dersler:
                for ders in dersler:
                    print(f"Ders ID: {ders['ders_id']}, Ders Adı: {ders['ders_adi']}")
            else:
                print("Bu öğrenci için ders bulunamadı veya öğrenci ID'si geçersiz.")
        elif secim == "6":
            ders_id = input("Ders ID'sini girin: ")
            hoca_id = input("Hoca ID'sini girin: ")
            ogrenciler = db.dersi_alan_ogrenciler(ders_id, hoca_id)
            print(f"\n--- Ders ID: {ders_id} için Öğrenciler ---")
            if ogrenciler:
                for ogrenci in ogrenciler:
                    print(f"Öğrenci ID: {ogrenci['ogr_id']}, {ogrenci['ogr_isim']} {ogrenci['ogr_soyisim']}, Email: {ogrenci['ogr_email']}")
            else:
                print("Bu ders için öğrenci bulunamadı veya ders ID'si geçersiz.")
        elif secim == "7":
            ders_id = input("Ders ID'sini girin: ")
            hoca_id = input("Hoca ID'sini girin: ")
            hocalar = db.dersi_veren_hoca(ders_id)
            print(f"\n--- Ders ID: {ders_id} için Hocalar ---")
            if hocalar:
                for hoca in hocalar:
                    print(f"Hoca ID: {hoca['hoca_id']}, {hoca['isim']} {hoca['soyisim']}, Email: {hoca['email']}")
            else:
                print("Bu ders için hoca bulunamadı veya ders ID'si geçersiz.")
        else:
            print("Geçersiz seçim! Lütfen 0-7 arasında bir değer girin.")

    db.baglanti_kapat()
    print("Program sonlandırıldı.")

if __name__ == "__main__":
    main()