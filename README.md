# MySQL Veritabanı Erişim Programı

Bu program, MySQL veritabanınızdaki verilere erişmenizi sağlayan basit bir Python scriptidir. PROJE veritabanındaki hocalar, öğrenciler ve dersler tablolarındaki verileri görüntüleyebilir ve aralarındaki ilişkileri sorgulayabilirsiniz.

## Gereksinimler

Programı çalıştırmak için aşağıdaki gereksinimlere ihtiyacınız vardır:

1. Python 3.x
2. MySQL veritabanı
3. MySQL Connector/Python kütüphanesi

## Kurulum

1. MySQL Connector/Python kütüphanesini yükleyin:

```
pip install mysql-connector-python
```

2. MySQL veritabanınızda `MYsql.sql` dosyasındaki SQL komutlarını çalıştırarak gerekli tabloları ve verileri oluşturun.

## Kullanım

Programı çalıştırmak için:

```
python veritabani_erisim.py
```

Program çalıştığında:

1. MySQL veritabanı şifrenizi girmeniz istenecektir.
2. Başarılı bağlantı sonrası, aşağıdaki işlemleri yapabilirsiniz:
   - Tüm hocaları listeleme
   - Tüm öğrencileri listeleme
   - Tüm dersleri listeleme
   - Bir hocanın verdiği dersleri listeleme
   - Bir öğrencinin aldığı dersleri listeleme
   - Bir dersi alan öğrencileri listeleme
   - Bir dersi veren hocayı görüntüleme

## Fonksiyonlar

Program aşağıdaki veritabanı işlemlerini gerçekleştirebilir:

- `tum_hocalari_getir()`: Tüm hocaların bilgilerini getirir
- `tum_ogrencileri_getir()`: Tüm öğrencilerin bilgilerini getirir
- `tum_dersleri_getir()`: Tüm derslerin bilgilerini getirir
- `hocanin_verdigi_dersler(hoca_id)`: Belirli bir hocanın verdiği dersleri getirir
- `ogrencinin_aldigi_dersler(ogr_id)`: Belirli bir öğrencinin aldığı dersleri getirir
- `dersi_alan_ogrenciler(ders_id)`: Belirli bir dersi alan öğrencileri getirir
- `dersi_veren_hoca(ders_id)`: Belirli bir dersi veren hocayı getirir

## Notlar

- Program, MySQL veritabanına bağlanmak için kullanıcı adı olarak varsayılan olarak 'root' kullanır. Farklı bir kullanıcı adı kullanmak isterseniz, kodu düzenleyebilirsiniz.
- Veritabanı adı olarak 'PROJE' kullanılmaktadır. Farklı bir veritabanı adı kullanmak isterseniz, kodu düzenleyebilirsiniz.