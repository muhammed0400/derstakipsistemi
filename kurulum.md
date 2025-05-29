# SQLAlchemy ve PyMySQL Kurulumu

Bu projeyi çalıştırmak için aşağıdaki kütüphanelerin yüklenmesi gerekmektedir:

```
pip install sqlalchemy pymysql
```

veya

```
python -m pip install sqlalchemy pymysql
```

komutlarını kullanarak gerekli kütüphaneleri yükleyebilirsiniz.

## Proje Hakkında

Bu proje, MySQL veritabanı erişimini SQLAlchemy kütüphanesi kullanarak gerçekleştirmektedir. Önceki MySQL Connector yaklaşımı yerine daha modern ve esnek bir ORM (Object-Relational Mapping) çözümü sunmaktadır.

## Değişiklikler

- MySQL Connector yerine SQLAlchemy kullanılmaya başlandı
- Sorgu parametreleri için daha güvenli bir yaklaşım (:param şeklinde) kullanıldı
- Veritabanı bağlantı yönetimi geliştirildi
- Sorgu sonuçları için daha tutarlı bir dönüş formatı sağlandı