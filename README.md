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

---

## AI Disclosure & Manual Refinement

Dalam pengerjaan proyek myportofolio, sejauh ini saya memanfaatkan *Generative AI* sebagai pendiskusi teknis. Saya tetap melakukan intervensi teknis dan keputusan secara manual:

1.  **Logika CSS:** AI saya gunakan untuk membantu memahami lebih lanjut fungsi dari suatu styling di CSS, misalnya "apakah cukup dengan `grid-template-columns: repeat(2, 1fr);` dapat memastikan setiap konten tambahan turun ke bawah, bagaimana logika urutan dan ui jika user melakukan klik pada salah satu card?"
2.  **Penanganan Bug** AI membantu saya dalam melakukan debugging, misalnya ketika card *Experience* yang seharusnya hanya muncul 2 dalam 1 row tiba-tiba menjadi 4 card sangat kecil dalam 1 row, saya meminta bantuan AI untuk mengecek apa yang salah (ternyata div yang terduplikat).