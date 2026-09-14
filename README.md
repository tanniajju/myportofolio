# Personal Portfolio
Nama : Tania Ju

NPM : 2506608123

Kelas : PBP A

## Section
* **Hero section:** Berisi informasi berupa data diri saya untuk portofolio
* **Experience:** Berisi pengalaman organisasi saya selama berkuliah di Fasilkom UI

## Fitur Utama
*   **Semantic HTML Structure:** Menggunakan tag semantik HTML5 (`<section>`, `<nav>`, `<article>`) untuk aksesibilitas dan SEO yang optimal.
*   **Fully Responsive Grid:** Tata letak beradaptasi secara dinamis dari desktop (2 kolom) menjadi mobile (1 kolom) menggunakan CSS Grid dan Media Queries.
*   **Interactive UI/UX:** Animasi *hover* kustom pada kartu pengalaman dan piringan *spin* pada foto profil, lengkap dengan penanganan *sticky hover bug* untuk perangkat layar sentuh.

## Logbook Progres Mingguan

| Minggu | Tanggal | Progress / Fitur yang Dikerjakan | Kendala & Solusi Teknis |
| :---: | :--- | :--- | :--- |
| **1** | 24 - 28 Aug 2026 | Setup Git repository, Django Installation | - |
| **2** | 31 - 04 Sep 2026 | Setup HTML kerangka dasar dan penyusunan section *Hero* | Localhost sempat tidak merespons perubahan pada *style.css*. Solusi: melakukan reset server/koneksi hingga terupdate|
| **3** | 07 Sep 2026 | Penyusunan section *Experience* | Penggunaan layout carousel horizontal untuk section *Experience* menyebabkan perbedaan tinggi tiap *card*. Solusi: Menerapkan layout grid. |
---

# Tugas 1
**1. Penggunaan Elemen Semantik HTML5**

Saya secara aktif menggunakan elemen semantik HTML5 seperti `<section>` untuk membungkus area *Experience* dan `<nav>` untuk bilah navigasi. Secara visual tidak ada perbedaan dengan menggunakan `<div>` biasa, hanya saja secara teknis, ini mempermudah *maintainability* kode saat proyek bertambah besar dan mengoptimalkan *Screen Reader* untuk aksesibilitas.Ini mempermudah mesin pencari (SEO) dapat mengindeks hierarki informasi portofolio saya dengan akurat.

**2. Tantangan Struktur HTML dan Styling CSS**

Tantangan terbesar bagi saya adalah merapikan bagian section/div itu sendiri, bagaimana menentukan dan membagi suatu div sehingga dapat diatur dengan tepat. Saya merasa perlu lebih banyak pengalaman dan waktu berlatih untuk dapat memisahkan dan kemudian menaruh suatu styling di div yang tepat. Misalnya untuk bagian *Experience*, menjadi suatu tantangan bagi saya untuk mengatur efek ketika di-*hover* dan menyesuaikan isi kartu.

**3. Batasan Static Web & Rencana Fungsionalitas Dinamis**
Batasan paling terasa dari *static web* murni adalah tingginya redudansi pengeditan manual. Setiap ada penambahan pengalaman kepanitiaan baru, saya harus mengubah file HTML dan memastikan tag penutupnya tidak merusak struktur. Untuk iterasi proyek selanjutnya, fungsionalitas dinamis yang paling ingin saya siapkan adalah pemisahan data. Saya mungkin akan memikirkan untuk menggunakan file JSON atau menggunakan fitur lainnya (mungkin mempelajari backend atau menggunakan database juga).


**AI Disclosure & Manual Refinement**

Dalam pengerjaan proyek myportofolio (Tugas 1), sejauh ini saya memanfaatkan *Generative AI* sebagai pendiskusi teknis. Saya tetap melakukan intervensi teknis dan keputusan secara manual:

1.  **Logika CSS:** AI saya gunakan untuk membantu memahami lebih lanjut fungsi dari suatu styling di CSS, misalnya "apakah cukup dengan `grid-template-columns: repeat(2, 1fr);` dapat memastikan setiap konten tambahan turun ke bawah, bagaimana logika urutan dan ui jika user melakukan klik pada salah satu card?"
2.  **Penanganan Bug** AI membantu saya dalam melakukan debugging, misalnya ketika card *Experience* yang seharusnya hanya muncul 2 dalam 1 row tiba-tiba menjadi 4 card sangat kecil dalam 1 row, saya meminta bantuan AI untuk mengecek apa yang salah (ternyata div yang terduplikat).

---

# Tugas 2
**1. Alur Permintaan pada Halaman Portofolio**
* Pengguna mengakses URL halaman portofolio baru (misalnya `/skill`).
* `urls.py` proyek: Permintaan HTTP dari *browser* pertama kali masuk ke berkas rute utama proyek. Berkas ini bertugas memeriksa awalan URL dan meneruskannya ke `urls.py` tingkat aplikasi menggunakan fungsi `include()`.
* `urls.py`aplikasi: Berkas URL tingkat aplikasi mencocokkan sisa path URL (misalnya `skill/`) dengan daftar rute yang tersedia.
* `views.py`: Bertindak sebagai jembatan logika yang memanggil model untuk mengambil data, menyiapkan *context*, dan memanggil fungsi `render()`.
* `models.py`: Menyediakan representasi struktur data (misalnya `Skill`). Melalui Django ORM, perintah kueri (seperti `Skill.objects.all()`) dijalankan untuk mengambil data terkait yang tersimpan lalu dikembalikan ke *view*.
* `templates/`: Menerima data *context* dari *view*. Mesin Django Template Language (DTL) memproses logika tampilan dokumen HTML statis yang utuh.
* Pengiriman Respons ke Browser: Menerima berkas HTML yang telah selesai disusun beserta aset statisnya (CSS dan gambar) sebagai HTTP *response* (status kode 200 OK) untuk dirender menjadi antarmuka visual user.

**2. Urgensi Penyimpanan Data pada Model dan Dampaknya**
Menyimpan data portofolio di dalam model basis data dibandingkan *hard-coded* memberi beberapa keuntungan:
* ***Separation of Concerns*:**
  Mengikuti prinsip arsitektur perangkat lunak yang baik, struktur presentasi antarmuka (HTML/CSS) dipisahkan secara dari lapisan data, dengan demikian tidak terjadi pengulangan kode untuk deklarasi data juga.
* ***Maintainability*:**
  Jika terjadi pembaruan informasi, *developer* tidak perlu mengubah kode tampilan di file HTML, *recommit*, atau *redeploy*. Data dapat dikelola secara aman melalui admin page atau antarmuka database.
* ***Scalability & Extensibility*:**
  Data yang tersimpan di basis data bersifat dinamis dan dapat dimanipulasi dengan mudah. Kita dapat melakukan *sorting*, *filtering*, *search*, atau *grouping*. Selain itu, jika di kemudian hari ingin dibuatkan API untuk aplikasi mobile, data model yang sama dapat langsung diserialisasi ke format JSON tanpa menulis ulang informasi.


**3. Perbedaan `makemigrations` dan `migrate` serta Contoh Kasusnya**

Kedua perintah ini merupakan bagian dari sistem migrasi Django untuk menyinkronkan definisi model di kode Python dengan skema tabel di database:

* **`python manage.py makemigrations`:**
  Berfungsi untuk **merekam dan mendeteksi perubahan** yang dilakukan pada berkas `models.py`. Perintah ini tidak mengubah tabel di dalam database secara langsung, melainkan membuat berkas migrasi baru (`migrations/`, misal `0002_skill.py`) yang berisi instruksi perubahan skema dalam bentuk deklaratif.
* **`python manage.py migrate`:**
  Berfungsi untuk **mengeksekusi instruksi** yang tercatat di dalam berkas-berkas migrasi ke sistem manajemen database aktual. Perintah ini secara nyata membuat tabel, menambahkan kolom, memperbarui tipe data, atau menghapus batasan di database.

#### Contoh Perubahan Model yang Mengharuskan Menjalankan Kedua Perintah:
Ketika saya menambahkan model baru `Skill`, ini memerlukan kedua perintah karena terdapat perubahan yang berpengaruh langsung ke database.

Sementara perubahan method, opsi choices (tanpa mengubah panjang maksimal), dan opsi validasi form admin tidak perlu menjalankan perintah tersebut karena hanya perubahan di skema model.

**AI Disclosure & Manual Refinement**

Dalam pengerjaan proyek myportofolio (Tugas 2), sejauh ini saya memanfaatkan *Generative AI* sebagai pendiskusi teknis. Saya tetap melakukan intervensi teknis dan keputusan secara manual:

1.  **Styling & Layout:** AI saya gunakan untuk membantu memahami lebih lanjut fungsi dari suatu styling di CSS, misalnya "struktur seperti apa yang sebaiknya digunakan untuk membuat 3 kolom terpisah skill seperti section di notion".
2.  **Iterative Debugging:** AI membantu saya dalam melakukan debugging, dengan log error spesifik seperti kegagalan assertion pada test case, untuk memahami akar masalah dan memperbaiki dengan tepat.
3. **Refaktorisasi Templating**: Saran penerapan {% %} untuk memecah kolom kategori secara dinamis dan menampilkan display kategori sebagai header tanpa hard-code HTML.