import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread

class RoboCopyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python RoboCopy GUI")
        self.root.geometry("700x600")
        
        # Kaynak ve hedef seçimi
        ttk.Label(root, text="Kaynak Dizin:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ttk.Entry(root, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(root, text="Gözat", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(root, text="Hedef Dizin:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_entry = ttk.Entry(root, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(root, text="Gözat", command=self.browse_dest).grid(row=1, column=2, padx=5, pady=5)
        
        # Dosya filtresi
        ttk.Label(root, text="Dosya Filtresi (örn: *.txt):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.file_filter = ttk.Entry(root, width=50)
        self.file_filter.grid(row=2, column=1, padx=5, pady=5)
        
        # Seçenekler
        ttk.Label(root, text="Kopyalama Seçenekleri:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.copy_subdirs = tk.BooleanVar(value=True)
        ttk.Checkbutton(root, text="Alt dizinleri kopyala (/S)", variable=self.copy_subdirs).grid(row=4, column=0, columnspan=3, sticky="w")
        
        self.empty_dirs = tk.BooleanVar()
        ttk.Checkbutton(root, text="Boş dizinleri kopyala (/E)", variable=self.empty_dirs).grid(row=5, column=0, columnspan=3, sticky="w")
        
        self.overwrite = tk.BooleanVar(value=True)
        ttk.Checkbutton(root, text="Varolan dosyaların üzerine yaz (/IS)", variable=self.overwrite).grid(row=6, column=0, columnspan=3, sticky="w")
        
        self.mirror = tk.BooleanVar()
        ttk.Checkbutton(root, text="Aynalama yap (/MIR)", variable=self.mirror).grid(row=7, column=0, columnspan=3, sticky="w")
        
        self.move_files = tk.BooleanVar()
        ttk.Checkbutton(root, text="Dosyaları taşı (kopyalama) (/MOV)", variable=self.move_files).grid(row=8, column=0, columnspan=3, sticky="w")
        
        # Günlük seçenekleri
        ttk.Label(root, text="Günlük Seçenekleri:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        
        self.show_progress = tk.BooleanVar(value=True)
        ttk.Checkbutton(root, text="İlerlemeyi göster (/NP)", variable=self.show_progress).grid(row=10, column=0, columnspan=3, sticky="w")
        
        self.log_file = tk.BooleanVar()
        ttk.Checkbutton(root, text="Günlük dosyası oluştur (/LOG+)", variable=self.log_file).grid(row=11, column=0, columnspan=3, sticky="w")
        
        # İşlem butonları
        ttk.Button(root, text="Kopyalamayı Başlat", command=self.start_copy).grid(row=12, column=0, padx=5, pady=10)
        ttk.Button(root, text="Durdur", command=self.stop_copy).grid(row=12, column=1, padx=5, pady=10)
        ttk.Button(root, text="Çıkış", command=root.quit).grid(row=12, column=2, padx=5, pady=10)
        
        # Günlük alanı
        ttk.Label(root, text="İşlem Günlüğü:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.log_text = tk.Text(root, height=15, width=85)
        self.log_text.grid(row=14, column=0, columnspan=3, padx=5, pady=5)
        
        # İşlem durumu
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=15, column=0, columnspan=3, padx=5, pady=5)
        
        # İşlem kontrolü
        self.is_running = False
        self.should_stop = False
    
    def browse_source(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, directory)
    
    def browse_dest(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, directory)
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_copy(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        
        if not source or not dest:
            messagebox.showerror("Hata", "Kaynak ve hedef dizinleri seçmelisiniz!")
            return
        
        if not os.path.exists(source):
            messagebox.showerror("Hata", "Kaynak dizin bulunamadı!")
            return
        
        # Hedef dizin yoksa oluştur
        if not os.path.exists(dest):
            try:
                os.makedirs(dest)
            except Exception as e:
                messagebox.showerror("Hata", f"Hedef dizin oluşturulamadı: {str(e)}")
                return
        
        self.is_running = True
        self.should_stop = False
        self.progress["value"] = 0
        self.log_text.delete(1.0, tk.END)
        
        # Kopyalama işlemini ayrı bir thread'de başlat
        Thread(target=self.copy_files, args=(source, dest), daemon=True).start()
    
    def stop_copy(self):
        if self.is_running:
            self.should_stop = True
            self.log_message("Kopyalama durduruluyor...")
        else:
            messagebox.showinfo("Bilgi", "Çalışan bir kopyalama işlemi yok.")
    
    def copy_files(self, source, dest):
        try:
            file_filter = self.file_filter.get().strip()
            
            # Dosya listesini oluştur
            files_to_copy = []
            empty_dirs_to_copy = []
            
            if self.copy_subdirs.get() or self.empty_dirs.get() or self.mirror.get():
                # Alt dizinlerle birlikte
                for root_dir, dirs, files in os.walk(source):
                    if self.should_stop:
                        break
                        
                    # Boş dizinler için
                    if self.empty_dirs.get() or self.mirror.get():
                        rel_path = os.path.relpath(root_dir, source)
                        target_dir = os.path.join(dest, rel_path)
                        if not os.path.exists(target_dir):
                            empty_dirs_to_copy.append((root_dir, target_dir))
                    
                    # Dosyalar için
                    for file in files:
                        if self.should_stop:
                            break
                            
                        if file_filter:
                            import fnmatch
                            if not fnmatch.fnmatch(file, file_filter):
                                continue
                                
                        src_file = os.path.join(root_dir, file)
                        rel_path = os.path.relpath(src_file, source)
                        dst_file = os.path.join(dest, rel_path)
                        files_to_copy.append((src_file, dst_file))
            else:
                # Sadece kök dizindeki dosyalar
                for file in os.listdir(source):
                    if self.should_stop:
                        break
                        
                    src_file = os.path.join(source, file)
                    if os.path.isfile(src_file):
                        if file_filter:
                            import fnmatch
                            if not fnmatch.fnmatch(file, file_filter):
                                continue
                                
                        dst_file = os.path.join(dest, file)
                        files_to_copy.append((src_file, dst_file))
            
            # Toplam dosya sayısı
            total_files = len(files_to_copy)
            copied_files = 0
            
            self.log_message(f"Toplam {total_files} dosya kopyalanacak.")
            
            # Boş dizinleri kopyala
            if (self.empty_dirs.get() or self.mirror.get()) and not self.should_stop:
                for src_dir, dst_dir in empty_dirs_to_copy:
                    try:
                        os.makedirs(dst_dir, exist_ok=True)
                        self.log_message(f"Dizin oluşturuldu: {dst_dir}")
                    except Exception as e:
                        self.log_message(f"Dizin oluşturma hatası: {dst_dir} - {str(e)}")
            
            # Dosyaları kopyala
            for src, dst in files_to_copy:
                if self.should_stop:
                    break
                
                try:
                    # Hedef dizin yoksa oluştur
                    dst_dir = os.path.dirname(dst)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir, exist_ok=True)
                    
                    # Dosya zaten varsa ve üzerine yazma kapalıysa atla
                    if os.path.exists(dst) and not self.overwrite.get() and not self.mirror.get():
                        self.log_message(f"Atlandı (zaten var): {dst}")
                        continue
                    
                    # Taşıma veya kopyalama
                    if self.move_files.get():
                        shutil.move(src, dst)
                        self.log_message(f"Taşındı: {src} -> {dst}")
                    else:
                        shutil.copy2(src, dst)
                        self.log_message(f"Kopyalandı: {src} -> {dst}")
                    
                    copied_files += 1
                    progress = (copied_files / total_files) * 100 if total_files > 0 else 100
                    self.progress["value"] = progress
                    self.root.update()
                    
                except Exception as e:
                    self.log_message(f"Hata: {src} -> {dst} - {str(e)}")
            
            # Aynalama modunda hedefteki fazlalıkları sil
            if self.mirror.get() and not self.should_stop:
                self.log_message("Aynalama modu: Hedefteki fazlalıklar kontrol ediliyor...")
                self.cleanup_mirror(source, dest)
            
            if self.should_stop:
                self.log_message("Kopyalama kullanıcı tarafından durduruldu.")
            else:
                self.log_message(f"Kopyalama tamamlandı. Toplam {copied_files}/{total_files} dosya işlendi.")
                self.progress["value"] = 100
            
            self.is_running = False
            
        except Exception as e:
            self.log_message(f"Beklenmeyen hata: {str(e)}")
            self.is_running = False
    
    def cleanup_mirror(self, source, dest):
        """Aynalama modunda hedefte kaynakta olmayan dosyaları sil"""
        try:
            # Hedefteki tüm dosyaları bul
            for root_dir, dirs, files in os.walk(dest):
                if self.should_stop:
                    break
                    
                # Kaynaktaki karşılık gelen dizin
                rel_path = os.path.relpath(root_dir, dest)
                source_dir = os.path.join(source, rel_path)
                
                # Dizin kaynakta yoksa sil
                if not os.path.exists(source_dir):
                    try:
                        shutil.rmtree(root_dir)
                        self.log_message(f"Dizin silindi (kaynakta yok): {root_dir}")
                        continue
                    except Exception as e:
                        self.log_message(f"Dizin silme hatası: {root_dir} - {str(e)}")
                        continue
                
                # Dosyaları kontrol et
                for file in files:
                    if self.should_stop:
                        break
                        
                    dst_file = os.path.join(root_dir, file)
                    src_file = os.path.join(source_dir, file)
                    
                    if not os.path.exists(src_file):
                        try:
                            os.remove(dst_file)
                            self.log_message(f"Dosya silindi (kaynakta yok): {dst_file}")
                        except Exception as e:
                            self.log_message(f"Dosya silme hatası: {dst_file} - {str(e)}")
            
            # Boş dizinleri temizle
            if not self.should_stop:
                for root_dir, dirs, files in os.walk(dest, topdown=False):
                    if self.should_stop:
                        break
                        
                    try:
                        if not os.listdir(root_dir):
                            os.rmdir(root_dir)
                            self.log_message(f"Boş dizin silindi: {root_dir}")
                    except Exception as e:
                        self.log_message(f"Boş dizin silme hatası: {root_dir} - {str(e)}")
                        
        except Exception as e:
            self.log_message(f"Aynalama temizleme hatası: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboCopyGUI(root)
    root.mainloop()
