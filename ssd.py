import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import requests
import threading
import io
import math
import random

# ─── Theme Configuration ───────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_deep":       "#0D0D1A",
    "bg_card":       "#141428",
    "bg_panel":      "#1A1A35",
    "accent_pink":   "#FF6B9D",
    "accent_purple": "#A855F7",
    "accent_teal":   "#06B6D4",
    "accent_gold":   "#F59E0B",
    "text_primary":  "#F5E6FF",
    "text_muted":    "#9CA3AF",
    "border":        "#2D2D5A",
    "success":       "#10B981",
    "tag_bg":        "#2D1B69",
}

# ─── Comprehensive Women's Health Disease Database ─────────────────────────────
DISEASES_DB = {
    "PCOS (Polycystic Ovary Syndrome)": {
        "emoji": "🌸",
        "category": "Hormonal",
        "description": "A hormonal disorder causing enlarged ovaries with small cysts. Affects 1 in 10 women of childbearing age.",
        "symptoms": ["Irregular periods", "Excess androgen", "Weight gain", "Acne", "Hair thinning", "Mood changes"],
        "diet": {
            "eat": [
                "🥦 High-fiber vegetables (broccoli, spinach, kale)",
                "🐟 Lean proteins (salmon, tuna, chicken breast)",
                "🫐 Anti-inflammatory berries (blueberries, strawberries)",
                "🥑 Healthy fats (avocado, olive oil, nuts)",
                "🌾 Low-GI grains (quinoa, brown rice, oats)",
                "🧄 Anti-inflammatory spices (turmeric, cinnamon, ginger)",
            ],
            "avoid": [
                "🍞 Refined carbs and white bread",
                "🥤 Sugary drinks and sodas",
                "🍔 Processed and fried foods",
                "🧀 Full-fat dairy (limit intake)",
                "🍭 Sweets and sugary snacks",
            ]
        },
        "exercises": [
            {"name": "Brisk Walking", "duration": "30 min/day", "benefit": "Improves insulin sensitivity", "icon": "🚶‍♀️"},
            {"name": "Yoga (Restorative)", "duration": "45 min, 3x/week", "benefit": "Reduces cortisol & balances hormones", "icon": "🧘‍♀️"},
            {"name": "Strength Training", "duration": "30 min, 2-3x/week", "benefit": "Builds muscle, improves metabolism", "icon": "🏋️‍♀️"},
            {"name": "Swimming", "duration": "30 min, 3x/week", "benefit": "Low-impact, full-body workout", "icon": "🏊‍♀️"},
            {"name": "Cycling", "duration": "20-30 min/day", "benefit": "Boosts cardiovascular health", "icon": "🚴‍♀️"},
        ],
        "color": "#FF6B9D"
    },
    "Endometriosis": {
        "emoji": "🌺",
        "category": "Reproductive",
        "description": "Tissue similar to the uterine lining grows outside the uterus, causing severe pain and potential fertility issues.",
        "symptoms": ["Pelvic pain", "Heavy periods", "Painful intercourse", "Fatigue", "Bloating", "Infertility"],
        "diet": {
            "eat": [
                "🥬 Dark leafy greens (spinach, swiss chard)",
                "🫚 Omega-3 rich foods (flaxseeds, walnuts, fish)",
                "🍋 Citrus fruits high in Vitamin C",
                "🫚 Extra virgin olive oil",
                "🥕 Colorful vegetables (carrots, beets, peppers)",
                "🍵 Green tea (anti-inflammatory)",
            ],
            "avoid": [
                "🥩 Red meat and processed meats",
                "🧁 Gluten (many patients benefit from reduction)",
                "🥛 Dairy products",
                "☕ Excess caffeine and alcohol",
                "🍟 Trans fats and fast food",
            ]
        },
        "exercises": [
            {"name": "Gentle Yoga", "duration": "30 min, daily", "benefit": "Reduces pelvic tension and pain", "icon": "🧘‍♀️"},
            {"name": "Pilates", "duration": "40 min, 3x/week", "benefit": "Strengthens core without aggravating symptoms", "icon": "🤸‍♀️"},
            {"name": "Walking", "duration": "20-30 min, daily", "benefit": "Releases endorphins, natural pain relief", "icon": "🚶‍♀️"},
            {"name": "Stretching", "duration": "15 min, daily", "benefit": "Relieves muscle tension around pelvis", "icon": "🙆‍♀️"},
            {"name": "Swimming", "duration": "30 min, 2x/week", "benefit": "Non-impact, reduces inflammation", "icon": "🏊‍♀️"},
        ],
        "color": "#A855F7"
    },
    "Breast Cancer": {
        "emoji": "🎗️",
        "category": "Oncology",
        "description": "Cancer that forms in the cells of the breasts. Most common cancer among women worldwide, highly treatable when detected early.",
        "symptoms": ["Lump in breast", "Change in breast shape", "Nipple discharge", "Skin dimpling", "Breast pain"],
        "diet": {
            "eat": [
                "🥦 Cruciferous vegetables (broccoli, cauliflower, Brussels sprouts)",
                "🍇 Resveratrol-rich foods (grapes, berries, pomegranate)",
                "🫚 Flaxseeds (lignans that may reduce estrogen)",
                "🐟 Fatty fish (anti-inflammatory omega-3s)",
                "🧅 Allium vegetables (garlic, onions, leeks)",
                "🍵 Green tea and antioxidant-rich foods",
            ],
            "avoid": [
                "🍷 Alcohol (even moderate amounts increase risk)",
                "🍖 Processed meats",
                "🧈 High saturated fat foods",
                "🍭 High sugar foods (feed cancer cells)",
                "🥡 Ultra-processed packaged foods",
            ]
        },
        "exercises": [
            {"name": "Aerobic Exercise", "duration": "150 min/week", "benefit": "Reduces recurrence risk by 40-50%", "icon": "🏃‍♀️"},
            {"name": "Strength Training", "duration": "2x/week", "benefit": "Preserves bone density during treatment", "icon": "🏋️‍♀️"},
            {"name": "Yoga", "duration": "45 min, 3x/week", "benefit": "Reduces fatigue and anxiety", "icon": "🧘‍♀️"},
            {"name": "Walking", "duration": "30 min, daily", "benefit": "Maintains healthy weight, boosts mood", "icon": "🚶‍♀️"},
            {"name": "Tai Chi", "duration": "30 min, 3x/week", "benefit": "Improves balance and reduces stress", "icon": "🥋"},
        ],
        "color": "#EC4899"
    },
    "Osteoporosis": {
        "emoji": "🦴",
        "category": "Bone Health",
        "description": "A condition where bones become weak and brittle. Women are 4x more likely than men to develop osteoporosis after menopause.",
        "symptoms": ["Back pain", "Height loss", "Stooped posture", "Bone fractures", "Brittle nails", "Muscle weakness"],
        "diet": {
            "eat": [
                "🥛 Calcium-rich dairy (low-fat milk, yogurt, cheese)",
                "🥬 Leafy greens (kale, bok choy, collard greens)",
                "🐟 Canned salmon and sardines (with bones)",
                "☀️ Vitamin D-fortified foods",
                "🥜 Almonds and sesame seeds",
                "🍊 Citrus fruits (Vitamin C for collagen)",
            ],
            "avoid": [
                "☕ Excess caffeine (more than 3 cups/day)",
                "🍷 Alcohol (interferes with calcium absorption)",
                "🧂 High-sodium foods (increase calcium loss)",
                "🥤 Carbonated drinks (phosphoric acid affects bones)",
                "🍖 Very high protein diets (may leach calcium)",
            ]
        },
        "exercises": [
            {"name": "Weight-Bearing Walking", "duration": "30-45 min, daily", "benefit": "Stimulates bone density", "icon": "🚶‍♀️"},
            {"name": "Resistance Training", "duration": "30 min, 3x/week", "benefit": "Builds bone and muscle mass", "icon": "🏋️‍♀️"},
            {"name": "Balance Exercises", "duration": "15 min, daily", "benefit": "Prevents falls and fractures", "icon": "🤸‍♀️"},
            {"name": "Tai Chi", "duration": "45 min, 2x/week", "benefit": "Improves balance and coordination", "icon": "🥋"},
            {"name": "Dancing", "duration": "30 min, 3x/week", "benefit": "Weight-bearing and joyful for bones", "icon": "💃"},
        ],
        "color": "#06B6D4"
    },
    "Thyroid Disorders": {
        "emoji": "🦋",
        "category": "Endocrine",
        "description": "Women are 5-8x more likely than men to develop thyroid issues. Includes hypothyroidism, hyperthyroidism, and Hashimoto's thyroiditis.",
        "symptoms": ["Fatigue", "Weight changes", "Mood swings", "Hair loss", "Temperature sensitivity", "Heart palpitations"],
        "diet": {
            "eat": [
                "🥜 Brazil nuts (selenium for thyroid function)",
                "🐟 Seafood (iodine source)",
                "🥚 Eggs (iodine and selenium)",
                "🫐 Antioxidant-rich berries",
                "🥕 Colorful vegetables and fruits",
                "🌾 Gluten-free grains (for Hashimoto's)",
            ],
            "avoid": [
                "🥦 Raw cruciferous veggies in excess (goitrogens)",
                "🌰 Soy products in large amounts",
                "🍭 Processed sugars and refined carbs",
                "☕ Excess caffeine",
                "🧂 Iodized salt (for hyperthyroidism)",
            ]
        },
        "exercises": [
            {"name": "Yoga", "duration": "45 min, 3x/week", "benefit": "Stimulates thyroid through neck poses", "icon": "🧘‍♀️"},
            {"name": "Walking", "duration": "30 min, daily", "benefit": "Boosts metabolism gently", "icon": "🚶‍♀️"},
            {"name": "Swimming", "duration": "30 min, 3x/week", "benefit": "Regulates body temperature", "icon": "🏊‍♀️"},
            {"name": "Light Jogging", "duration": "20 min, 3x/week", "benefit": "Improves cardiovascular and metabolism", "icon": "🏃‍♀️"},
            {"name": "Stretching", "duration": "15 min, daily", "benefit": "Reduces muscle stiffness", "icon": "🙆‍♀️"},
        ],
        "color": "#F59E0B"
    },
    "Menopause": {
        "emoji": "🌙",
        "category": "Life Stage",
        "description": "The natural end of menstrual cycles, typically occurring in a woman's late 40s to early 50s, accompanied by significant hormonal changes.",
        "symptoms": ["Hot flashes", "Night sweats", "Sleep issues", "Mood changes", "Vaginal dryness", "Memory fog"],
        "diet": {
            "eat": [
                "🫘 Phytoestrogen foods (soy, flaxseeds, chickpeas)",
                "🥛 Calcium and Vitamin D rich foods",
                "🐟 Omega-3 fatty acids (salmon, mackerel)",
                "🫐 Antioxidant-rich fruits and vegetables",
                "💧 Plenty of water and hydrating foods",
                "🌾 Whole grains for sustained energy",
            ],
            "avoid": [
                "🌶️ Spicy foods (trigger hot flashes)",
                "☕ Caffeine and alcohol (worsen symptoms)",
                "🍭 Sugar and refined carbs",
                "🧂 High sodium foods (causes water retention)",
                "🍔 Processed foods (worsen inflammation)",
            ]
        },
        "exercises": [
            {"name": "Cardio Exercise", "duration": "150 min/week", "benefit": "Reduces hot flash severity", "icon": "🏃‍♀️"},
            {"name": "Strength Training", "duration": "2-3x/week", "benefit": "Prevents muscle and bone loss", "icon": "🏋️‍♀️"},
            {"name": "Yoga", "duration": "45 min, 3x/week", "benefit": "Reduces anxiety, improves sleep", "icon": "🧘‍♀️"},
            {"name": "Pilates", "duration": "40 min, 2x/week", "benefit": "Improves posture and flexibility", "icon": "🤸‍♀️"},
            {"name": "Dancing", "duration": "30 min, 3x/week", "benefit": "Lifts mood and maintains bone health", "icon": "💃"},
        ],
        "color": "#8B5CF6"
    },
    "Uterine Fibroids": {
        "emoji": "🌷",
        "category": "Reproductive",
        "description": "Noncancerous growths of the uterus that often appear during childbearing years. Affect up to 80% of women by age 50.",
        "symptoms": ["Heavy periods", "Pelvic pressure", "Frequent urination", "Lower back pain", "Constipation", "Abdominal bloating"],
        "diet": {
            "eat": [
                "🥬 Dark leafy greens (reduce estrogen dominance)",
                "🫐 Berries (flavonoids that inhibit fibroid growth)",
                "🐟 Cold-water fish (anti-inflammatory omega-3s)",
                "🫚 Flaxseeds (balance estrogen)",
                "🍋 Citrus (Vitamin C, reduce heavy bleeding)",
                "🥕 Beta-carotene rich foods (carrots, sweet potato)",
            ],
            "avoid": [
                "🥩 Red meat and pork (fuel estrogen)",
                "☕ Alcohol and caffeine",
                "🌽 High-glycemic foods",
                "🧀 Dairy products",
                "🍭 Refined sugar",
            ]
        },
        "exercises": [
            {"name": "Walking", "duration": "30 min, daily", "benefit": "Reduces estrogen levels naturally", "icon": "🚶‍♀️"},
            {"name": "Swimming", "duration": "30 min, 3x/week", "benefit": "Low-impact, reduces pelvic pressure", "icon": "🏊‍♀️"},
            {"name": "Yoga", "duration": "40 min, 3x/week", "benefit": "Reduces stress hormones that worsen fibroids", "icon": "🧘‍♀️"},
            {"name": "Light Cycling", "duration": "20 min, 3x/week", "benefit": "Improves circulation in pelvic area", "icon": "🚴‍♀️"},
            {"name": "Tai Chi", "duration": "30 min, 2x/week", "benefit": "Gentle movement, stress reduction", "icon": "🥋"},
        ],
        "color": "#EC4899"
    },
    "Cervical Cancer": {
        "emoji": "🔴",
        "category": "Oncology",
        "description": "Cancer of the cervix, often caused by HPV infection. Highly preventable with vaccination and regular Pap smears.",
        "symptoms": ["Abnormal vaginal bleeding", "Pelvic pain", "Pain during intercourse", "Unusual discharge", "Back pain"],
        "diet": {
            "eat": [
                "🥦 Cruciferous vegetables (broccoli, cabbage)",
                "🫐 Berries (antioxidants fight cell damage)",
                "🧄 Garlic (allicin with anti-cancer properties)",
                "🍊 Citrus fruits (Vitamin C, folate)",
                "🥕 Beta-carotene foods (carrots, pumpkin)",
                "🌿 Folate-rich foods (asparagus, lentils)",
            ],
            "avoid": [
                "🍷 Alcohol",
                "🍔 Processed and fast foods",
                "🍭 Sugar-rich foods",
                "☕ Excessive caffeine",
                "🥡 Packaged and preservative-rich foods",
            ]
        },
        "exercises": [
            {"name": "Gentle Walking", "duration": "30 min, daily", "benefit": "Boosts immune function", "icon": "🚶‍♀️"},
            {"name": "Yoga", "duration": "40 min, 3x/week", "benefit": "Reduces treatment side effects", "icon": "🧘‍♀️"},
            {"name": "Stretching", "duration": "20 min, daily", "benefit": "Reduces fatigue and tension", "icon": "🙆‍♀️"},
            {"name": "Swimming", "duration": "30 min, 2x/week", "benefit": "Gentle cardio during recovery", "icon": "🏊‍♀️"},
            {"name": "Deep Breathing", "duration": "10 min, daily", "benefit": "Reduces anxiety and improves oxygen flow", "icon": "💨"},
        ],
        "color": "#EF4444"
    },
    "Ovarian Cancer": {
        "emoji": "💛",
        "category": "Oncology",
        "description": "Cancer that forms in or on the ovaries. Often called the 'silent killer' due to vague early symptoms. Early detection improves survival significantly.",
        "symptoms": ["Bloating", "Pelvic pain", "Frequent urination", "Difficulty eating", "Back pain", "Fatigue"],
        "diet": {
            "eat": [
                "🥬 Leafy greens (protective phytonutrients)",
                "🍅 Tomatoes (lycopene, cancer-fighting compound)",
                "🫐 Colorful berries (high antioxidants)",
                "🐟 Omega-3 fish (anti-inflammatory)",
                "🧄 Garlic and onions (sulfur compounds)",
                "🫘 Legumes (fiber, folate, plant protein)",
            ],
            "avoid": [
                "🥩 Red and processed meats",
                "🍷 Alcohol",
                "🧈 Saturated fats",
                "🍭 High-sugar foods",
                "🥡 Ultra-processed foods",
            ]
        },
        "exercises": [
            {"name": "Walking", "duration": "20-30 min, daily", "benefit": "Maintains energy during treatment", "icon": "🚶‍♀️"},
            {"name": "Gentle Yoga", "duration": "30 min, 3x/week", "benefit": "Reduces nausea and anxiety", "icon": "🧘‍♀️"},
            {"name": "Aquatic Therapy", "duration": "30 min, 2x/week", "benefit": "Rebuilds strength gently", "icon": "🏊‍♀️"},
            {"name": "Stretching", "duration": "15 min, daily", "benefit": "Improves flexibility and reduces pain", "icon": "🙆‍♀️"},
            {"name": "Chair Exercises", "duration": "20 min, daily", "benefit": "Builds strength without strain", "icon": "🪑"},
        ],
        "color": "#F59E0B"
    },
    "Lupus (SLE)": {
        "emoji": "🦋",
        "category": "Autoimmune",
        "description": "A systemic autoimmune disease where the immune system attacks its own tissues. Women are 9x more likely to develop lupus than men.",
        "symptoms": ["Butterfly rash", "Joint pain", "Fatigue", "Photosensitivity", "Kidney issues", "Hair loss"],
        "diet": {
            "eat": [
                "🐟 Omega-3 fish (salmon, sardines, mackerel)",
                "🫐 Antioxidant berries",
                "🥬 Dark leafy greens",
                "🫚 Olive oil (anti-inflammatory)",
                "🍵 Green tea",
                "🥜 Walnuts and flaxseeds",
            ],
            "avoid": [
                "🌞 Alfalfa sprouts (can trigger flares)",
                "🧄 Garlic in large amounts",
                "🍷 Alcohol",
                "☕ Excessive caffeine",
                "🧂 High-sodium foods",
            ]
        },
        "exercises": [
            {"name": "Water Aerobics", "duration": "30 min, 3x/week", "benefit": "Joint-friendly, reduces inflammation", "icon": "🏊‍♀️"},
            {"name": "Yoga (Gentle)", "duration": "40 min, 3x/week", "benefit": "Reduces fatigue and joint pain", "icon": "🧘‍♀️"},
            {"name": "Walking", "duration": "20-30 min, daily", "benefit": "Maintains cardiovascular health", "icon": "🚶‍♀️"},
            {"name": "Pilates", "duration": "30 min, 2x/week", "benefit": "Strengthens without overexertion", "icon": "🤸‍♀️"},
            {"name": "Stretching", "duration": "15 min, daily", "benefit": "Maintains joint flexibility", "icon": "🙆‍♀️"},
        ],
        "color": "#A855F7"
    },
    "Anemia (Iron-Deficiency)": {
        "emoji": "💉",
        "category": "Blood",
        "description": "Very common in women due to menstruation. Occurs when the body lacks enough iron to produce sufficient red blood cells.",
        "symptoms": ["Fatigue and weakness", "Pale skin", "Shortness of breath", "Dizziness", "Cold hands/feet", "Brittle nails"],
        "diet": {
            "eat": [
                "🥩 Lean red meat (heme iron, highly absorbable)",
                "🫘 Legumes (lentils, chickpeas, beans)",
                "🥬 Dark leafy greens (spinach, kale)",
                "🌾 Iron-fortified cereals and grains",
                "🍊 Vitamin C with iron foods (boosts absorption)",
                "🥜 Pumpkin seeds and sesame seeds",
            ],
            "avoid": [
                "☕ Coffee and tea with meals (inhibit iron absorption)",
                "🥛 Calcium-rich foods with iron-rich meals",
                "🌾 Phytate-rich foods in excess",
                "🍫 Processed foods low in iron",
                "🥤 Carbonated drinks during meals",
            ]
        },
        "exercises": [
            {"name": "Gentle Walking", "duration": "20-30 min, daily", "benefit": "Improves oxygen circulation", "icon": "🚶‍♀️"},
            {"name": "Yoga (Breathing)", "duration": "30 min, 3x/week", "benefit": "Enhances oxygen intake", "icon": "🧘‍♀️"},
            {"name": "Light Cycling", "duration": "15-20 min, 3x/week", "benefit": "Boosts energy gradually", "icon": "🚴‍♀️"},
            {"name": "Swimming", "duration": "20 min, 2x/week", "benefit": "Low-impact cardio for energy", "icon": "🏊‍♀️"},
            {"name": "Stretching", "duration": "15 min, daily", "benefit": "Reduces fatigue and stiffness", "icon": "🙆‍♀️"},
        ],
        "color": "#EF4444"
    },
    "Anxiety & Depression": {
        "emoji": "🧠",
        "category": "Mental Health",
        "description": "Women are twice as likely as men to experience anxiety and depression. Hormonal fluctuations, life transitions, and societal pressures contribute significantly.",
        "symptoms": ["Persistent worry", "Low mood", "Sleep disturbances", "Loss of interest", "Fatigue", "Physical aches"],
        "diet": {
            "eat": [
                "🐟 Omega-3 fatty acids (brain-boosting)",
                "🍫 Dark chocolate (serotonin boost, 70%+)",
                "🥦 Leafy greens (folate for mood)",
                "🥚 Eggs (tryptophan for serotonin)",
                "🫐 Berries (antioxidants for brain health)",
                "🥣 Fermented foods (gut-brain connection)",
            ],
            "avoid": [
                "☕ Excess caffeine (worsens anxiety)",
                "🍷 Alcohol (depressant, disrupts sleep)",
                "🍭 Sugar and processed foods (mood crashes)",
                "🥡 Ultra-processed fast food",
                "🧂 High-sodium processed snacks",
            ]
        },
        "exercises": [
            {"name": "Running/Jogging", "duration": "30 min, 3-5x/week", "benefit": "Releases endorphins, the 'happy hormones'", "icon": "🏃‍♀️"},
            {"name": "Yoga", "duration": "45 min, daily", "benefit": "Reduces cortisol, induces calm", "icon": "🧘‍♀️"},
            {"name": "Dancing", "duration": "30 min, 3x/week", "benefit": "Social, joyful, boosts dopamine", "icon": "💃"},
            {"name": "Walking in Nature", "duration": "30-60 min, daily", "benefit": "Nature exposure reduces anxiety", "icon": "🌿"},
            {"name": "Group Classes", "duration": "1 hr, 2-3x/week", "benefit": "Social connection fights isolation", "icon": "👯‍♀️"},
        ],
        "color": "#06B6D4"
    },
}

# ─── Main Application ──────────────────────────────────────────────────────────
class WomensHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Women's Health Guide — Diet & Exercise Advisor")
        self.geometry("1280x820")
        self.configure(fg_color=COLORS["bg_deep"])
        self.minsize(900, 650)

        self.current_disease = None
        self.search_results = list(DISEASES_DB.keys())
        self.active_tab = tk.StringVar(value="diet")
        self.category_filter = tk.StringVar(value="All")

        self._build_ui()
        self._populate_disease_list(self.search_results)

    # ── Build UI ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        self._build_header()

        # Main content area (sidebar + detail panel)
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # Left sidebar
        self._build_sidebar(content)

        # Right detail panel
        self._build_detail_panel(content)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_panel"],
                               corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo / title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=24, pady=12)

        logo_label = ctk.CTkLabel(title_frame, text="♀",
                                   font=ctk.CTkFont(size=36, weight="bold"),
                                   text_color=COLORS["accent_pink"])
        logo_label.pack(side="left", padx=(0, 10))

        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left")

        ctk.CTkLabel(text_frame, text="Women's Health Guide",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Disease Library · Diet & Exercise Advisor",
                     font=ctk.CTkFont(size=11),
                     text_color=COLORS["text_muted"]).pack(anchor="w")

        # Stats
        stats_frame = ctk.CTkFrame(header, fg_color="transparent")
        stats_frame.pack(side="right", padx=24)

        categories = list(set(d["category"] for d in DISEASES_DB.values()))
        for val, label in [(str(len(DISEASES_DB)), "Diseases"), (str(len(categories)), "Categories")]:
            sf = ctk.CTkFrame(stats_frame, fg_color=COLORS["bg_card"], corner_radius=10)
            sf.pack(side="left", padx=6, pady=10)
            ctk.CTkLabel(sf, text=val,
                         font=ctk.CTkFont(size=20, weight="bold"),
                         text_color=COLORS["accent_pink"]).pack(padx=14, pady=(6, 0))
            ctk.CTkLabel(sf, text=label,
                         font=ctk.CTkFont(size=9),
                         text_color=COLORS["text_muted"]).pack(padx=14, pady=(0, 6))

    def _build_sidebar(self, parent):
        sidebar = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"],
                                corner_radius=16, width=290)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        sidebar.pack_propagate(False)
        sidebar.grid_propagate(False)

        # Search
        search_frame = ctk.CTkFrame(sidebar, fg_color=COLORS["bg_card"], corner_radius=12)
        search_frame.pack(fill="x", padx=14, pady=(14, 8))

        ctk.CTkLabel(search_frame, text="🔍  Search Disease",
                     font=ctk.CTkFont(size=11),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=12, pady=(8, 4))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = ctk.CTkEntry(search_frame,
                                     textvariable=self.search_var,
                                     placeholder_text="Type to search...",
                                     fg_color=COLORS["bg_deep"],
                                     border_color=COLORS["border"],
                                     text_color=COLORS["text_primary"],
                                     font=ctk.CTkFont(size=13),
                                     height=36)
        search_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Category filter
        categories = ["All"] + sorted(set(d["category"] for d in DISEASES_DB.values()))
        ctk.CTkLabel(sidebar, text="FILTER BY CATEGORY",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=16, pady=(4, 4))

        cat_scroll = ctk.CTkScrollableFrame(sidebar, fg_color="transparent",
                                             height=50, orientation="horizontal")
        cat_scroll.pack(fill="x", padx=12, pady=(0, 6))

        self.cat_buttons = {}
        for cat in categories:
            btn = ctk.CTkButton(cat_scroll, text=cat,
                                 fg_color=COLORS["accent_pink"] if cat == "All" else COLORS["bg_card"],
                                 text_color=COLORS["text_primary"],
                                 hover_color=COLORS["accent_purple"],
                                 corner_radius=20, height=26,
                                 font=ctk.CTkFont(size=10),
                                 command=lambda c=cat: self._filter_category(c))
            btn.pack(side="left", padx=3)
            self.cat_buttons[cat] = btn

        # Disease count
        self.count_label = ctk.CTkLabel(sidebar,
                                         text=f"Showing {len(DISEASES_DB)} conditions",
                                         font=ctk.CTkFont(size=10),
                                         text_color=COLORS["text_muted"])
        self.count_label.pack(anchor="w", padx=16, pady=(2, 4))

        # Disease list
        self.disease_list_frame = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent", label_text="")
        self.disease_list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _build_detail_panel(self, parent):
        self.detail_panel = ctk.CTkFrame(parent, fg_color=COLORS["bg_panel"], corner_radius=16)
        self.detail_panel.grid(row=0, column=1, sticky="nsew")

        # Welcome screen
        self._show_welcome()

    def _show_welcome(self):
        for w in self.detail_panel.winfo_children():
            w.destroy()

        welcome = ctk.CTkFrame(self.detail_panel, fg_color="transparent")
        welcome.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(welcome, text="♀",
                     font=ctk.CTkFont(size=80),
                     text_color=COLORS["accent_pink"]).pack()
        ctk.CTkLabel(welcome, text="Women's Health Advisor",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=COLORS["text_primary"]).pack(pady=(10, 4))
        ctk.CTkLabel(welcome,
                     text="Select a disease from the left panel to explore\ndiet recommendations and beneficial exercises.",
                     font=ctk.CTkFont(size=14),
                     text_color=COLORS["text_muted"],
                     justify="center").pack()

        # Quick stats
        stats_row = ctk.CTkFrame(welcome, fg_color="transparent")
        stats_row.pack(pady=24)
        items = [("12", "Conditions"), ("5+", "Exercises each"), ("Personalised", "Diet Plans")]
        for val, lbl in items:
            sf = ctk.CTkFrame(stats_row, fg_color=COLORS["bg_card"], corner_radius=12)
            sf.pack(side="left", padx=10)
            ctk.CTkLabel(sf, text=val,
                         font=ctk.CTkFont(size=24, weight="bold"),
                         text_color=COLORS["accent_pink"]).pack(padx=20, pady=(10, 0))
            ctk.CTkLabel(sf, text=lbl,
                         font=ctk.CTkFont(size=10),
                         text_color=COLORS["text_muted"]).pack(padx=20, pady=(0, 10))

    # ── Disease List ───────────────────────────────────────────────────────────
    def _populate_disease_list(self, diseases):
        for w in self.disease_list_frame.winfo_children():
            w.destroy()

        for name in diseases:
            data = DISEASES_DB[name]
            self._create_disease_card(name, data)

    def _create_disease_card(self, name, data):
        card = ctk.CTkFrame(self.disease_list_frame,
                             fg_color=COLORS["bg_card"],
                             corner_radius=12,
                             cursor="hand2")
        card.pack(fill="x", pady=4, padx=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=8)

        # Emoji + name
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(top, text=data["emoji"],
                     font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 8))

        name_frame = ctk.CTkFrame(top, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(name_frame, text=name,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["text_primary"],
                     anchor="w").pack(anchor="w")

        # Category tag
        cat_label = ctk.CTkLabel(name_frame, text=data["category"],
                                  font=ctk.CTkFont(size=9),
                                  text_color=data["color"],
                                  anchor="w")
        cat_label.pack(anchor="w")

        # Bind clicks
        for widget in [card, inner, top, name_frame]:
            widget.bind("<Button-1>", lambda e, n=name: self._show_disease(n))
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=COLORS["bg_panel"]))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=COLORS["bg_card"]))

    # ── Disease Detail ─────────────────────────────────────────────────────────
    def _show_disease(self, name):
        self.current_disease = name
        data = DISEASES_DB[name]

        for w in self.detail_panel.winfo_children():
            w.destroy()

        # Scrollable content
        scroll = ctk.CTkScrollableFrame(self.detail_panel, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=2, pady=2)

        # ── Hero section
        hero = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=14)
        hero.pack(fill="x", padx=12, pady=(12, 8))

        hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
        hero_inner.pack(fill="x", padx=20, pady=16)

        # Title row
        title_row = ctk.CTkFrame(hero_inner, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(title_row, text=data["emoji"],
                     font=ctk.CTkFont(size=44)).pack(side="left", padx=(0, 14))

        title_text = ctk.CTkFrame(title_row, fg_color="transparent")
        title_text.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(title_text, text=name,
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLORS["text_primary"],
                     anchor="w").pack(anchor="w")

        cat_badge = ctk.CTkFrame(title_text, fg_color=COLORS["tag_bg"], corner_radius=20)
        cat_badge.pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(cat_badge, text=f"  {data['category']}  ",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=data["color"]).pack(padx=6, pady=2)

        # Description
        ctk.CTkLabel(hero_inner, text=data["description"],
                     font=ctk.CTkFont(size=13),
                     text_color=COLORS["text_muted"],
                     wraplength=700,
                     justify="left",
                     anchor="w").pack(anchor="w", pady=(12, 0))

        # Symptoms
        sym_frame = ctk.CTkFrame(hero_inner, fg_color=COLORS["bg_panel"], corner_radius=10)
        sym_frame.pack(fill="x", pady=(12, 0))

        ctk.CTkLabel(sym_frame, text="⚠  Common Symptoms",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLORS["accent_gold"]).pack(anchor="w", padx=14, pady=(10, 6))

        sym_row = ctk.CTkFrame(sym_frame, fg_color="transparent")
        sym_row.pack(fill="x", padx=14, pady=(0, 10))

        for sym in data["symptoms"]:
            tag = ctk.CTkFrame(sym_row, fg_color=COLORS["bg_card"], corner_radius=14)
            tag.pack(side="left", padx=4, pady=2)
            ctk.CTkLabel(tag, text=f"• {sym}",
                         font=ctk.CTkFont(size=10),
                         text_color=COLORS["text_primary"]).pack(padx=10, pady=4)

        # ── Tab buttons
        tab_row = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_row.pack(fill="x", padx=12, pady=8)

        self.tab_diet_btn = ctk.CTkButton(tab_row, text="🥗  Diet & Nutrition",
                                           fg_color=COLORS["accent_pink"],
                                           hover_color=COLORS["accent_purple"],
                                           text_color="white",
                                           font=ctk.CTkFont(size=13, weight="bold"),
                                           corner_radius=10, height=40,
                                           command=lambda: self._switch_tab("diet", tab_content))
        self.tab_diet_btn.pack(side="left", padx=(0, 8))

        self.tab_ex_btn = ctk.CTkButton(tab_row, text="💪  Exercises",
                                         fg_color=COLORS["bg_card"],
                                         hover_color=COLORS["accent_purple"],
                                         text_color=COLORS["text_muted"],
                                         font=ctk.CTkFont(size=13),
                                         corner_radius=10, height=40,
                                         command=lambda: self._switch_tab("exercise", tab_content))
        self.tab_ex_btn.pack(side="left")

        # ── Tab content
        tab_content = ctk.CTkFrame(scroll, fg_color="transparent")
        tab_content.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._show_diet_tab(tab_content, data)

    def _switch_tab(self, tab, container):
        for w in container.winfo_children():
            w.destroy()
        if tab == "diet":
            self.tab_diet_btn.configure(fg_color=COLORS["accent_pink"],
                                         text_color="white",
                                         font=ctk.CTkFont(size=13, weight="bold"))
            self.tab_ex_btn.configure(fg_color=COLORS["bg_card"],
                                       text_color=COLORS["text_muted"],
                                       font=ctk.CTkFont(size=13))
            self._show_diet_tab(container, DISEASES_DB[self.current_disease])
        else:
            self.tab_ex_btn.configure(fg_color=COLORS["accent_pink"],
                                       text_color="white",
                                       font=ctk.CTkFont(size=13, weight="bold"))
            self.tab_diet_btn.configure(fg_color=COLORS["bg_card"],
                                         text_color=COLORS["text_muted"],
                                         font=ctk.CTkFont(size=13))
            self._show_exercise_tab(container, DISEASES_DB[self.current_disease])

    def _show_diet_tab(self, parent, data):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="both", expand=True)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        # Foods to Eat
        eat_card = ctk.CTkFrame(row, fg_color=COLORS["bg_card"], corner_radius=14)
        eat_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)

        ctk.CTkLabel(eat_card, text="✅  Foods to Eat",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["success"]).pack(anchor="w", padx=16, pady=(14, 8))

        for food in data["diet"]["eat"]:
            item = ctk.CTkFrame(eat_card, fg_color=COLORS["bg_panel"], corner_radius=8)
            item.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(item, text=food,
                         font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_primary"],
                         anchor="w",
                         wraplength=250).pack(anchor="w", padx=12, pady=7)

        # Foods to Avoid
        avoid_card = ctk.CTkFrame(row, fg_color=COLORS["bg_card"], corner_radius=14)
        avoid_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)

        ctk.CTkLabel(avoid_card, text="❌  Foods to Avoid",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#EF4444").pack(anchor="w", padx=16, pady=(14, 8))

        for food in data["diet"]["avoid"]:
            item = ctk.CTkFrame(avoid_card, fg_color=COLORS["bg_panel"], corner_radius=8)
            item.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(item, text=food,
                         font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_primary"],
                         anchor="w",
                         wraplength=250).pack(anchor="w", padx=12, pady=7)

    def _show_exercise_tab(self, parent, data):
        ctk.CTkLabel(parent, text="💪  Recommended Exercises",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLORS["text_primary"]).pack(anchor="w", pady=(8, 12))

        for i, ex in enumerate(data["exercises"]):
            self._create_exercise_card(parent, ex, i)

    def _create_exercise_card(self, parent, ex, index):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=14)
        card.pack(fill="x", pady=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        # Number badge
        badge = ctk.CTkFrame(inner, fg_color=COLORS["accent_pink"],
                              corner_radius=20, width=36, height=36)
        badge.pack(side="left", padx=(0, 14))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text=str(index + 1),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Content
        content = ctk.CTkFrame(inner, fg_color="transparent")
        content.pack(side="left", fill="x", expand=True)

        name_row = ctk.CTkFrame(content, fg_color="transparent")
        name_row.pack(fill="x")

        ctk.CTkLabel(name_row, text=f"{ex['icon']}  {ex['name']}",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["text_primary"]).pack(side="left")

        # Duration tag
        dur_badge = ctk.CTkFrame(name_row, fg_color=COLORS["tag_bg"], corner_radius=10)
        dur_badge.pack(side="left", padx=10)
        ctk.CTkLabel(dur_badge, text=f"⏱  {ex['duration']}",
                     font=ctk.CTkFont(size=10),
                     text_color=COLORS["accent_teal"]).pack(padx=8, pady=3)

        ctk.CTkLabel(content, text=f"✦  {ex['benefit']}",
                     font=ctk.CTkFont(size=12),
                     text_color=COLORS["text_muted"],
                     anchor="w").pack(anchor="w", pady=(4, 0))

    # ── Search & Filter ────────────────────────────────────────────────────────
    def _on_search(self, *args):
        query = self.search_var.get().lower().strip()
        category = self.category_filter.get()

        results = []
        for name, data in DISEASES_DB.items():
            cat_match = category == "All" or data["category"] == category
            text_match = (not query or
                          query in name.lower() or
                          query in data["category"].lower() or
                          query in data["description"].lower() or
                          any(query in s.lower() for s in data["symptoms"]))
            if cat_match and text_match:
                results.append(name)

        self.count_label.configure(text=f"Showing {len(results)} condition{'s' if len(results) != 1 else ''}")
        self._populate_disease_list(results)

    def _filter_category(self, category):
        self.category_filter.set(category)
        for cat, btn in self.cat_buttons.items():
            btn.configure(
                fg_color=COLORS["accent_pink"] if cat == category else COLORS["bg_card"],
                text_color=COLORS["text_primary"] if cat == category else COLORS["text_muted"]
            )
        self._on_search()


# ─── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = WomensHealthApp()
    app.mainloop()