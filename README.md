# Personal Portfolio
Nama : Tania Ju

NPM : 2506608123

Kelas : PBP A

## Panduan Instalasi
### 1. Clone Repositori & Persiapan env
```bash
# Clone repositori ini
git clone <https://github.com/tanniajju/myportofolio.git>
cd myportofolio

# Buat virtual environment
python -m venv env

# Aktifkan virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

### 2. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 3. Migrasi Database & Menjalankan Pengujian
```bash
# Jalankan migrasi basis data
python manage.py migrate

# Jalankan seluruh unit test untuk memastikan fungsionalitas berjalan normal
python manage.py test main
```

### 4. Menjalankan Server Pengembangan
```bash
python manage.py runserver
```
Buka peramban dan akses alamat http://localhost:8000/.

## Section
* **Hero section:** Berisi informasi berupa data diri saya untuk portofolio
* **Experience:** Berisi pengalaman organisasi saya selama berkuliah di Fasilkom UI
* **Skill:** Berisi keahlian (bahasa pemrograman, *framework*, dan *tool/platform*) yang saya pelajari sejauh ini

## Fitur Utama
*   **Semantic HTML Structure:** Menggunakan tag semantik HTML5 (`<section>`, `<nav>`, `<article>`) untuk aksesibilitas dan SEO yang optimal.
*   **Fully Responsive Grid:** Tata letak beradaptasi secara dinamis dari desktop (2 kolom) menjadi mobile (1 kolom) menggunakan CSS Grid dan Media Queries.
*   **Interactive UI/UX:** Animasi *hover* kustom pada kartu pengalaman dan piringan *spin* pada foto profil, lengkap dengan penanganan *sticky hover bug* untuk perangkat layar sentuh.

## Logbook Progres Mingguan

| Minggu | Tanggal | Progress / Fitur yang Dikerjakan | Kendala & Solusi Teknis |
| :---: | :--- | :--- | :--- |
| **1** | 24 - 30 Aug 2026 | Setup Git repository, Django Installation | - |
| **2** | 31 Aug - 06 Sep 2026 | Setup HTML kerangka dasar dan penyusunan section *Hero* | Localhost sempat tidak merespons perubahan pada *style.css*. Solusi: melakukan reset server/koneksi hingga terupdate|
| **3** | 07 - 13 Sep 2026 | Penyusunan section *Experience* | Penggunaan layout carousel horizontal untuk section *Experience* menyebabkan perbedaan tinggi tiap *card*. Solusi: Menerapkan layout grid. |
| **4** | 14 - 18 Sep 2026 | Penyusunan section *Skill* dengan implementasi MVT, navigasi *footer*, unit testing *Skill* | - |
| **5** | 21 - 15 Sep 2026 | Penyusunan section *Skill, Experience, Project* dengan implementasi *Form & Data Delivery* | - |
| **6** | 28 Sep - 02 Okt 2026 | Penerapan Autentikasi, Session, dan Cookie | - |
| **7** | 05 Okt 2026 | Penerapan Web Interactivity with JavaScript | Terdapat 2 section yang dapat dikerjakan pada tugas 3 & 4, untuk pengerjaan tugas 5, saya memilih implementasinya di Experience |
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

# Tugas 3
**1. Alasan Menggunakan ModelForm dan *{% csrf_token %}***

Karena `ModelForm` mempermudah pembuatan form Django yang terhubung langsung dengan model database model. Sehingga Django secara otomatis membaca tipe data dari field model dan melakukan validasi input pengguna tanpa perlu menulis logika validasi dari awal. Selain itu, form dapat langsung disimpan ke database menggunakan metode .save() tanpa perlu memetakan satu per satu atribut secara manual. Selain itu, `ModelForm` juga mengurangi risiko kesalahan (human error) dalam penulisan nama atribut input HTML, serta mencegah* mass assignment vulnerability* dengan membatasi field apa saja yang boleh diisi melalui *parameter fields* atau *exclude*.

**Mengapa diwajibkan menambahkan *{% csrf_token %}* pada form?**

Tag *{% csrf_token %}* digunakan untuk melindungi aplikasi web dari serangan *CSRF (Cross-Site Request Forgery)*, yang terjadi jika  pihak ketiga atau situs berbahaya menipu peramban pengguna yang sedang login untuk mengirimkan *request* berbahaya (seperti mengubah data atau menghapus akun) tanpa sepengetahuan pengguna. Dengan adanya token CSRF yang digenerate secara unik untuk setiap sesi pengguna, Django dapat memverifikasi bahwa *request* POST yang masuk benar-benar berasal dari halaman web aplikasi kita, bukan dari situs luar.

**2. Mengapa JSON Lebih Disukai Dibandingkan XML dalam Pengembangan Web Modern?***

JSON lebih ringan dan efisien ukurannya (JSON menggunakan sintaks berbasis objek yang bersih dan minim *closing tags* yang menjadikan ukuran file JSON jauh lebih kecil), sehingga penggunaan bandwidth lebih hemat dan kecepatan transfer data via jaringan menjadi lebih cepat.

JSON juga memberi kemudahan *parsing* di sisi klien. Karena JSON pada dasarnya selaras dengan struktur objek JavaScript, browser dapat langsung membaca dan mengubah data JSON menjadi objek JavaScript dengan sangat cepat menggunakan `JSON.parse()`. Sebaliknya, XML memerlukan parser khusus (seperti DOM parser) yang lebih kompleks dan memakan sumber daya lebih besar.

Terakhir, struktur data JSON menggunakan pasangan *key-value* dan *array* yang sangat intuitif bagi pengembang modern untuk dibaca maupun diintegrasikan ke RESTful API.

**3. Alur Fungsi View Mengembalikan Data dalam Bentuk JSON & Alasan Serialization***

Alur saat fungsi view mengembalikan data portofolio dalam bentuk JSON:

* Pengguna mengirimkan *request* ke endpoint URL tertentu (misalnya */api/project*).
* Fungsi `view` di Django menerima request tersebut dan melakukan query ke *database* untuk mengambil data project.
* Data diterima dalam bentuk objek model Django (*QuerySet* atau *Model Instance*) yang tidak bisa dibaca langsung oleh protokol HTTP/JavaScript dalam format mentah.
* Data diubah ke fdalam format standar (JSON) melalui proses serialisasi.
* Fungsi view mengembalikan respons menggunakan modul khusus Django (seperti `JsonResponse` atau `HttpResponse` dengan *content type application/json*).

Oleh karena itu, serialisasi wajib dilakukan untuk menerjemahkan objek mentah Python/Django yang kompleks tersebut menjadi format teks standar (JSON) yang dapat dikirim melalui jaringan dan mudah dipahami oleh sistem atau frontend lain. Karena objek model Django adalah representasi objek Python bersarang yang kompleks dan terhubung langsung dengan mesin database (berisi metode, metadata, dan tipe data khusus Python), sementara protokol transmisi web seperti HTTP hanya dapat mengirimkan aliran data berupa teks mentah (seperti string JSON atau XML).

**AI Disclosure & Manual Refinement**

Dalam pengerjaan proyek myportofolio (Tugas 3), sejauh ini saya memanfaatkan *Generative AI* sebagai pendiskusi teknis. Saya tetap melakukan intervensi teknis dan keputusan secara manual:

1.  **Penyusunan Struktur Kode Awal (Boilerplate & CSS):** AI membantu menghasilkan kerangka dasar HTML, konfigurasi Carousel layout untuk halaman Experience, serta struktur dasar agar sesuai dengan standar konvensi Django.
2.  **Iterative Debugging:** AI membantu saya dalam melakukan debugging ketika terjadi kesalahan pada template rendering dan error testcase.
3. **Perumusan Konsep Logika**: AI memberikan rekomendasi penerapan properti Python seperti @property pada model untuk menentukan status aktif suatu pengalaman (`is_ongoing`) setelah perubahan `models.py`.

Meskipun membantu, AI memiliki beberapa keterbatasan nyata yang ditemukan selama proses pengembangan, seperti tidak konsistennya penamaan variabel, kurangnya penjelasan atau konteks mendalam/spesifik, dan *edge cases*. Untuk memastikan aplikasi tetap berjalan stabil, saya melakukan koreksi sintaks dan validasi model, penyempurnaan logika properti model, serta penyesuaian antarmuka dan styling css.

**Lampiran prompt:**
1. "Environment: Request Method: GET Request URL: http://localhost:8000/project ... [lampirkan traceback error TemplateDoesNotExist atau TypeError] ... Masih ada 2 error & failed, tolong bantu periksa celah yang menyebabkan masalah tersebut dan jelaskan dengan detail."
2. "Sepertinya logika pengecekan status selesai atau tidak masih salah deh, soalnya experience yg baru aku masukkan saja salah. Sepertinya karena ended_at tidak aku kosongin, sementara def is_ongoing(self): return self.ended_at is None. Tapi aku isi tanggal di masa depan, harusnya pengecekan logika mengcover hal ini, bagaimana mengecek untuk tipe data Datetime sekarang"
3. "Bagaimana struktur HTML dan CSS menggunakan tata letak grid yang tampilannya responsif, rapi, dan kartu-kartunya memiliki tinggi yang seragam""

# Tugas 4
Pada Tugas 4, diterapkan pola autentikasi dan otorisasi karena aplikasi portofolio memuat data yang merepresentasikan identitas dan karya pemiliknya, sehingga tidak boleh dapat diubah atau dihapus oleh sembarang orang. Autentikasi memastikan siapa yang sedang mengakses aplikasi, sedangkan otorisasi membatasi apa saja yang boleh dilakukan setelah identitas tersebut diketahui. Pembagian hak akses dilakukan berdasarkan peran dengan prinsip *least privilege*, yaitu setiap pengguna hanya memperoleh hak sesuai kebutuhannya. Dengan demikian, pemilik tetap memegang kendali penuh atas portofolionya, tetapi pengelolaan data menjadi lebih fleksibel dan aman.

### Ringkasan hak akses per peran

| Peran | Baca | Star / Unstar | Ubah | Buat | Hapus |
|---|---|---|---|---|---|
| Guest | ✔ | ✘ | ✘ | ✘ | ✘ |
| Logged in User | ✔ | ✔ | ✘ | ✘ | ✘ |
| Editor | ✔ | ✔ | ✔ | ✘ | ✘ |
| Pemilik (superuser) | ✔ | ✔ | ✔ | ✔ | ✔ |

**AI Disclosure & Manual Refinement**

Dalam pengerjaan proyek myportofolio (Tugas 4), sejauh ini saya memanfaatkan *Generative AI* sebagai pendiskusi teknis. Saya tetap melakukan intervensi teknis dan keputusan secara manual:

1.  **Faktorisasi fungsi untuk menyesuaikan struktur pemanggilan skill:** Karena bagian skill menggunakan pemanggilan grouping khusus, penambahan tombol star perlu disesuaikan dengan cara yang berbeda. Untuk itu, AI membantu menghasilkan kerangka konfigurasi untuk halaman Skill, serta struktur dasar agar sesuai dengan standar konvensi Django.
2.  **Iterative Debugging:** AI membantu saya dalam melakukan debugging ketika terjadi kesalahan pada template rendering dan error testcase.
3. **Membantu performatan Readme:** AI membantu saya dalam membuat format table readme (pembagian hak peran) secara cepat agar readme lebih readable

**Lampiran prompt:**
1. *pasted error code*, kenapa terjadi error demikian? Berikan opsi perbaikan terbaik dan penjelasannya
2. Bagaimana menerapkan fitur star pada section skill dengan tidak merusak struktur grouping dan filter untuk pencarian dan penampilan header berdasarkan kategori?
3. Berdasarkan *pasted penjelasan peran di perintah tugas*, buat struktur table untuk readme yang sederhana dan mudah dibaca.

# Tugas 5
**1. Apa itu debouncing dan mengapa penting diterapkan pada fitur pencarian AJAX**

Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan suatu aktivitas selama waktu tertentu. Pada fitur pencarian, debouncing digunakan agar request AJAX tidak dikirim setiap kali pengguna mengetik satu karakter.

Misalnya, ketika pengguna mengetik `portfolio`, tanpa debouncing dapat terjadi banyak request seperti:

- `p`
- `po`
- `por`
- `port`
- `portf`
- `portfo`
- `portfol`
- `portfoli`
- `portfolio`

Dengan debouncing, request hanya dikirim setelah pengguna berhenti mengetik selama waktu yang telah ditentukan.

Teknik ini penting karena dapat mengurangi jumlah request ke server, mengurangi beban server, dan membuat fitur pencarian menjadi lebih efisien serta responsif.

**2. Fungsi penggunaan 'await' ketika menggunakan 'fetch()**
`fetch()` digunakan untuk mengirim request HTTP dan mengambil data dari server. Karena proses tersebut berjalan secara asynchronous, `fetch()` menghasilkan sebuah `Promise`.

`await` digunakan untuk menunggu sampai `Promise` tersebut selesai sebelum program melanjutkan ke baris berikutnya. Dengan demikian, kita dapat memperoleh hasil response dari server dan kemudian memprosesnya.

Contohnya:

```js
const response = await fetch(endpoint);
const data = await response.json();
```

Pada kode tersebut, program menunggu sampai request selesai sebelum melanjutkan ke response.json().
Jika tidak menggunakan await, kita akan mendapatkan Promise, bukan hasil response secara langsung. Akibatnya, kita tidak dapat langsung menggunakan hasil tersebut sebagai response atau data yang dikirim oleh server.

**3. Serangan XSS (Cross-Site Scripting) dan alasan data AJAX/JavaScript lebih rentan**
XSS (Cross-Site Scripting) adalah serangan dengan cara menyisipkan kode JavaScript berbahaya ke dalam data yang kemudian ditampilkan atau dieksekusi oleh browser pengguna.

Data yang ditampilkan langsung melalui template Django relatif lebih aman karena Django secara otomatis melakukan HTML escaping pada nilai yang dirender melalui template. Contohnya, karakter seperti `<` dan `>` akan diubah sehingga tidak dianggap sebagai tag HTML atau kode yang dapat dieksekusi.

Sebaliknya, ketika data dari endpoint AJAX dimasukkan ke halaman menggunakan JavaScript, terutama melalui innerHTML, Django tidak melakukan escaping terhadap data tersebut. JavaScript memasukkan data langsung ke HTML sehingga data yang mengandung HTML atau JavaScript berbahaya dapat dieksekusi oleh browser.

Oleh karena itu, pada implementasi AJAX, setiap nilai teks yang dimasukkan ke HTML harus di-escape terlebih dahulu, misalnya menggunakan fungsi `escapeHtml()`, atau menggunakan `textContent` ketika memungkinkan. Selain itu, input teks juga dibersihkan di sisi server menggunakan `strip_tags` pada ModelForm sebagai lapisan perlindungan tambahan.

**AI Disclosure & Manual Refinement**

Dalam pengerjaan proyek `myportofolio` (Tugas 5), saya menggunakan **Generative AI** sebagai pendiskusi teknis untuk memahami requirement, menentukan tahapan pengerjaan yang efektif, serta membantu debugging. Keputusan akhir dan penyesuaian kode tetap saya lakukan secara manual:

1. **Perencanaan tahapan AJAX:** AI membantu saya menentukan urutan pengerjaan yang paling efektif, mulai dari endpoint JSON, AJAX GET, debouncing, modal dan AJAX POST, hingga CSRF, toast notification, dan XSS protection.

2. **Iterative Debugging:** AI membantu menganalisis error pada Django, JavaScript, dan template berdasarkan kode serta error yang saya berikan. Saya kemudian menguji dan menyesuaikan solusi tersebut dengan struktur proyek.

3. **Requirement Checking:** AI membantu mengecek implementasi berdasarkan checklist tugas untuk memastikan fitur seperti loading/empty/error state, permission, HTTP status code, debouncing, dan XSS protection telah terpenuhi.

4. **Manual Refinement:** Beberapa saran AI tidak langsung digunakan. Saya menyesuaikan atau menghilangkan perubahan yang tidak diperlukan agar implementasi tetap sederhana dan sesuai dengan struktur proyek serta requirement tugas.

**Lampiran prompt:**
1. *Pasted requirement tugas*, bantu tentukan tahapan pengerjaan yang paling efektif dan efisien.
2. *Pasted kode dan error*, kenapa terjadi error ini dan apa perbaikan yang paling sesuai dengan struktur proyek?
3. Berdasarkan checklist tugas, bantu cek apakah implementasi AJAX, debouncing, modal, CSRF, toast, dan XSS sudah terpenuhi.
