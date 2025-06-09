import os
import shutil
import threading
import time
from tkinter import filedialog, messagebox, Menu
import customtkinter as ctk
from PIL import Image

class ModernRoboCopyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Uygulama ayarları
        self.title("Modern RoboCopy GUI")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Tema ayarları
        ctk.set_appearance_mode("System")  # Sistem temasını takip eder
        ctk.set_default_color_theme("blue")  # Mavi tema
        
        # Değişkenler
        self.is_running = False
        self.should_stop = False
        self.total_files = 0
        self.copied_files = 0
        
        # UI oluştur
        self.create_widgets()
        
    def create_widgets(self):
        # Ana frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Kaynak ve hedef seçimi
        self.create_source_dest_section()
        
        # Parametreler
        self.create_parameters_section()
        
        # İşlem butonları
        self.create_action_buttons()
        
        # Günlük alanı
        self.create_log_section()
        
        # Durum çubuğu
        self.status_bar = ctk.CTkLabel(self, text="Hazır", anchor="w")
        self.status_bar.pack(fill="x", padx=10, pady=(0, 10))
    
    def create_source_dest_section(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", padx=5, pady=5)
        
        # Kaynak
        ctk.CTkLabel(frame, text="Kaynak Dizin:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ctk.CTkEntry(frame, width=400)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        browse_img = ctk.CTkImage(Image.open("folder.png") if os.path.exists("folder.png") else None, size=(20, 20))
        ctk.CTkButton(frame, text="Gözat", image=browse_img, width=30, command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Hedef
        ctk.CTkLabel(frame, text="Hedef Dizin:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dest_entry = ctk.CTkEntry(frame, width=400)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(frame, text="Gözat", image=browse_img, width=30, command=self.browse_dest).grid(row=1, column=2, padx=5, pady=5)
        
        # Dosya filtresi
        ctk.CTkLabel(frame, text="Dosya Filtresi:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.file_filter = ctk.CTkEntry(frame, placeholder_text="örn: *.txt;*.docx", width=400)
        self.file_filter.grid(row=2, column=1, padx=5, pady=5)
    
    def create_parameters_section(self):
        # Notebook (sekme yapısı)
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="x", padx=5, pady=5)
        
        # Temel parametreler sekmesi
        self.tab1 = self.tabview.add("Temel")
        self.tab2 = self.tabview.add("Gelişmiş")
        self.tab3 = self.tabview.add("Günlük")
        
        # Temel sekme
        self.copy_subdirs = ctk.CTkSwitch(self.tab1, text="Alt dizinleri kopyala (/S)")
        self.copy_subdirs.pack(pady=5, anchor="w")
        self.copy_subdirs.select()
        
        self.empty_dirs = ctk.CTkSwitch(self.tab1, text="Boş dizinleri kopyala (/E)")
        self.empty_dirs.pack(pady=5, anchor="w")
        
        self.overwrite = ctk.CTkSwitch(self.tab1, text="Varolan dosyaların üzerine yaz (/IS)")
        self.overwrite.pack(pady=5, anchor="w")
        self.overwrite.select()
        
        self.mirror = ctk.CTkSwitch(self.tab1, text="Aynalama yap (/MIR)")
        self.mirror.pack(pady=5, anchor="w")
        
        # Gelişmiş sekme
        self.move_files = ctk.CTkSwitch(self.tab2, text="Dosyaları taşı (kopyalama) (/MOV)")
        self.move_files.pack(pady=5, anchor="w")
        
        self.purge = ctk.CTkSwitch(self.tab2, text="Hedefteki fazlalıkları sil (/PURGE)")
        self.purge.pack(pady=5, anchor="w")
        
        self.multi_thread = ctk.CTkSwitch(self.tab2, text="Çoklu thread kullan (/MT)")
        self.multi_thread.pack(pady=5, anchor="w")
        self.multi_thread.select()
        
        self.retry = ctk.CTkEntry(self.tab2, placeholder_text="Tekrar deneme sayısı (/R)")
        self.retry.pack(pady=5, fill="x")
        
        # Günlük sekmesi
        self.show_progress = ctk.CTkSwitch(self.tab3, text="İlerlemeyi göster (/NP)")
        self.show_progress.pack(pady=5, anchor="w")
        self.show_progress.select()
        
        self.log_file = ctk.CTkSwitch(self.tab3, text="Günlük dosyası oluştur (/LOG+)")
        self.log_file.pack(pady=5, anchor="w")
        
        self.log_path = ctk.CTkEntry(self.tab3, placeholder_text="Günlük dosya yolu")
        self.log_path.pack(pady=5, fill="x")
    
    def create_action_buttons(self):
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        # Butonlar
        start_img = ctk.CTkImage(Image.open("play.png") if os.path.exists("play.png") else None, size=(20, 20))
        self.start_btn = ctk.CTkButton(
            button_frame, text="Kopyalamayı Başlat", 
            image=start_img, command=self.start_copy
        )
        self.start_btn.pack(side="left", padx=5, pady=5)
        
        stop_img = ctk.CTkImage(Image.open("stop.png") if os.path.exists("stop.png") else None, size=(20, 20))
        self.stop_btn = ctk.CTkButton(
            button_frame, text="Durdur", 
            image=stop_img, command=self.stop_copy,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5, pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(button_frame, orientation="horizontal", mode="determinate")
        self.progress.pack(side="right", padx=5, pady=5, fill="x", expand=True)
        self.progress.set(0)
        
        # Dosya sayacı
        self.file_counter = ctk.CTkLabel(button_frame, text="0/0 dosya")
        self.file_counter.pack(side="right", padx=10)
    
    def create_log_section(self):
        # Günlük alanı
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(log_frame, text="İşlem Günlüğü").pack(anchor="w", padx=5, pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Context menu
        self.log_menu = Menu(self, tearoff=False)
        self.log_menu.add_command(label="Temizle", command=self.clear_log)
        self.log_menu.add_command(label="Kopyala", command=self.copy_log)
        
        self.log_text.bind("<Button-3>", lambda e: self.log_menu.tk_popup(e.x_root, e.y_root))
    
    def browse_source(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, directory)
    
    def browse_dest(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, directory)
    
    def clear_log(self):
        self.log_text.delete("1.0", "end")
    
    def copy_log(self):
        self.clipboard_clear()
        self.clipboard_append(self.log_text.get("1.0", "end"))
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.update_status(f"Son işlem: {message}")
    
    def update_status(self, message):
        self.status_bar.configure(text=message)
    
    def update_progress(self, current, total):
        progress = (current / total) * 100 if total > 0 else 0
        self.progress.set(progress / 100)
        self.file_counter.configure(text=f"{current}/{total} dosya")
    
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
        self.progress.set(0)
        self.clear_log()
        
        # Buton durumlarını güncelle
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Kopyalama işlemini ayrı bir thread'de başlat
        threading.Thread(target=self.copy_files, args=(source, dest), daemon=True).start()
    
    def stop_copy(self):
        if self.is_running:
            self.should_stop = True
            self.log_message("Kopyalama durduruluyor...")
        else:
            messagebox.showinfo("Bilgi", "Çalışan bir kopyalama işlemi yok.")
    
    def copy_files(self, source, dest):
        try:
            file_filter = self.file_filter.get().strip()
            filters = [f.strip() for f in file_filter.split(";")] if file_filter else []
            
            # Dosya listesini oluştur
            files_to_copy = []
            empty_dirs_to_copy = []
            
            if self.copy_subdirs.get() or self.empty_dirs.get() or self.mirror.get() or self.purge.get():
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
                            
                        if filters:
                            import fnmatch
                            if not any(fnmatch.fnmatch(file, pattern) for pattern in filters):
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
                        if filters:
                            import fnmatch
                            if not any(fnmatch.fnmatch(file, pattern) for pattern in filters):
                                continue
                                
                        dst_file = os.path.join(dest, file)
                        files_to_copy.append((src_file, dst_file))
            
            # Toplam dosya sayısı
            self.total_files = len(files_to_copy)
            self.copied_files = 0
            
            self.log_message(f"Toplam {self.total_files} dosya kopyalanacak.")
            self.update_progress(0, self.total_files)
            
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
                        self.copied_files += 1
                        self.update_progress(self.copied_files, self.total_files)
                        continue
                    
                    # Taşıma veya kopyalama
                    if self.move_files.get():
                        shutil.move(src, dst)
                        self.log_message(f"Taşındı: {src} -> {dst}")
                    else:
                        shutil.copy2(src, dst)
                        self.log_message(f"Kopyalandı: {src} -> {dst}")
                    
                    self.copied_files += 1
                    self.update_progress(self.copied_files, self.total_files)
                    
                except Exception as e:
                    self.log_message(f"Hata: {src} -> {dst} - {str(e)}")
            
            # Aynalama veya temizleme modunda hedefteki fazlalıkları sil
            if (self.mirror.get() or self.purge.get()) and not self.should_stop:
                self.log_message("Hedefteki fazlalıklar kontrol ediliyor...")
                self.cleanup_target(source, dest)
            
            if self.should_stop:
                self.log_message("Kopyalama kullanıcı tarafından durduruldu.")
            else:
                self.log_message(f"Kopyalama tamamlandı. Toplam {self.copied_files}/{self.total_files} dosya işlendi.")
                self.progress.set(1.0)
            
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            
        except Exception as e:
            self.log_message(f"Beklenmeyen hata: {str(e)}")
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
    
    def cleanup_target(self, source, dest):
        """Hedefte kaynakta olmayan dosyaları sil"""
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
            self.log_message(f"Hedef temizleme hatası: {str(e)}")

if __name__ == "__main__":
    app = ModernRoboCopyApp()
    app.mainloop()
