# Proyek Pemantauan Gudang Real-time dengan Kafka dan PySpark

Proyek ini mensimulasikan sistem pemantauan suhu dan kelembaban gudang secara real-time menggunakan Apache Kafka sebagai message broker dan Apache Spark (PySpark) untuk pemrosesan stream data.

## Daftar Isi
1.  [Fitur Utama](#fitur-utama)
2.  [Arsitektur](#arsitektur)
3.  [Prasyarat](#prasyarat)
4.  [Struktur Proyek](#struktur-proyek)
5.  [Setup Lingkungan Awal (Untuk Pengguna Baru/Clone)](#setup-lingkungan-awal-untuk-pengguna-baruclone)
6.  [Setup Lingkungan Detail (Jika Menginstal dari Awal)](#setup-lingkungan-detail-jika-menginstal-dari-awal)
    *   [Java Development Kit (JDK)](#java-development-kit-jdk)
    *   [Python](#python)
    *   [Apache Kafka](#apache-kafka)
    *   [Apache Spark](#apache-spark)
    *   [Visual Studio Code (Opsional)](#visual-studio-code-opsional)
7.  [Menjalankan Aplikasi](#menjalankan-aplikasi)
    *   [Langkah 1: Jalankan Zookeeper](#langkah-1-jalankan-zookeeper)
    *   [Langkah 2: Jalankan Kafka Server](#langkah-2-jalankan-kafka-server)
    *   [Langkah 3: Buat Topik Kafka (Hanya Jika Belum Ada)](#langkah-3-buat-topik-kafka-hanya-jika-belum-ada)
    *   [Langkah 4: Jalankan Producer Kafka](#langkah-4-jalankan-producer-kafka)
    *   [Langkah 5: Jalankan PySpark Consumer/Processor](#langkah-5-jalankan-pyspark-consumerprocessor)
8.  [Contoh Output](#contoh-output)
9.  [Menghentikan Aplikasi](#menghentikan-aplikasi)
10. [Troubleshooting Umum](#troubleshooting-umum)

## Fitur Utama
*   Simulasi data sensor suhu dan kelembaban dari beberapa gudang.
*   Pengiriman data sensor ke topik Kafka secara real-time.
*   Konsumsi dan pemrosesan stream data menggunakan PySpark.
*   Filtering data untuk peringatan suhu tinggi (> 80°C) dan kelembaban tinggi (> 70%).
*   Penggabungan (join) stream data suhu dan kelembaban berdasarkan ID gudang dan window waktu.
*   Deteksi kondisi kritis (suhu > 80°C DAN kelembaban > 70%) dan pemberian status gudang.
*   Output hasil analisis ke konsol.

## Arsitektur
1.  **Sensor Suhu (Producer Python)**: Mengirim data suhu (JSON) ke topik `sensor-suhu-gudang` di Kafka.
2.  **Sensor Kelembaban (Producer Python)**: Mengirim data kelembaban (JSON) ke topik `sensor-kelembaban-gudang` di Kafka.
3.  **Apache Kafka**: Berperan sebagai message broker, menerima dan menyimpan stream data dari producer.
4.  **PySpark Streaming Application (Consumer/Processor)**:
    *   Membaca data dari kedua topik Kafka.
    *   Melakukan filter individual.
    *   Melakukan join stream berdasarkan `gudang_id` dan window waktu.
    *   Menganalisis kondisi gabungan dan mencetak status serta peringatan.

## Prasyarat
Sebelum memulai, pastikan sistem Anda telah terinstal komponen-komponen dasar yang tercantum di bagian [Setup Lingkungan Detail](#setup-lingkungan-detail-jika-menginstal-dari-awal), terutama JDK, Python, Kafka, dan Spark.

## Struktur Proyek
```
BigDataKafkaProject/
├── .venv/                     # Folder virtual environment (diabaikan oleh Git)
├── kafka_producers/
│   ├── suhu_producer.py
│   └── kelembaban_producer.py
├── spark_consumer/
│   └── pyspark_consumer_processor.py
├── .gitignore                 # File untuk mengabaikan file/folder tertentu oleh Git
├── requirements.txt           # File daftar dependensi Python
└── README.md                  # File ini
```

## Setup Lingkungan Awal (Untuk Pengguna Baru/Clone)
Jika Anda meng-clone repositori ini atau memulai di lingkungan baru:

1.  **Clone Repositori (jika belum):**
    ```bash
    git clone https://github.com/Nopitrasari29/BigDataKafkaProject_502723012.git
    cd BigDataKafkaProject_502723012
    ```
2.  **Pastikan Prasyarat Dasar Terinstal:** Anda masih memerlukan JDK, Python, Apache Kafka, dan Apache Spark terinstal dan terkonfigurasi di sistem Anda seperti yang dijelaskan di [Setup Lingkungan Detail](#setup-lingkungan-detail-jika-menginstal-dari-awal). `README` ini tidak mencakup instalasi Kafka/Spark itu sendiri, hanya setup proyek Python.
3.  **Buat Virtual Environment:**
    Di direktori utama proyek, jalankan:
    ```bash
    python -m venv .venv
    ```
4.  **Aktifkan Virtual Environment:**
    *   **Command Prompt (cmd) Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **PowerShell Windows:** (Anda mungkin perlu menjalankan `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` di PowerShell sebagai Administrator sekali)
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    Prompt terminal Anda akan berubah, diawali dengan `(.venv)`.
5.  **Instal Dependensi Python:**
    Dengan virtual environment aktif, jalankan:
    ```bash
    pip install -r requirements.txt
    ```
    Ini akan menginstal `kafka-python` dan `pyspark` dengan versi yang sesuai.

## Setup Lingkungan Detail (Jika Menginstal dari Awal)

Bagian ini menjelaskan instalasi komponen utama jika Anda belum memilikinya.

### Java Development Kit (JDK)
1.  Unduh dan instal JDK (misal, JDK 11 dari Oracle atau Adoptium Temurin).
2.  Atur environment variable `JAVA_HOME` ke direktori instalasi JDK Anda (misal, `C:\Program Files\Java\jdk-11.0.15`).
3.  Tambahkan `%JAVA_HOME%\bin` ke environment variable `Path` sistem Anda.

### Python
1.  Unduh dan instal Python (versi 3.8 - 3.10 direkomendasikan) dari [python.org](https://www.python.org/downloads/).
2.  Saat instalasi, centang opsi "Add Python to PATH".

### Apache Kafka
1.  Unduh versi binary Kafka (misal, `kafka_2.13-3.9.1.tgz` jika Spark Anda menggunakan Scala 2.13, atau `kafka_2.12-X.Y.Z.tgz` jika Spark Anda Scala 2.12) dari [kafka.apache.org/downloads](https://kafka.apache.org/downloads).
2.  Ekstrak ke direktori (misal, `D:\kafka\kafka_2.13-3.9.1`). Sebut ini `KAFKA_HOME`.
    *Catatan: Versi Scala Kafka (`_2.12` atau `_2.13`) sebaiknya cocok dengan versi Scala Spark Anda untuk menghindari potensi masalah, meskipun untuk koneksi dasar tidak selalu strik.*

### Apache Spark
1.  Unduh versi binary Spark "pre-built for Apache Hadoop" (misal, `spark-3.5.5-bin-hadoop3` yang dibangun dengan Scala 2.12) dari [spark.apache.org/downloads.html](https://spark.apache.org/downloads.html). **Pastikan versi Scala Spark (misal `_2.12`) cocok dengan akhiran pada package Kafka yang akan Anda gunakan di `spark-submit`.**
2.  Ekstrak ke direktori (misal, `D:\spark-hadoop\spark-3.5.5-bin-hadoop3`).
3.  Atur environment variable `SPARK_HOME` ke direktori ini.
4.  **Untuk Windows:**
    *   Unduh `winutils.exe` yang sesuai dengan versi Hadoop yang digunakan Spark Anda (misal, dari [GitHub cdarlint/winutils](https://github.com/cdarlint/winutils)).
    *   Buat direktori `C:\hadoop\bin` (atau path lain).
    *   Letakkan `winutils.exe` di `C:\hadoop\bin\`.
    *   Atur environment variable `HADOOP_HOME` ke `C:\hadoop`.
    *   Tambahkan `%SPARK_HOME%\bin` dan `%HADOOP_HOME%\bin` ke environment variable `Path` sistem Anda.
5.  Restart komputer Anda jika Anda baru saja mengatur environment variables.

## Menjalankan Aplikasi

### Langkah 1: Jalankan Zookeeper
Buka Command Prompt BARU (jangan di dalam venv VSCode).
```cmd
cd D:\kafka\kafka_2.13-3.9.1  # Sesuaikan dengan path KAFKA_HOME Anda
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```
Tunggu hingga Zookeeper siap (muncul pesan `binding to port 0.0.0.0/0.0.0.0:2181` dan tidak ada error baru).

### Langkah 2: Jalankan Kafka Server
Buka Command Prompt BARU LAINNYA.
```cmd
cd D:\kafka\kafka_2.13-3.9.1  # Sesuaikan dengan path KAFKA_HOME Anda
.\bin\windows\kafka-server-start.bat .\config\server.properties
```
Tunggu hingga Kafka Server siap (muncul pesan `[KafkaServer id=X] started` dan terhubung ke Zookeeper).

### Langkah 3: Buat Topik Kafka (Hanya Jika Belum Ada)
Jika ini adalah kali pertama Anda menjalankan atau jika topik telah dihapus. Buka Command Prompt BARU KETIGA.
```cmd
cd D:\kafka\kafka_2.13-3.9.1  # Sesuaikan dengan path KAFKA_HOME Anda

.\bin\windows\kafka-topics.bat --create --topic sensor-suhu-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

.\bin\windows\kafka-topics.bat --create --topic sensor-kelembaban-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Anda akan melihat pesan `Created topic ...`. Biarkan terminal Zookeeper dan Kafka Server tetap berjalan.

### Langkah 4: Jalankan Producer Kafka
Buka dua terminal di VSCode (atau terminal lain). Pastikan virtual environment `(.venv)` aktif di kedua terminal tersebut.

*   **Terminal 1 (Producer Suhu):**
    ```bash
    # (.venv) PS C:\path\to\BigDataKafkaProject_502723012> 
    python kafka_producers/suhu_producer.py
    ```
*   **Terminal 2 (Producer Kelembaban):**
    ```bash
    # (.venv) PS C:\path\to\BigDataKafkaProject_502723012> 
    python kafka_producers/kelembaban_producer.py
    ```
Biarkan kedua producer ini berjalan.

### Langkah 5: Jalankan PySpark Consumer/Processor
Buka terminal ketiga di VSCode (atau terminal lain). Pastikan virtual environment `(.venv)` aktif.

1.  **Set Environment Variables untuk PySpark (PENTING untuk Windows):**
    Hanya perlu dijalankan sekali per sesi terminal.
    *   **PowerShell:**
        ```powershell
        $env:PYSPARK_PYTHON = ".\.venv\Scripts\python.exe"
        $env:PYSPARK_DRIVER_PYTHON = ".\.venv\Scripts\python.exe"
        ```
    *   **Command Prompt (cmd):**
        ```cmd
        set PYSPARK_PYTHON=.\.venv\Scripts\python.exe
        set PYSPARK_DRIVER_PYTHON=.\.venv\Scripts\python.exe
        ```

2.  **Jalankan `spark-submit`:**
    **PENTING:** Sesuaikan nilai `KAFKA_PACKAGE` di dalam file `spark_consumer/pyspark_consumer_processor.py` agar cocok dengan versi Spark dan Scala yang Anda gunakan. Contohnya sudah ada di dalam file tersebut. Perintah `spark-submit` akan menggunakan konfigurasi tersebut.
    ```bash
    # (.venv) PS C:\path\to\BigDataKafkaProject_502723012> 
    spark-submit spark_consumer/pyspark_consumer_processor.py
    ```
    *Catatan: `KAFKA_PACKAGE` sekarang dikonfigurasi di dalam skrip PySpark, jadi tidak perlu `--packages` di sini lagi jika skrip sudah disesuaikan.*

Tunggu beberapa saat, Anda akan melihat output analisis data di terminal ini.

## Contoh Output
1. suhu_producer.py
![image](https://github.com/user-attachments/assets/2a334b05-eb64-4e82-8955-f355d31cb317)

2. kelembaban_producer.py
![image](https://github.com/user-attachments/assets/06ec6535-733c-450e-9af4-7839dac503c5)

3. pyspark_consumer_processor.py
![image](https://github.com/user-attachments/assets/9e956ca6-5eeb-45cb-abd1-8684168acc66)


## Menghentikan Aplikasi
1.  Tekan `Ctrl+C` di terminal PySpark (Consumer/Processor). Skrip sudah diatur untuk mencoba menghentikan SparkSession dengan bersih.
2.  Tekan `Ctrl+C` di masing-masing terminal Producer Python.
3.  Tekan `Ctrl+C` di terminal Kafka Server.
4.  Tekan `Ctrl+C` di terminal Zookeeper.
5.  Untuk menonaktifkan virtual environment di terminal, ketik: `deactivate`

## Troubleshooting Umum
*   **`JAVA_HOME not set`**: Pastikan `JAVA_HOME` dan `Path` sudah benar.
*   **`winutils.exe` error / `NullPointerException` di Spark (Windows)**: Pastikan `HADOOP_HOME` dan `Path` benar, dan `winutils.exe` ada di `%HADOOP_HOME%\bin`.
*   **Kafka `Connection refused`**: Pastikan Zookeeper berjalan SEBELUM Kafka Server. Pastikan Zookeeper dan Kafka Server benar-benar siap sebelum menjalankan producer/consumer.
*   **PySpark `Python was not found` atau `Cannot run program "python3"`**:
    *   Nonaktifkan "App execution aliases" untuk `python.exe` dan `python3.exe` di Windows Settings.
    *   Setel `$env:PYSPARK_PYTHON` dan `$env:PYSPARK_DRIVER_PYTHON` (PowerShell) atau `set PYSPARK_PYTHON` / `set PYSPARK_DRIVER_PYTHON` (cmd) ke path `python.exe` di dalam `venv` Anda sebelum menjalankan `spark-submit`.
*   **PySpark `NoClassDefFoundError` atau `ClassNotFoundException` (seringkali terkait `scala.*`)**:
    *   Ini biasanya karena ketidakcocokan versi Scala antara instalasi Spark Anda dan package Kafka yang digunakan. Verifikasi versi Scala Spark Anda dengan `spark-shell`. Kemudian, pastikan variabel `KAFKA_PACKAGE` di dalam file `pyspark_consumer_processor.py` dikonfigurasi dengan benar menggunakan akhiran Scala (`_2.12` atau `_2.13`) dan versi Spark yang sesuai.
*   **Python `IndentationError`**: Periksa spasi/tab yang tidak konsisten di kode Python Anda.
*   **PySpark `TypeError: DataFrame.join() got an unexpected keyword argument 'joinType'`**: Ganti `joinType="inner"` menjadi `how="inner"` pada metode `join()` di skrip PySpark.
