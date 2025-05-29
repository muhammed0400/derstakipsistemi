# SQLAlchemy Entegrasyonu

## Proje Açıklaması

Bu projede, MySQL veritabanı erişimi için MySQL Connector yerine SQLAlchemy kütüphanesi kullanılmaya başlanmıştır. Bu değişiklik, veritabanı işlemlerini daha modern ve esnek bir şekilde gerçekleştirmeyi sağlar.

## Yapılan Değişiklikler

- `mysql.connector` yerine `sqlalchemy` ve `pymysql` kütüphaneleri kullanıldı
- Veritabanı bağlantısı için SQLAlchemy engine ve connection nesneleri kullanıldı
- SQL sorguları için `text()` fonksiyonu kullanılarak parametreli sorgular oluşturuldu
- Sorgu parametreleri `%s` yerine `:param_name` formatında kullanıldı
- Sorgu sonuçları için daha tutarlı bir dönüş formatı sağlandı

## Kurulum

Projeyi çalıştırmak için aşağıdaki kütüphanelerin yüklenmesi gerekmektedir:

```
pip install sqlalchemy pymysql
```

veya

```
python -m pip install sqlalchemy pymysql
```

## Olası Hatalar ve Çözümleri

### ModuleNotFoundError: No module named 'sqlalchemy'

Bu hata, SQLAlchemy kütüphanesinin yüklü olmadığını gösterir. Yukarıdaki kurulum komutlarını kullanarak kütüphaneleri yükleyin.

### ModuleNotFoundError: No module named 'pymysql'

Bu hata, PyMySQL kütüphanesinin yüklü olmadığını gösterir. Yukarıdaki kurulum komutlarını kullanarak kütüphaneleri yükleyin.

### OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'localhost'")

Bu hata, MySQL sunucusunun çalışmadığını veya bağlantı bilgilerinin yanlış olduğunu gösterir. MySQL sunucusunun çalıştığından ve bağlantı bilgilerinin doğru olduğundan emin olun.

## Kullanım

Program, önceki sürümle aynı şekilde çalışmaktadır. Menü seçenekleri ve işlevsellik değişmemiştir. Sadece arka planda çalışan veritabanı erişim kodu güncellenmiştir.

```
python veritabani_erisim.py
```

komutu ile programı çalıştırabilirsiniz.