PBP Tugas 3
===========
### Adyatma Wijaksara Aryaputra Nugraha Yudha - 2106750805
### [HTML](https://pbp-tugas2-adyatma.herokuapp.com/mywatchlist/html) | [XML](https://pbp-tugas2-adyatma.herokuapp.com/mywatchlist/xml) | [JSON](https://pbp-tugas2-adyatma.herokuapp.com/mywatchlist/json)

Jelaskan perbedaan antara JSON, XML, dan HTML!
-
- JSOM (JavaScript Object Notation)
Untuk menyimpan data dalam bentuk key dan value.
- XML (Extensible Markup Language)
Untuk mengirim data dari suatu stack ke stack lain (misal dari json ke html).
- HTML (HyperText Markup Language)
Untuk mendefinisikan struktur dan menampilkan data dari data suatu data delivery.

Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
-
Karena kita membutuhkan data delivery untuk mengirim data dari satu stack ke stack lainnya. Hal ini karena untuk data yang banyak tidak mungkin untuk disimpan dalam frontend. Sehingga kita membutuhkan data delivery untuk menampilkan data tersebut yang disimpan di backend.

Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas.
-
1. Buat aplikasi mywatchlist baru dengan `python manage.py startapp mywatchlist`.
2. Buat sepuluh data awal `WatchListItem` dengan atribut `title`, `rating`, `release_date`, `watched`, `review`. di dalam folder `fixtures`.
3. Buat model `WatchListItem` dengan atribut `title`, `rating`, `release_date`, `watched`, `review`.
4. Buat fungsi `show_watchlist`, `show_mywatchlist_html`, `show_mywatchlist_xml`, dan `show_mywatchlist_json` di dalam views.py.
5. Buat template 'mywatchlist.html' untuk menampilkan data dari `show_mywatchlist_html`.
6. Buat routing di `mywatchlist\urls.py` untuk menampilkan data dari `show_watchlist`, `show_mywatchlist_html`, `show_mywatchlist_xml`, dan `show_mywatchlist_json`.
7. Buat routing app di `project_django\urls.py` untuk mengarahkan ke `mywatchlist\urls.py`.
8. Buat test case dengan `tests.py` untuk `show_mywatchlist_html`, `show_mywatchlist_xml`, dan `show_mywatchlist_json`.
8. Daftarkan app mywatchlist ke dalam `project_django\settings.py`.
9. Jalankan perintah `python manage.py makemigrations` dan `python manage.py migrate` untuk membuat tabel baru.
10. Jalankan perintah `python manage.py loaddata fixtures\mywatchlist.json` untuk memasukkan data awal ke dalam tabel.

Mengakses tiga URL di poin 6 menggunakan Postman, menangkap screenshot, dan menambahkannya ke dalam README.md
-
- HTML
  ![alt text](./assets/PBP%20Tugas%203%20-%20HTML.png "HTML di Postman")
- XML
  ![alt text](./assets/PBP%20Tugas%203%20-%20XML.png "XML di Postman")
- JSON
  ![alt text](./assets/PBP%20Tugas%203%20-%20JSON.png "JSON di Postman")


