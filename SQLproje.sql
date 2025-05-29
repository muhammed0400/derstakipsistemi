-- Veritabanı ve karakter seti
CREATE DATABASE IF NOT EXISTS PROJE
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
USE PROJE;

CREATE TABLE admin (
  ad_id     INT PRIMARY KEY AUTO_INCREMENT,  -- Otomatik artan benzersiz ID
  ad_mail   VARCHAR(100) NOT NULL UNIQUE,    -- Mail adresi (benzersiz ve boş olamaz)
  ad_sifre  VARCHAR(100) NOT NULL            -- Şifre (boş olamaz)
);
INSERT INTO admin (ad_mail, ad_sifre) VALUES
('admin1@gmail.edu.tr', '1234'),
('admin2@gmail.edu.tr', '5678');



-- Tablolar
CREATE TABLE hocalar(
  hoca_id    INT PRIMARY KEY AUTO_INCREMENT,
  isim       VARCHAR(100),
  soyisim    VARCHAR(100),
  email      VARCHAR(100) UNIQUE NOT NULL,
  sifre      VARCHAR(64) NOT NULL
);

CREATE TABLE ogrenciler (
   ogr_id      INT PRIMARY KEY AUTO_INCREMENT,
   ogr_no      VARCHAR(20) UNIQUE NOT NULL,
   isim        VARCHAR(100) NOT NULL,
   sifre       VARCHAR(64) NOT NULL,
   ogr_soyisim VARCHAR(100),
   ogr_email   VARCHAR(155) UNIQUE
);


CREATE TABLE dersler (
  ders_id    INT PRIMARY KEY AUTO_INCREMENT,
  ders_adi   VARCHAR(100)
);

-- İlişki Tabloları
CREATE TABLE ogrenciler_ders(
  ogr_id  INT,
  ders_id INT,
  FOREIGN KEY (ogr_id) REFERENCES ogrenciler(ogr_id),
  FOREIGN KEY (ders_id) REFERENCES dersler(ders_id)
);

CREATE TABLE hocalar_ders(
  hoca_id INT,
  ders_id INT,
  FOREIGN KEY (hoca_id) REFERENCES hocalar(hoca_id),
  FOREIGN KEY (ders_id) REFERENCES dersler(ders_id)
);

-- Veri Ekleme
INSERT INTO hocalar (isim, soyisim, email, sifre) VALUES
('Ahmet', 'Yılmaz', 'ahmet.yilmaz@ceng.edu.tr', 1234),
('Zeynep', 'Arslan', 'zeynep.arslan@ceng.edu.tr', 2345),
('Kerem', 'Kara', 'kerem.kara@ceng.edu.tr', 3456),
('Selin', 'Demir', 'selin.demir@ceng.edu.tr', 4567),
('Can', 'Tekin', 'can.tekin@ceng.edu.tr', 5678);

INSERT INTO dersler (ders_adi) VALUES
('Veri Tabanı Sistemleri'),
('İşletim Sistemleri'),
('Yazılım Mühendisliği'),
('Bilgisayar Ağları'),
('Web Programlama'),
('Makine Öğrenmesi'),
('Dağıtık Sistemler'),
('İnsan Bilgisayar Etkileşimi'),
('Siber Güvenlik Temelleri'),
('Mobil Uygulama Geliştirme');

INSERT INTO ogrenciler (ogr_no, isim, ogr_soyisim, ogr_email, sifre) VALUES
('1001', 'Ali', 'Kaya', 'ali.kaya@stu.edu.tr', 1111),
('1002', 'Ayşe', 'Demir', 'ayse.demir@stu.edu.tr', 2222),
('1003', 'Mehmet', 'Çelik', 'mehmet.celik@stu.edu.tr', 3333),
('1004', 'Zeynep', 'Yıldız', 'zeynep.yildiz@stu.edu.tr', 4444),
('1005', 'Can', 'Arslan', 'can.arslan@stu.edu.tr', 5555),
('1006', 'Elif', 'Korkmaz', 'elif.korkmaz@stu.edu.tr', 6666),
('1007', 'Burak', 'Öztürk', 'burak.ozturk@stu.edu.tr', 7777),
('1008', 'Seda', 'Şahin', 'seda.sahin@stu.edu.tr', 8888),
('1009', 'Emre', 'Aksoy', 'emre.aksoy@stu.edu.tr', 9999),
('1010', 'Deniz', 'Koç', 'deniz.koc@stu.edu.tr', 1122),
('1011', 'Ahmet', 'Kurt', 'ahmet.kurt@stu.edu.tr', 1234),
('1012', 'Merve', 'Yıldırım', 'merve.yildirim@stu.edu.tr', 2345),
('1013', 'Cem', 'Şahin', 'cem.sahin@stu.edu.tr', 3456),
('1014', 'Selin', 'Korkmaz', 'selin.korkmaz@stu.edu.tr', 4567),
('1015', 'Berk', 'Aydın', 'berk.aydin@stu.edu.tr', 5678),
('1016', 'Ece', 'Taş', 'ece.tas@stu.edu.tr', 6789),
('1017', 'Kaan', 'Güneş', 'kaan.gunes@stu.edu.tr', 7890),
('1018', 'Deniz', 'Bulut', 'deniz.bulut@stu.edu.tr', 8901),
('1019', 'Zeynep', 'Toprak', 'zeynep.toprak@stu.edu.tr', 9012),
('1020', 'Arda', 'Yılmaz', 'arda.yilmaz@stu.edu.tr', 1122),
('1021', 'İrem', 'Çetin', 'irem.cetin@stu.edu.tr', 2233),
('1022', 'Emir', 'Koç', 'emir.koc@stu.edu.tr', 3344),
('1023', 'Defne', 'Aksoy', 'defne.aksoy@stu.edu.tr', 4455),
('1024', 'Tolga', 'Demir', 'tolga.demir@stu.edu.tr', 5566),
('1025', 'Gizem', 'Kara', 'gizem.kara@stu.edu.tr', 6677);



INSERT INTO hocalar_ders (hoca_id, ders_id) VALUES
(1,1),
(2,2), (2,7),
(3,4), (3,9),
(4,5), (4,10),
(5,3), (5,6);

-- Öğrenci-Ders Rastgele Atama Prosedürü
DELIMITER $$
CREATE PROCEDURE RastgeleDersAta()
BEGIN
  DECLARE ogr_no INT DEFAULT 1;
  DECLARE ders_sayisi INT;
  
  WHILE ogr_no <= 25 DO
    SET ders_sayisi = FLOOR(3 + RAND() * 3); -- 3-5 rastgele ders
    
    INSERT INTO ogrenciler_ders (ogr_id, ders_id)
    SELECT ogr_no, ders_id 
    FROM dersler 
    ORDER BY RAND() 
    LIMIT ders_sayisi;
    
    SET ogr_no = ogr_no + 1;
  END WHILE;
END$$
DELIMITER ;

-- Prosedürü Çalıştırma
CALL RastgeleDersAta();



select * from dersler;


