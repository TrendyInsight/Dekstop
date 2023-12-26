import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Variabel global untuk menyimpan objek axes
ax = None
canvas = None  # Variabel global untuk menyimpan objek canvas

# Fungsi untuk mengambil data dari database dan menampilkan rekomendasi outfit di antarmuka pengguna
def tampilkan_data():
    # Membuat koneksi ke database
    conn = sqlite3.connect('mobile_data.db')
    cursor = conn.cursor()

    # Mengambil data dari tabel
    cursor.execute('SELECT * FROM data')
    records = cursor.fetchall()

    # Membersihkan tampilan sebelum menampilkan data baru
    for row in tree.get_children():
        tree.delete(row)

    # Menampilkan data dalam antarmuka pengguna
    for record in records:
        tree.insert('', 'end', values=record)

    # Menutup koneksi
    conn.close()

# Fungsi untuk memperbarui grafik bar chart secara real-time
def update_live_chart(frame):
    # Membuat koneksi ke database
    conn = sqlite3.connect('mobile_data.db')
    cursor = conn.cursor()

    # Mengambil data untuk grafik
    cursor.execute('SELECT * FROM data')
    records = cursor.fetchall()

    # Menutup koneksi
    conn.close()

    # Memisahkan data untuk kolom "Atasan Favorit," "Bawahan Favorit," "Terusan Favorit," dan "Rekomendasi Outfit"
    atasan_favorit = [record[2] for record in records]
    bawahan_favorit = [record[3] for record in records]
    terusan_favorit = [record[4] for record in records]

    # Bersihkan grafik sebelum menggambar yang baru
    ax.clear()

    # Jumlah kategori (Atasan Favorit, Bawahan Favorit, Terusan Favorit)
    num_categories = len(atasan_favorit)

    # Lebar bar
    bar_width = 0.2

    # Koordinat untuk setiap kategori
    index = range(num_categories)

    # Warna RGB untuk legenda
    colors = [(0.2, 0.4, 0.6), (0.8, 0.2, 0.4), (0.4, 0.6, 0.2)]

    # Gambar grafik bar chart
    bars = []
    for i, (data, color) in enumerate(zip([atasan_favorit, bawahan_favorit, terusan_favorit], colors)):
        bar = ax.bar([j + i * bar_width for j in index], data, bar_width, color=color, label=f'Kategori {i+1}')
        bars.append(bar)

    # Tambahkan label dan judul
    ax.set_xlabel('Data ID')
    ax.set_ylabel('Favorit Count')
    ax.set_title('Grafik Live Favorit')

    # Tambahkan legenda dengan menggunakan RGB
    legend_labels = ['Atasan Favorit', 'Bawahan Favorit', 'Terusan Favorit']
    ax.legend(handles=bars, labels=legend_labels)

    # Update canvas
    canvas.draw()

# Fungsi untuk menampilkan grafik saat tombol "Lihat Grafik Live Outfit Favorit" diklik
def tampilkan_grafik():
    global ax, canvas

    # Membuat grafik live chart
    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=app)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Menambahkan animasi untuk memperbarui grafik secara real-time
    ani = FuncAnimation(fig, update_live_chart, frames=None, interval=1000)  # Interval dalam milidetik (1000 ms = 1 detik)

    # Memanggil fungsi untuk memperbarui grafik
    update_live_chart(None)

    # Menampilkan grafik
    canvas.draw()

# Buat database SQLite jika belum ada
conn = sqlite3.connect('mobile_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        content TEXT,
        atasan_favorit INTEGER,
        bawahan_favorit INTEGER,
        terusan_favorit INTEGER,
        rekomendasi_outfit TEXT
    )
''')
conn.commit()
conn.close()

# Membuat antarmuka pengguna tkinter
app = tk.Tk()
app.title("Trendy Insight Desktop")
app.iconbitmap("klambi.ico")

# Membuat tabel untuk menampilkan data
tree = ttk.Treeview(app, columns=('Atasan Favorit', 'Bawahan Favorit', 'Terusan Favorit', 'Rekomendasi Outfit'), show='headings')
tree.heading('Atasan Favorit', text='Atasan Favorit')
tree.heading('Bawahan Favorit', text='Bawahan Favorit')
tree.heading('Terusan Favorit', text='Terusan Favorit')
tree.heading('Rekomendasi Outfit', text='Rekomendasi Outfit')  # Menambahkan kolom "Rekomendasi Outfit"
tree.pack()

# Membuat tombol untuk memperbarui data
btn_refresh = tk.Button(app, text="Refresh Data", command=tampilkan_data)
btn_refresh.pack()

# Membuat tombol untuk menampilkan grafik
btn_show_chart = tk.Button(app, text="Lihat Grafik Outfit Favorit", command=tampilkan_grafik)
btn_show_chart.pack()

app.mainloop()
