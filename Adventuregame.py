import os
import time
import random

# ═════════════════════════════════════════════════════════════
#        PEONY'S MAGICAL POTION SHOP - ADVENTURE GAME
#              Petualangan Meramu Ramuan Ajaib
# ═════════════════════════════════════════════════════════════

class PeonyPotionGame2:
    def __init__(self):
        self.gold = 0
        self.reputation = 0
        self.customers_served = 0
        self.inventory = []
        self.completed_orders = 0
        self.failed_orders = 0
        self.unlockedRecipes = set()  # Track recipe yang sudah dibuka
        
        # Buku Ramuan Ajaib - Semua resep
        self.all_potions = {
            "Ramuan Kesehatan": {
                "deskripsi": "Menyembuhkan luka ringan dan meningkatkan energi",
                "price": 50,
                "recipe_price": 30,
                "ingredients": {
                    "Daun Mint Hutan": {"jumlah": 3, "efek": "menenangkan", "efek_desc": "Menenangkan yang kuat dan berlapis (butuh porsi lumayan)", "benar": True},
                    "Bunga Chamomile": {"jumlah": 2, "efek": "penenang", "efek_desc": "Penenang sedang", "benar": False},
                    "Akar Ginger": {"jumlah": 1, "efek": "hangat", "efek_desc": "Kehangatan ringan (hanya sedikit diperlukan)", "benar": True}
                },
                "cara_meramu": "Campurkan bahan dengan perlahan, aduk akan membawa efek terbaik"
            },
            "Ramuan Kekuatan": {
                "deskripsi": "Meningkatkan kekuatan fisik dan ketahanan tubuh",
                "price": 75,
                "recipe_price": 40,
                "ingredients": {
                    "Biji Ginseng Merah": {"jumlah": 2, "efek": "energi", "efek_desc": "Energi yang seimbang (butuh dua bagian)", "benar": True},
                    "Kulit Pohon Elm": {"jumlah": 1, "efek": "kuat", "efek_desc": "Kekuatan kokoh (esensial tapi hanya sedikit)", "benar": True},
                    "Bubuk Batu Mulia": {"jumlah": 1, "efek": "cemerlang", "efek_desc": "Kilau berkilauan", "benar": False}
                },
                "cara_meramu": "Panaskan dengan hati-hati, jangan terlalu panas atau hasil akan berkurang"
            },
            "Ramuan Berani": {
                "deskripsi": "Memberikan keberanian dan menghilangkan ketakutan",
                "price": 60,
                "recipe_price": 35,
                "ingredients": {
                    "Kelopak Bunga Mawar Merah": {"jumlah": 4, "efek": "berani", "efek_desc": "Keberanian yang membara (butuh banyak kelopak!)", "benar": True},
                    "Bulu Burung Elang": {"jumlah": 1, "efek": "terbang", "efek_desc": "Terbang tinggi", "benar": False},
                    "Akar Jahe Liar": {"jumlah": 2, "efek": "panas", "efek_desc": "Panas yang menyala (butuh dua bagian)", "benar": True}
                },
                "cara_meramu": "Aduk dengan penuh semangat, energi Anda akan mempengaruhi hasilnya"
            },
            "Ramuan Mimpi Indah": {
                "deskripsi": "Memberikan tidur nyenyak dan mimpi indah",
                "price": 55,
                "recipe_price": 32,
                "ingredients": {
                    "Bunga Lavender": {"jumlah": 5, "efek": "tenang", "efek_desc": "Kedamaian mendalam (butuh banyak bunga untuk efek penuh)", "benar": True},
                    "Kelopak Bunga Teratai": {"jumlah": 2, "efek": "nyenyak", "efek_desc": "Nyenyak yang sempurna (butuh dua kelopak)", "benar": True},
                    "Bulu Burung Hantu Putih": {"jumlah": 1, "efek": "sihir", "efek_desc": "Keajaiban mistis", "benar": False}
                },
                "cara_meramu": "Aduk perlahan dengan penuh kasih sayang, intuisi Anda adalah panduan"
            },
            "Ramuan Antitoksin": {
                "deskripsi": "Menetralisir racun dan membersihkan tubuh",
                "price": 80,
                "recipe_price": 50,
                "ingredients": {
                    "Rumput Liar Penawar": {"jumlah": 3, "efek": "bersih", "efek_desc": "Pembersihan menyeluruh (memerlukan tiga bagian rumput)", "benar": True},
                    "Biji Tumbuhan Belladonna": {"jumlah": 1, "efek": "toksin", "efek_desc": "Racun ganda", "benar": False},
                    "Akar Burdock": {"jumlah": 2, "efek": "pembersih", "efek_desc": "Pembersih alami (dua akar diperlukan)", "benar": True}
                },
                "cara_meramu": "Rebus dengan sempurna, terlalu cepat atau lambat akan berpengaruh"
            }
        }
        
        # Buku ramuan yang dibuka (awalnya hanya satu)
        self.unlockedRecipes.add("Ramuan Kesehatan")
        self.potion_book = {k: v for k, v in self.all_potions.items() if k in self.unlockedRecipes}
        
        # Area Petualangan dan Tanaman
        self.adventure_areas = {
            "Hutan Gelap": {
                "plants": {
                    "Daun Mint Hutan": {"benar": True, "rarity": "umum"},
                    "Biji Beracun": {"benar": False, "rarity": "langka"},
                    "Rumput Liar": {"benar": False, "rarity": "umum"}
                },
                "deskripsi": "Hutan yang gelap dan menakutkan, tapi kaya dengan tanaman obat"
            },
            "Bukit Batu": {
                "plants": {
                    "Akar Ginger": {"benar": True, "rarity": "umum"},
                    "Biji Ginseng Merah": {"benar": True, "rarity": "langka"},
                    "Batu Berkilau": {"benar": False, "rarity": "langka"}
                },
                "deskripsi": "Bukit yang terjal dan penuh dengan batu-batu besar"
            },
            "Taman Bunga Liar": {
                "plants": {
                    "Kelopak Bunga Mawar Merah": {"benar": True, "rarity": "umum"},
                    "Bunga Lavender": {"benar": True, "rarity": "umum"},
                    "Kelopak Bunga Teratai": {"benar": True, "rarity": "langka"},
                    "Duri Beracun": {"benar": False, "rarity": "umum"}
                },
                "deskripsi": "Taman yang indah dengan berbagai macam bunga yang mekar"
            },
            "Rawa Mistis": {
                "plants": {
                    "Akar Burdock": {"benar": True, "rarity": "umum"},
                    "Rumput Liar Penawar": {"benar": True, "rarity": "langka"},
                    "Lumut Mencurigakan": {"benar": False, "rarity": "umum"},
                    "Kulit Pohon Elm": {"benar": True, "rarity": "umum"}
                },
                "deskripsi": "Rawa yang berselimut kabut tebal, tempat berbahaya tapi penuh sumber daya"
            }
        }
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def slow_print(self, text, delay=0.02):
        """Print text dengan efek mengetik"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def print_title(self):
        """Display game title"""
        self.clear_screen()
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  🧙‍♂️  PEONY'S MAGICAL POTION SHOP - ADVENTURE GAME  🧙‍♂️".center(68) + "║")
        print("║" + "      Meramu Ramuan Ajaib untuk Menyelamatkan Orang Lain".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
    
    def display_stats(self):
        """Display Peony stats"""
        print(f"📊 STATUS PEONY")
        print(f"   💰 Emas: {self.gold}")
        print(f"   ⭐ Reputasi: {self.reputation}")
        print(f"   📦 Pesanan Selesai: {self.completed_orders}")
        print(f"   ❌ Pesanan Gagal: {self.failed_orders}")
        print()
    
    def show_potion_book(self):
        """Tampilkan daftar ramuan di buku"""
        self.clear_screen()
        self.print_title()
        print("📚 BUKU RAMUAN AJAIB PEONY\n")
        print("=" * 70)
        
        for idx, (potion_name, details) in enumerate(self.potion_book.items(), 1):
            print(f"\n{idx}. 🧪 {potion_name}")
            print(f"   📝 Deskripsi: {details['deskripsi']}")
            print(f"   💰 Harga Jual: {details['price']} Emas")
            print(f"   📋 Cara Meramu: {details['cara_meramu']}")
            print(f"   🌿 Bahan-bahan yang benar memiliki efek:")
            
            for ingredient, props in details['ingredients'].items():
                if props['benar']:
                    print(f"      • {ingredient} - [{props['efek']}]")
            print()
    
    def show_recipe_shop(self):
        """Toko Resep - Beli resep ramuan baru"""
        while True:
            self.clear_screen()
            self.print_title()
            print("🏪 TOKO RESEP RAMUAN AJAIB\n")
            print("=" * 70)
            
            self.display_stats()
            
            print("\n📚 Resep yang Tersedia:\n")
            
            available_recipes = []
            for idx, (potion_name, details) in enumerate(self.all_potions.items(), 1):
                if potion_name not in self.unlockedRecipes:
                    available_recipes.append((potion_name, details))
                    print(f"{idx}. 📖 {potion_name}")
                    print(f"   {details['deskripsi']}")
                    print(f"   💰 Harga Resep: {details['recipe_price']} Emas\n")
                else:
                    print(f"✅ {potion_name} (Sudah Dibeli)\n")
            
            print("=" * 70)
            
            if not available_recipes:
                print("\n🎉 Selamat! Kamu sudah membeli semua resep ramuan!")
                input("\nTekan ENTER untuk kembali...")
                break
            
            print(f"\n0. ❌ Keluar dari Toko")
            print(f"\nPilih nomor resep yang ingin dibeli (atau 0 untuk keluar):")
            
            choice = input("\n> ").strip()
            
            if choice == "0":
                break
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(available_recipes):
                    recipe_name, recipe_details = available_recipes[choice_idx]
                    recipe_cost = recipe_details['recipe_price']
                    
                    print(f"\n📖 {recipe_name}")
                    print(f"   Harga: {recipe_cost} Emas")
                    print(f"\nKamu punya: {self.gold} Emas")
                    
                    if self.gold >= recipe_cost:
                        confirm = input(f"\nBeli resep ini? (ya/tidak): ").strip().lower()
                        if confirm == 'ya' or confirm == 'y':
                            self.gold -= recipe_cost
                            self.unlockedRecipes.add(recipe_name)
                            self.potion_book[recipe_name] = self.all_potions[recipe_name]
                            
                            print(f"\n✅ BERHASIL! Resep {recipe_name} berhasil dibeli!")
                            print(f"   Sisa emas: {self.gold}")
                            input("\nTekan ENTER untuk melanjutkan...")
                    else:
                        print(f"\n❌ Emas tidak cukup! Kurang {recipe_cost - self.gold} Emas.")
                        input("\nTekan ENTER untuk melanjutkan...")
                else:
                    print("❌ Pilihan tidak valid.")
                    time.sleep(1)
            except (ValueError, IndexError):
                print("❌ Pilihan tidak valid.")
                time.sleep(1)
    
    def intro_scene(self):
        """Pembukaan cerita Peony"""
        self.print_title()
        time.sleep(1)
        
        self.slow_print("📖 MULAI PETUALANGAN BERSAMA PEONY\n", delay=0.05)
        time.sleep(1)
        
        opening_text = """
╔═══════════════════════════════════════════════════════════════════╗
║                    ✨ CERITA DIMULAI ✨                          ║
╚═══════════════════════════════════════════════════════════════════╝

Hiduplah seorang kurcaci muda bernama PEONY.
Kesehariannya hanya tentang mencari tanaman obat, meramu obat, 
dan eksperimen eksperimen lainnya.

Di pedalaman hutan yang gelap dan penuh misteri, Peony memiliki rumah kecil 
yang dikelilingi berbagai tanaman ajaib. Di rumahnya terdapat laboratorium 
sederhana dengan berbagai cairan, botol, dan alat meramu yang aneh.

Peony terkenal di seluruh desa karena kemampuannya meramu ramuan ajaib 
yang benar-benar berkhasiat. Banyak orang yang datang membeli ramuannya 
untuk berbagai keperluan.

Hari ini dimulai seperti hari biasa, namun... sesuatu yang berbeda 
akan terjadi...
        """
        
        self.slow_print(opening_text, delay=0.01)
        time.sleep(2)
        
        input("\n⏳ Tekan ENTER untuk lanjut...\n")
    
    def show_customer_order(self):
        """Pelanggan datang memesan ramuan"""
        self.clear_screen()
        self.print_title()
        
        time.sleep(1)
        
        # Pilih ramuan secara random
        potion_names = list(self.potion_book.keys())
        ordered_potion = random.choice(potion_names)
        
        print("🚪 DET-DET-DET! Ada yang mengetuk pintu rumahmu!\n")
        time.sleep(1)
        
        customer_names = ["Petani Odi", "Nenek Elsa", "Prajurit Kuat", "Pedagang Angin", "Pemuda Penasaran"]
        customer_name = random.choice(customer_names)
        
        self.slow_print(f"Seorang {customer_name} masuk dengan terburu-buru...\n")
        time.sleep(1)
        
        print(f"👤 {customer_name}: 'Halo Peony! Aku membutuhkan {ordered_potion}!'")
        print(f"                 'Bisakah kau buatkan untuk saya?'\n")
        
        potion_details = self.potion_book[ordered_potion]
        print(f"📜 Pesanan: {ordered_potion}")
        print(f"📝 Deskripsi: {potion_details['deskripsi']}")
        print(f"💰 Bayaran: {potion_details['price']} Emas\n")
        
        print("=" * 70)
        print("🤔 Pilihan Peony:\n")
        print("1. ✅ Terima pesanan ini")
        print("2. ❌ Tolak pesanan (tidak punya bahan)")
        
        choice = input("\n> ").strip()
        
        if choice == "1":
            return ordered_potion, customer_name
        else:
            print(f"\n😢 {customer_name}: 'Sayang sekali... aku akan mencari Peony lain.'")
            input("\nTekan ENTER untuk melanjutkan...")
            return None, None
    
    def adventure_gathering(self, potion_name):
        """Petualangan mencari bahan ramuan"""
        self.clear_screen()
        self.print_title()
        
        print("🏕️  PETUALANGAN MENCARI BAHAN RAMUAN\n")
        time.sleep(1)
        
        potion_details = self.potion_book[potion_name]
        required_ingredients = {ing: props for ing, props in potion_details['ingredients'].items() if props['benar']}
        
        self.slow_print(f"Peony bersiap untuk mencari bahan {potion_name}...\n")
        time.sleep(1)
        
        print(f"📋 Bahan yang perlu dicari memiliki efek:")
        for ingredient in required_ingredients.keys():
            effect = required_ingredients[ingredient]['efek']
            print(f"   • Sesuatu dengan efek [{effect}]")
        print()
        time.sleep(2)
        
        gathered_ingredients = {}
        
        for ingredient_needed in required_ingredients.keys():
            print("=" * 70)
            print(f"🌿 Mencari bahan dengan efek [{required_ingredients[ingredient_needed]['efek']}]\n")
            time.sleep(1)
            
            # Cari area yang memiliki ingredient
            found_area = None
            for area_name, area_data in self.adventure_areas.items():
                if ingredient_needed in area_data['plants']:
                    found_area = (area_name, area_data)
                    break
            
            if found_area:
                area_name, area_data = found_area
                print(f"🗺️  Peony pergi ke: {area_name}")
                print(f"   Deskripsi: {area_data['deskripsi']}\n")
                time.sleep(1)
                
                # Presentasikan pilihan tanaman TANPA menunjukkan jumlah
                plants_list = list(area_data['plants'].keys())
                random.shuffle(plants_list)
                
                print(f"👀 Peony melihat beberapa tanaman di area ini:\n")
                
                for idx, plant_name in enumerate(plants_list[:3], 1):
                    plant_info = area_data['plants'][plant_name]
                    # Pilih info acak tentang tanaman
                    plant_descriptions = [
                        f"Tanaman dengan aroma yang menenangkan",
                        f"Tanaman berwarna hijau cerah dengan daun lebar",
                        f"Tanaman berbunga dengan keharuman yang memikat",
                        f"Tanaman berbatang tebal dan kokoh",
                        f"Tanaman dengan tekstur unik dan warna menawan"
                    ]
                    desc = random.choice(plant_descriptions)
                    print(f"{idx}. 🌱 {plant_name}")
                    print(f"    {desc} (Langka: {plant_info['rarity']})")
                    # Tampilkan efek yang dirasakan saat menyentuh
                    effects_near = [
                        "Mencium aroma yang lezat",
                        "Merasa energi hangat",
                        "Merasakan kesegaran",
                        "Merasakan kehangatan"
                    ]
                    print(f"    Saat Peony mendekati, {random.choice(effects_near)}")
                
                print(f"\n💭 Mana yang cocok dengan efek [{required_ingredients[ingredient_needed]['efek']}]?\n")
                
                while True:
                    try:
                        choice = int(input("> ").strip())
                        if 1 <= choice <= 3:
                            selected_plant = plants_list[choice - 1]
                            
                            if selected_plant == ingredient_needed:
                                print(f"\n✅ TEPAT! {selected_plant} memancarkan efek [{required_ingredients[ingredient_needed]['efek']}] yang sempurna!\n")
                                gathered_ingredients[ingredient_needed] = required_ingredients[ingredient_needed]['jumlah']
                                time.sleep(1)
                                break
                            else:
                                is_good_plant = area_data['plants'][selected_plant]['benar'] if selected_plant in area_data['plants'] else False
                                
                                if is_good_plant and selected_plant != ingredient_needed:
                                    print(f"\n⚠️  SALAH! {selected_plant} memang tanaman bagus, tapi efeknya tidak sesuai.")
                                    print(f"   Efeknya bukan [{required_ingredients[ingredient_needed]['efek']}].")
                                    print(f"   Coba lagi!\n")
                                else:
                                    print(f"\n❌ SALAH! {selected_plant} adalah tanaman berbahaya!")
                                    print(f"   Jika digunakan, pembeli bisa mengalami alergi atau keracunan!\n")
                            
                            time.sleep(1)
                        else:
                            print("Pilihan tidak valid. Coba lagi (1-3).\n")
                    except ValueError:
                        print("Masukan tidak valid. Coba lagi.\n")
        
        print("\n" + "=" * 70)
        print("✅ SEMUA BAHAN BERHASIL DIKUMPULKAN!\n")
        print("Peony kembali ke rumahnya untuk meramu...\n")
        time.sleep(2)
        
        return gathered_ingredients
    
    def brewing_process(self, potion_name, ingredients):
        """Proses meramu ramuan"""
        self.clear_screen()
        self.print_title()
        
        print("🧪 PROSES MERAMU RAMUAN\n")
        print("=" * 70 + "\n")
        
        potion_details = self.potion_book[potion_name]
        
        self.slow_print(f"Peony mulai meramu {potion_name}...\n")
        time.sleep(1)
        
        print(f"📖 Panduan: {potion_details['cara_meramu']}\n")
        time.sleep(1)
        
        required_ingredients = {ing: props for ing, props in potion_details['ingredients'].items() if props['benar']}
        
        # Proses meramu TANPA menunjukkan jumlah yang tepat
        # Sistem berbasis intuisi dan keberuntungan
        success = True
        quality_score = 0
        
        for ingredient, props in required_ingredients.items():
            print(f"🌿 Menambahkan {ingredient}...")
            efek_desc = props.get('efek_desc', props['efek'])
            print(f"   📝 Petunjuk efek: {efek_desc}")
            print(f"   ⚗️  Berapa banyak yang harus ditambahkan? (Dengarkan petunjuk efek!)\n")
            
            # Player input jumlah tanpa tahu jawaban yang benar
            max_attempts = 2
            perfect_amount = props['jumlah']
            
            for attempt in range(max_attempts):
                try:
                    player_amount = int(input(f"   Masukkan jumlah (Usaha {attempt + 1}/{max_attempts}): "))
                    
                    if player_amount == perfect_amount:
                        print(f"   ✨ Sempurna! Efek ramuan mulai bersinar!")
                        quality_score += 2
                        time.sleep(0.5)
                        break
                    elif player_amount == perfect_amount - 1 or player_amount == perfect_amount + 1:
                        print(f"   ⚠️  Hampir sempurna... Ramuan bereaksi baik.")
                        quality_score += 1
                        time.sleep(0.5)
                        break
                    elif player_amount == perfect_amount - 2 or player_amount == perfect_amount + 2:
                        print(f"   😕 Tidak ideal... Ramuan bereaksi aneh.")
                        quality_score += 0
                        time.sleep(0.5)
                        break
                    else:
                        if attempt == 0:
                            print(f"   ❌ Bereaksi tidak sesuai... Coba lagi!\n")
                        else:
                            print(f"   💥 Ramuan mulai bergejolak berbahaya!\n")
                            success = False
                        time.sleep(0.5)
                except ValueError:
                    print("   ❌ Input tidak valid. Coba angka.\n")
            
            if not success:
                break
            
            print()
        
        print("=" * 70 + "\n")
        time.sleep(1)
        
        if not success:
            print("💥 BENCANA MERAMU!\n")
            self.slow_print(f"Tiba-tiba ledakan kecil terjadi di labu!")
            self.slow_print(f"Ramuan meledak dan menyebar di mana-mana!")
            self.slow_print(f"Peony terbakar dan percikan api memecahkan botol!")
            return False, False  # (success, perfect)
        
        elif quality_score >= len(required_ingredients) * 2:
            print("✨ MERAMU SEMPURNA!\n")
            self.slow_print(f"Ramuan berubah warna menjadi indah yang memukau.")
            self.slow_print(f"Cahaya ajaib memancar dari botol!")
            self.slow_print(f"{potion_name} berhasil dibuat dengan sempurna!")
            return True, True  # (success, perfect)
        elif quality_score >= len(required_ingredients):
            print("✅ MERAMU BERHASIL!\n")
            self.slow_print("Ramuan berubah warna yang benar dan bercahaya.")
            self.slow_print(f"{potion_name} berhasil dibuat!")
            return True, False  # (success, not perfect)
        else:
            print("⚠️  MERAMU MENGECEWAKAN\n")
            self.slow_print("Ramuan berhasil dibuat, tapi warna dan efeknya terlihat meragukan.")
            self.slow_print(f"{potion_name} jadi, tapi kualitasnya biasa saja.")
            return True, False  # (success, not perfect)
    
    def deliver_potion(self, potion_name, customer_name, brewing_success, brewing_perfect, used_wrong_ingredient):
        """Pengiriman ramuan kepada pelanggan"""
        self.clear_screen()
        self.print_title()
        
        print("📦 PENGIRIMAN RAMUAN\n")
        print("=" * 70 + "\n")
        
        potion_details = self.potion_book[potion_name]
        
        print(f"Peony mengemas {potion_name} dan menyerahkannya kepada {customer_name}...\n")
        time.sleep(2)
        
        if not brewing_success:
            print(f"💔 {customer_name}: 'Apa-apaan ini?! Botolnya kosong! Lebih baik aku bayar setengah.'")
            reward = potion_details['price'] // 2
            self.gold += reward
            self.failed_orders += 1
            self.reputation -= 5
            print(f"\n❌ PESANAN GAGAL: Mendapat {reward} Emas (Reputasi -5)")
            
        elif used_wrong_ingredient:
            print(f"⏰ Seminggu kemudian...")
            print(f"😤 {customer_name}: 'PEONY! Aku minum ramuanmu dan jadi alergi!'\n")
            print(f"   'Pipisku membengkak dan gatal di mana-mana!'")
            
            self.failed_orders += 1
            self.reputation -= 10
            self.gold -= 20  # Denda
            print(f"\n❌ PESANAN GAGAL AKIBAT ALERGI: -20 Emas, Reputasi -10")
            
        elif brewing_perfect:
            print(f"😍 {customer_name}: 'Wah! Ini adalah ramuan terbaik yang pernah aku coba!'")
            print(f"               'Terima kasih Peony! Aku akan rekomendasikan ke semua orang!'")
            
            bonus = 20
            reward = potion_details['price'] + bonus
            self.gold += reward
            self.completed_orders += 1
            self.reputation += 10
            print(f"\n✨ PESANAN SEMPURNA! Mendapat {reward} Emas (Reputasi +10)")
            
        else:
            print(f"😊 {customer_name}: 'Terima kasih Peony! Ramuan ini bagus.'")
            print(f"               'Mungkin coba yang lebih sempurna lagi ya.'")
            
            reward = potion_details['price']
            self.gold += reward
            self.completed_orders += 1
            self.reputation += 3
            print(f"\n✅ PESANAN BERHASIL: Mendapat {reward} Emas (Reputasi +3)")
        
        self.display_stats()
        input("\nTekan ENTER untuk melanjutkan...")
    
    def main_game_loop(self):
        """Main game loop"""
        self.intro_scene()
        
        while True:
            self.clear_screen()
            self.print_title()
            
            print("═" * 70)
            print("🏠 RUMAH PEONY - MENU UTAMA")
            print("═" * 70 + "\n")
            
            self.display_stats()
            
            print("\n📋 Apa yang ingin Peony lakukan?\n")
            print("1. 📚 Lihat Buku Ramuan Ajaib")
            print("2. 🏪 Kunjungi Toko Resep")
            print("3. 🚪 Tunggu Pelanggan Datang")
            print("4. 💤 Istirahat (Simpan & Akhiri Game)")
            
            choice = input("\n> ").strip()
            
            if choice == "1":
                self.show_potion_book()
                input("\nTekan ENTER untuk kembali...")
                
            elif choice == "2":
                self.show_recipe_shop()
                
            elif choice == "3":
                ordered_potion, customer_name = self.show_customer_order()
                
                if ordered_potion and customer_name:
                    # Proses petualangan
                    ingredients = self.adventure_gathering(ordered_potion)
                    
                    # Check if used wrong ingredient
                    used_wrong = False
                    wrong_ingredient_names = [ing for ing, props in self.potion_book[ordered_potion]['ingredients'].items() if not props['benar']]
                    # Dalam game ini, semua ingredients yang correct sudah dipilih
                    # Jadi used_wrong = False untuk sekarang (bisa diexpand)
                    
                    # Proses meramu
                    success, perfect = self.brewing_process(ordered_potion, ingredients)
                    
                    # Pengiriman dan hasil
                    self.deliver_potion(ordered_potion, customer_name, success, perfect, used_wrong)
                    
            elif choice == "4":
                self.clear_screen()
                self.print_title()
                
                print("💤 Peony tertidur pulas setelah hari yang panjang...\n")
                print("=" * 70)
                print("📊 STATISTIK AKHIR PERMAINAN")
                print("=" * 70 + "\n")
                
                self.display_stats()
                
                total_orders = self.completed_orders + self.failed_orders
                success_rate = (self.completed_orders / total_orders * 100) if total_orders > 0 else 0
                
                print(f"📈 Rasio Kesuksesan: {self.completed_orders}/{total_orders} ({success_rate:.1f}%)")
                print(f"📚 Resep yang Dikuasai: {len(self.unlockedRecipes)}/{len(self.all_potions)}")
                
                if self.reputation >= 30:
                    print("\n🌟 STATUS: Peony menjadi pramuan terkenal di seluruh kerajaan!")
                elif self.reputation >= 15:
                    print("\n⭐ STATUS: Peony dikenal cukup baik oleh komunitas.")
                elif self.reputation > 0:
                    print("\n👤 STATUS: Peony mulai terkenal.")
                else:
                    print("\n😞 STATUS: Peony harus lebih hati-hati dengan ramuannya.")
                
                print("\nTerima kasih telah bermain Peony's Potion Shop!\n")
                print("═" * 70)
                break
            else:
                print("❌ Pilihan tidak valid. Coba lagi.")
                time.sleep(1)


def main():
    """Jalankan game"""
    game = PeonyPotionGame2()
    game.main_game_loop()


if __name__ == "__main__":
    main()
