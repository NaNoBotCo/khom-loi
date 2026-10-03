"""copy_text.py — every word on the page, English and Thai, written by hand.
FACTS-PENDING marks the lines that wait on research/facts.md."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# release places: name, lat, lng
SITES = [
    {"en": "Tha Phae Gate", "th": "ประตูท่าแพ", "lat": 18.7877, "lng": 98.9932},
    {"en": "Near Mae Jo, San Sai", "th": "ใกล้แม่โจ้ สันทราย", "lat": 18.8960, "lng": 99.0120},
]


def _airport_km(lat, lng):
    """distance from a place to the middle of Chiang Mai's runway, from map.json"""
    m = json.load(open(os.path.join(HERE, "..", "docs", "map.json")))
    best = 1e9
    for a, b, c, d in m["runways"]:
        if abs(a - 18.77) > 0.05 or abs(b - 98.96) > 0.05:
            continue
        for la, ln in ((a, b), (c, d), ((a + c) / 2, (b + d) / 2)):
            dx = (ln - lng) * math.cos(math.radians(18.79)) * 111.32
            dy = (la - lat) * 110.54
            best = min(best, math.hypot(dx, dy))
    return best


AIR_KM = _airport_km(SITES[0]["lat"], SITES[0]["lng"])

UI = {"en": {}, "th": {}}

UI["en"].update({
    "title": "Khom Loi, Drawn", "other_title": "โคมลอย วาดด้วยคณิต",
    "desc": "Why a Yi Peng sky lantern rises, how high and how long it flies, and where the wind brings it down over Chiang Mai, drawn with the physics of hot air.",
    "card_alt": "Paper lanterns rising over the Ping River under a full moon, drawn with math",
    "hero_alt": "A night sky over Chiang Mai with paper lanterns rising, each one flying by the page's physics",
    "kicker": "Yi Peng · Chiang Mai",
    "lede": "Paper, a bamboo hoop, a ring of fuel and a little fire. Why it goes up, how high, for how long, and where it comes down: every lantern on this page flies by the same sums.",
    "hint": "Tap the sky to send one up.",
    "cardline": "Why it rises, how high it flies, where it lands",
    "nav_label": "Sections",
    "nav": [("what", "What it is"), ("lift", "Why it rises"), ("flight", "One flight"), ("drift", "Where it lands"), ("sky", "How many"), ("yipeng", "Yi Peng 2026"), ("words", "Words"), ("sources", "Sources")],
    "lang_this": "EN", "lang_other": "ไทย",
    "lift_kick": "Why it rises", "lift_h": "Hot air is thin air",
    "lift_p": [
        "Air is tiny bits bumping around. Heat them and they bump harder and spread out, so the same space holds fewer of them. A lantern full of hot air holds less air, by weight, than the same space of cool night air.",
        "The lantern goes up when the night air it pushes aside weighs more than the hot air inside plus the paper, the hoop and the fuel. The difference is the lift.",
    ],
    "lift_eq": "lift = V × (ρ<sub>night</sub> − ρ<sub>inside</sub>) &nbsp;&nbsp; ρ = p ÷ (R × T)",
    "l_ti": "Inside the lantern", "l_ta": "The night", "l_h": "Lantern height",
    "l_lift": "Lift", "l_weight": "Weight", "l_rho": "Air, kg per m³ (night / inside)",
    "l_out": "night air", "l_in": "hot air inside",
    "spare": "to spare", "short": "short",
    "l_hot": "Paper near the flame chars at around 230 °C.",
    "lift_note": "The lantern drawn here is a paper drum, 62% as wide at the mouth as it is tall and a little wider at the top: 22 g/m² paper, a 12 g hoop, 25 g of fuel. T in the sum is in kelvin, °C + 273. V is the lantern's volume, p the air pressure, R the gas constant for air, 287 J/(kg·K).",
    "fl_kick": "One flight", "fl_h": "Up while it burns, down when it cools",
    "fl_p": [
        "Light the fuel and hold on. The air inside warms until the lantern tugs at your hands, and then you let go. It climbs while the fuel burns. When the fuel is gone the air inside cools in under a minute and the lantern comes down.",
    ],
    "f_fuel": "Fuel", "f_h": "Lantern height", "f_gsm": "Paper", "f_ta": "The night",
    "f_hold": "You hold it for", "f_top": "Highest", "f_aloft": "In the air", "f_hot": "Hottest inside",
    "fl_height": "height", "fl_heat": "inside temperature", "fl_burning": "fuel burning",
    "f_char": "paper chars",
    "f_never": "Too heavy: it stays in your hands",
    "fl_p2": [
        "Every quarter of a second the page works out four things: how much fuel burned, how much of its heat stayed in the air inside, how hard the night air pushes up, and how fast the lantern moves against the drag of the air. Twice the fuel flies about twice as long. A smaller lantern with the same fire runs hotter inside.",
    ],
    "fl_note": "FACTS-PENDING",
    "dr_kick": "Where it lands", "dr_h": "The wind decides",
    "dr_p": [
        "A lantern has no steering. It goes where the air goes, and the air higher up moves faster than the air by the river. Here are forty lanterns from one place, each a little different. The big ticketed releases are out near Mae Jo in San Sai.",
    ],
    "dr_site": "Let go from",
    "d_from": "Wind from", "d_speed": "Wind near the ground", "d_go": "Let 40 go",
    "d_med": "Half land within", "d_far": "Farthest", "d_air": "On the airport", "d_wat": "In the water",
    "dr_land": "came down on land", "dr_water": "in water", "dr_air": "on the airport",
    "dr_p2": [
        f"Chiang Mai's runway is {AIR_KM:.1f} km from Tha Phae Gate, as the crow flies. A lantern needs only a light wind from the east or north-east and ten minutes in the air to get there.",
    ],
    "dr_note": "Map: OpenStreetMap contributors (ODbL). The wind grows with height as (height ÷ 10 m)<sup>0.25</sup>, a usual shape on a calm night. Each lantern gets its own size, fuel and gust, and a wind up to 20° off the one you set.",
    "compass": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    "sk_kick": "A thousand lanterns", "sk_h": "How many are up at once",
    "sk_p": [
        "Let lanterns go at a steady rate and the sky fills, until the first ones start coming down. From then on the count holds: lanterns let go each minute times the minutes each one flies.",
        "Shops use the same sum, called Little's law: people in the shop = people coming in each minute × minutes each one stays.",
    ],
    "sk_eq": "up at once = λ × W",
    "s_lam": "Lanterns let go", "s_min": "For", "s_w": "Each flies (W)", "s_peak": "Most up at once", "s_total": "Let go in all",
    "sk_note": "W comes from the one-flight model above: a 1 m lantern, 30 g of fuel.",
    "sib_h": "Krathong, Drawn", "sib_p": " The same night on the river: folding the leaf, floating, and where the current takes it.",
    "words_h": "Words", "src_h": "Sources", "src_p": "Where the facts on this page come from.",
    "pic_kick": "Pictures", "pic_h": "Lanterns and the people who let them go",
    "foot": "Khom Loi, Drawn · text CC BY 4.0 · code MIT · map © OpenStreetMap contributors",
})

UI["th"].update({
    "title": "โคมลอย วาดด้วยคณิต", "other_title": "Khom Loi, Drawn",
    "desc": "ทำไมโคมลอยยี่เป็งถึงลอยขึ้น ลอยได้สูงแค่ไหน นานเท่าไร และลมพาไปตกที่ไหนในเชียงใหม่ วาดด้วยฟิสิกส์ของอากาศร้อน",
    "card_alt": "โคมลอยลอยขึ้นเหนือแม่น้ำปิงใต้พระจันทร์เต็มดวง วาดด้วยคณิต",
    "hero_alt": "ท้องฟ้ากลางคืนเหนือเชียงใหม่ มีโคมลอยลอยขึ้น ทุกดวงลอยตามฟิสิกส์ในหน้านี้",
    "kicker": "ยี่เป็ง · เชียงใหม่",
    "lede": "กระดาษ โครงไม้ไผ่ เชื้อเพลิงหนึ่งก้อน กับไฟนิดเดียว ทำไมมันลอยขึ้น ขึ้นได้สูงแค่ไหน นานเท่าไร แล้วไปตกที่ไหน โคมทุกดวงในหน้านี้ลอยด้วยสูตรเดียวกัน",
    "hint": "แตะท้องฟ้าเพื่อปล่อยโคม",
    "cardline": "ทำไมลอย ลอยสูงแค่ไหน ไปตกที่ไหน",
    "nav_label": "หัวข้อ",
    "nav": [("what", "โคมลอยคืออะไร"), ("lift", "ทำไมลอย"), ("flight", "หนึ่งเที่ยวบิน"), ("drift", "ไปตกที่ไหน"), ("sky", "กี่ดวง"), ("yipeng", "ยี่เป็ง 2569"), ("words", "คำศัพท์"), ("sources", "ที่มา")],
    "lang_this": "ไทย", "lang_other": "EN",
    "lift_kick": "ทำไมลอย", "lift_h": "อากาศร้อนคืออากาศที่บาง",
    "lift_p": [
        "อากาศคือเม็ดเล็ก ๆ ที่วิ่งชนกันไปมา พอร้อนขึ้นก็วิ่งแรงขึ้นและถอยห่างกัน ที่เท่าเดิมเลยมีอากาศน้อยลง โคมที่เต็มไปด้วยอากาศร้อนจึงเบากว่าอากาศเย็นตอนกลางคืนในที่เท่ากัน",
        "โคมจะลอยขึ้นเมื่ออากาศกลางคืนที่มันเบียดออกไปหนักกว่าอากาศร้อนข้างใน บวกกระดาษ โครง และเชื้อเพลิง ส่วนที่เหลือคือแรงยก",
    ],
    "lift_eq": "แรงยก = V × (ρ<sub>กลางคืน</sub> − ρ<sub>ข้างใน</sub>) &nbsp;&nbsp; ρ = p ÷ (R × T)",
    "l_ti": "ข้างในโคม", "l_ta": "อากาศกลางคืน", "l_h": "ความสูงของโคม",
    "l_lift": "แรงยก", "l_weight": "น้ำหนัก", "l_rho": "อากาศ กก. ต่อ ลบ.ม. (ข้างนอก / ข้างใน)",
    "l_out": "อากาศกลางคืน", "l_in": "อากาศร้อนข้างใน",
    "spare": "เหลือ", "short": "ขาด",
    "l_hot": "กระดาษใกล้ไฟเริ่มไหม้เกรียมที่ราว 230 °C",
    "lift_note": "โคมที่วาดตรงนี้เป็นทรงกระบอกกระดาษ ปากกว้าง 62% ของความสูง ด้านบนกว้างกว่านิดหน่อย กระดาษ 22 กรัมต่อตารางเมตร โครง 12 กรัม เชื้อเพลิง 25 กรัม ค่า T ในสูตรเป็นเคลวิน คือ °C + 273 ส่วน V คือปริมาตรโคม p คือความดันอากาศ R คือค่าคงที่ของอากาศ 287 J/(kg·K)",
    "fl_kick": "หนึ่งเที่ยวบิน", "fl_h": "ขึ้นตอนไฟติด ลงตอนอากาศเย็น",
    "fl_p": [
        "จุดเชื้อเพลิงแล้วจับไว้ อากาศข้างในร้อนขึ้นจนโคมดึงมือ แล้วค่อยปล่อย มันลอยขึ้นไปตลอดเวลาที่ไฟยังไหม้ พอเชื้อเพลิงหมด อากาศข้างในเย็นลงในไม่ถึงนาที แล้วโคมก็ตกลงมา",
    ],
    "f_fuel": "เชื้อเพลิง", "f_h": "ความสูงของโคม", "f_gsm": "กระดาษ", "f_ta": "อากาศกลางคืน",
    "f_hold": "ต้องจับไว้", "f_top": "สูงสุด", "f_aloft": "อยู่บนฟ้า", "f_hot": "ข้างในร้อนสุด",
    "fl_height": "ความสูง", "fl_heat": "อุณหภูมิข้างใน", "fl_burning": "ช่วงไฟติด",
    "f_char": "กระดาษไหม้เกรียม",
    "f_never": "หนักเกินไป ไม่หลุดจากมือเลย",
    "fl_p2": [
        "ทุก ๆ เสี้ยววินาที หน้านี้คิดสี่อย่าง เชื้อเพลิงไหม้ไปเท่าไร ความร้อนอยู่ข้างในเท่าไร อากาศดันขึ้นแรงแค่ไหน และโคมเคลื่อนเร็วแค่ไหนเมื่อมีแรงต้านของอากาศ เชื้อเพลิงสองเท่า ลอยได้นานราวสองเท่า โคมเล็กที่ใช้ไฟเท่ากัน ข้างในจะร้อนกว่า",
    ],
    "fl_note": "FACTS-PENDING",
    "dr_kick": "ไปตกที่ไหน", "dr_h": "ลมเป็นคนเลือก",
    "dr_p": [
        "โคมลอยไม่มีพวงมาลัย ลมไปทางไหนมันก็ไปทางนั้น และลมข้างบนพัดแรงกว่าลมริมน้ำ นี่คือโคมสี่สิบดวงจากที่เดียวกัน แต่ละดวงต่างกันนิดหน่อย งานปล่อยโคมใหญ่ที่ขายบัตรอยู่แถวแม่โจ้ สันทราย",
    ],
    "dr_site": "ปล่อยจาก",
    "d_from": "ลมพัดมาจาก", "d_speed": "ลมใกล้พื้น", "d_go": "ปล่อย 40 ดวง",
    "d_med": "ครึ่งหนึ่งตกภายใน", "d_far": "ไกลสุด", "d_air": "ตกในสนามบิน", "d_wat": "ตกในน้ำ",
    "dr_land": "ตกบนพื้น", "dr_water": "ตกในน้ำ", "dr_air": "ตกในสนามบิน",
    "dr_p2": [
        f"รันเวย์สนามบินเชียงใหม่ห่างจากประตูท่าแพ {AIR_KM:.1f} กม. เป็นเส้นตรง แค่มีลมเบา ๆ จากทิศตะวันออกหรือตะวันออกเฉียงเหนือ กับโคมที่ลอยอยู่สักสิบนาที ก็ไปถึงแล้ว",
    ],
    "dr_note": "แผนที่: OpenStreetMap contributors (ODbL) ลมแรงขึ้นตามความสูงแบบ (ความสูง ÷ 10 ม.)<sup>0.25</sup> ซึ่งเป็นรูปแบบปกติของคืนที่ลมสงบ โคมแต่ละดวงมีขนาด เชื้อเพลิง และลมกระโชกของตัวเอง ทิศลมเบี่ยงได้ถึง 20° จากที่ตั้งไว้",
    "compass": ["เหนือ", "ตะวันออกเฉียงเหนือ", "ตะวันออก", "ตะวันออกเฉียงใต้", "ใต้", "ตะวันตกเฉียงใต้", "ตะวันตก", "ตะวันตกเฉียงเหนือ"],
    "sk_kick": "โคมพันดวง", "sk_h": "บนฟ้ามีกี่ดวงพร้อมกัน",
    "sk_p": [
        "ถ้าปล่อยโคมทีละนิดอย่างสม่ำเสมอ ท้องฟ้าจะค่อย ๆ เต็ม จนดวงแรก ๆ เริ่มตกลงมา จากนั้นจำนวนบนฟ้าจะคงที่ คือ จำนวนที่ปล่อยต่อนาที คูณ จำนวนนาทีที่แต่ละดวงลอยอยู่",
        "ร้านค้าใช้สูตรเดียวกัน เรียกว่ากฎของลิตเติล คนในร้าน = คนเข้าร้านต่อนาที × นาทีที่แต่ละคนอยู่ในร้าน",
    ],
    "sk_eq": "บนฟ้าพร้อมกัน = λ × W",
    "s_lam": "ปล่อยโคม", "s_min": "นาน", "s_w": "แต่ละดวงลอย (W)", "s_peak": "บนฟ้ามากสุด", "s_total": "ปล่อยทั้งหมด",
    "sk_note": "ค่า W มาจากแบบจำลองหนึ่งเที่ยวบินข้างบน โคมสูง 1 เมตร เชื้อเพลิง 30 กรัม",
    "sib_h": "กระทง วาดด้วยคณิต", "sib_p": " คืนเดียวกันบนแม่น้ำ พับใบตอง ลอยน้ำ และกระแสน้ำพาไปไหน",
    "words_h": "คำศัพท์", "src_h": "ที่มา", "src_p": "ข้อมูลในหน้านี้มาจากที่เหล่านี้",
    "pic_kick": "ภาพ", "pic_h": "โคมลอยกับคนปล่อยโคม",
    "foot": "โคมลอย วาดด้วยคณิต · ข้อความ CC BY 4.0 · โค้ด MIT · แผนที่ © OpenStreetMap contributors",
})

for lang in ("en", "th"):
    UI[lang]["sites"] = [{"name": s[lang], "lat": s["lat"], "lng": s["lng"]} for s in SITES]
    UI[lang]["map_labels"] = [
        [18.7877, 98.9932, "ประตูท่าแพ" if lang == "th" else "Tha Phae Gate"],
        [18.7668, 98.9626, "สนามบิน" if lang == "th" else "Airport"],
        [18.8035, 99.0075, "แม่น้ำปิง" if lang == "th" else "The Ping"],
    ]

# Chiang Mai University's lantern (Wattanakasiwich et al. 2022): the same sum, worked here
_P, _T, _M, _V = 96500, 300.8, 0.0287, 0.159
CMU_C = _P * _T / (_P - (_M / _V) * 287.058 * _T) - 273.15

UI["en"].update({
    "what_kick": "What it is", "what_h": "Paper, a hoop and a ball of fire",
    "what_p": [
        "A khom loi is a paper drum, closed at the top and open at the bottom, on a hoop of bamboo. Two wires cross the hoop and hold the fuel in the middle: paper or cloth soaked in wax or paraffin. A Lanna description calls the burning part the <i>luk fai</i>, ลูกไฟ, the ball of fire, and says it was once cast from <i>khi ya</i> and is now toilet paper soaked in candle wax.",
        "Thai provincial notices set the most it can be: 90 cm across, 140 cm tall, one cubic metre inside, natural materials, and at most 55 g of fuel burning for at most 8 minutes. Bigger than that, it counts as an aircraft. Chiang Mai uses the same limits.",
        "In Lanna the word is <i>waao</i>, ว่าว. Yi Peng had two kinds: <i>waao hom</i>, ว่าวฮม, filled with smoke and let go by day, and <i>waao fai</i>, ว่าวไฟ, which carries fire and goes up at night. The night one is what most people now call khom loi; the airport's notices call the day one โคมควัน, <i>khom khwan</i>, the smoke lantern.",
        "Yi Peng is the full moon of the second Lanna month, the same night as the full moon of the twelfth month in central Thailand, Loy Krathong. The government's public relations department writes that the lanterns honour Phra Ket Kaew Chulamani, the Buddha's hair relic in Tavatimsa heaven, and carry sorrow and bad luck away.",
    ],
    "lift_note": f"The lantern drawn here is a paper drum, 62% as wide at the mouth as it is tall and a little wider at the top: 22 g/m² paper, a 12 g hoop, 30 g of fuel. T in the sum is in kelvin, °C + 273; p is 96.5 kPa, the air pressure Chiang Mai University's physics lab measured; R is 287 J/(kg·K) for air. That lab lifted a 28.7 g lantern of 0.159 m³ with a tealight in 2022. The same sum says it needs {CMU_C:.1f} °C inside at the lab's 27.65 °C; they worked out 85.8 °C and measured 95.0 °C with an infrared camera.",
    "l_hot": "Hotter than about 230 °C, paper starts to char. In TU Delft's tests one lantern's top caught fire 105 seconds after lighting, with its fuel still burning.",
    "fl_note": "This flight is the page's own model, built the way TU Delft's 2017 sky-lantern model is: lift from the difference in air density, air thinning with height, fuel burning down at a steady rate, then a fall at the speed where drag matches weight. The burn rate comes from TU Delft's timed burns (100–330 s) and the 55 g, 8 minute legal limit. The share of heat kept inside and the heat lost through the paper are tuned guesses. For comparison, Dutch inspectors watched ten lanterns in 2009: 2 to 5 minutes up, 50 to 300 m high, landing 633 to 1,900 m away.",
    "dr_p2": [
        f"All of Mueang Chiang Mai and Hang Dong, and parts of Saraphi, San Sai, Mae Rim and San Pa Tong, are closed to lanterns at Loy Krathong: 39 sub-districts in 6 districts. Tha Phae Gate is on this map to show why: the runway is {AIR_KM:.1f} km away as the crow flies. A light wind from the east and a few minutes in the air are enough.",
        "The airport has counted the lanterns that came down inside its fence: 1,425 in 2013, 142 in 2014 and 59 in 2015.",
    ],
    "yp_kick": "Yi Peng 2026", "yp_h": "Two nights, set hours",
    "yp_p": ["The full moon is Tuesday 24 November 2026 at 21:53 Chiang Mai time. The Civil Aviation Authority's notice for Chiang Mai and Lamphun, published 23 July 2026, sets the hours for lanterns:"],
    "dates": [
        ("Tue 24 Nov · 10:00–12:00", "daytime; in past years, the hours for smoke lanterns"),
        ("Tue 24 Nov · 19:00–01:00", "night lanterns"),
        ("Wed 25 Nov · 19:00–01:00", "night lanterns"),
    ],
    "yp_p2": [
        "In those hours Chiang Mai airport stops flying. In 2025 it cancelled 65 flights and retimed 96 over two nights; in 2023 it cancelled 101 and retimed 59.",
        "A release needs a permit from the district chief, asked for at least 30 days ahead. Chiang Mai approved about 62,000 lanterns in 2024; requests for 2025 came to 92,313. Launching near an airport against the Air Navigation Act carries up to 5 years in prison and a 200,000 baht fine.",
        "Chiang Mai province had not posted its 2026 notice by 3 October 2026. In past years it came out in October or November.",
    ],
    "words": [
        ("โคมลอย", "khom loi", "floating lantern, the night one that carries fire"),
        ("ยี่เป็ง", "yi peng", "full moon of the second Lanna month"),
        ("ว่าวไฟ", "waao fai", "Lanna: the fire lantern, let go at night"),
        ("ว่าวฮม", "waao hom", "Lanna: the smoke lantern, let go by day"),
        ("โคมควัน", "khom khwan", "smoke lantern, today's word for waao hom"),
        ("ลูกไฟ", "luk fai", "the ball of fire: the fuel"),
        ("เชื้อเพลิง", "chuea phloeng", "fuel, the word the notices use"),
        ("ปล่อยโคม", "ploi khom", "to let a lantern go"),
        ("โคมแขวน", "khom khwaen", "hanging lantern, stays on its pole"),
        ("โคมผัด", "khom phat", "turning lantern, spun by its own flame's heat"),
        ("ผางประทีป", "phang prathip", "small clay lamps lit for Yi Peng"),
        ("พระเกศแก้วจุฬามณี", "phra ket kaeo chulamani", "the Buddha's hair relic in Tavatimsa heaven"),
    ],
})

UI["th"].update({
    "what_kick": "โคมลอยคืออะไร", "what_h": "กระดาษ ห่วงไม้ไผ่ และลูกไฟ",
    "what_p": [
        "โคมลอยคือกระดาษทรงกระบอก ปิดด้านบน เปิดด้านล่าง ติดอยู่กับห่วงไม้ไผ่ มีลวดสองเส้นขึงไขว้กลางห่วง แขวนเชื้อเพลิงไว้ตรงกลาง คือกระดาษหรือผ้าชุบขี้ผึ้งหรือพาราฟิน ตำราล้านนาเรียกส่วนที่ไหม้ว่า ลูกไฟ เล่าว่าแต่ก่อนหล่อจากขี้ย้า ปัจจุบันนิยมใช้กระดาษชำระชุบขี้ผึ้งเทียน",
        "ประกาศจังหวัดกำหนดขนาดไว้ กว้างไม่เกิน 90 ซม. สูงไม่เกิน 140 ซม. ปริมาตรข้างในไม่เกิน 1 ลูกบาศก์เมตร ทำจากวัสดุธรรมชาติ เชื้อเพลิงไม่เกิน 55 กรัม ไหม้ไม่เกิน 8 นาที ใหญ่กว่านี้นับเป็นอากาศยาน เชียงใหม่ใช้เกณฑ์เดียวกัน",
        "ภาษาล้านนาเรียกว่า ว่าว ยี่เป็งมีสองแบบ ว่าวฮม อัดควันแล้วปล่อยตอนกลางวัน กับ ว่าวไฟ มีไฟติดไปด้วย ปล่อยตอนกลางคืน แบบกลางคืนคือที่คนส่วนใหญ่ตอนนี้เรียกว่าโคมลอย ส่วนประกาศของสนามบินเรียกแบบกลางวันว่า โคมควัน",
        "ยี่เป็งคือวันเพ็ญเดือนยี่ของล้านนา ตรงกับวันเพ็ญเดือนสิบสองของภาคกลาง คือคืนลอยกระทง กรมประชาสัมพันธ์เขียนไว้ว่า การปล่อยโคมเป็นการบูชาพระเกศแก้วจุฬามณีบนสวรรค์ชั้นดาวดึงส์ และปล่อยความทุกข์และเคราะห์ร้ายให้ลอยไป",
    ],
    "lift_note": f"โคมที่วาดตรงนี้เป็นทรงกระบอกกระดาษ ปากกว้าง 62% ของความสูง ด้านบนกว้างกว่านิดหน่อย กระดาษ 22 กรัมต่อตารางเมตร โครง 12 กรัม เชื้อเพลิง 30 กรัม ค่า T ในสูตรเป็นเคลวิน คือ °C + 273 ค่า p คือ 96.5 กิโลปาสคาล ความดันอากาศที่ห้องแล็บฟิสิกส์ มหาวิทยาลัยเชียงใหม่วัดได้ R คือ 287 J/(kg·K) ของอากาศ ห้องแล็บนั้นทำให้โคมหนัก 28.7 กรัม ปริมาตร 0.159 ลบ.ม. ลอยด้วยเทียนทีไลท์ในปี 2565 สูตรเดียวกันบอกว่าต้องร้อนข้างใน {CMU_C:.1f} °C ที่อุณหภูมิห้อง 27.65 °C ทีมวิจัยคำนวณได้ 85.8 °C และวัดด้วยกล้องอินฟราเรดได้ 95.0 °C",
    "l_hot": "ร้อนเกินราว 230 °C กระดาษเริ่มไหม้เกรียม ในการทดลองของ TU Delft ยอดโคมดวงหนึ่งติดไฟหลังจุด 105 วินาที ทั้งที่เชื้อเพลิงยังไหม้อยู่",
    "fl_note": "เที่ยวบินนี้เป็นแบบจำลองของหน้านี้เอง ทำแบบเดียวกับแบบจำลองโคมลอยของ TU Delft ปี 2560 แรงยกจากความหนาแน่นอากาศที่ต่างกัน อากาศบางลงตามความสูง เชื้อเพลิงไหม้ในอัตราคงที่ แล้วตกลงด้วยความเร็วที่แรงต้านอากาศเท่ากับน้ำหนัก อัตราไหม้มาจากเวลาที่ TU Delft จับได้ (100–330 วินาที) และเกณฑ์ตามกฎหมาย 55 กรัม 8 นาที ส่วนความร้อนที่เก็บไว้ข้างในและที่หายไปทางกระดาษเป็นค่าที่ตั้งเอง เทียบดู ผู้ตรวจของเนเธอร์แลนด์ดูโคม 10 ดวงในปี 2552 ลอยอยู่ 2–5 นาที สูง 50–300 เมตร ตกห่างออกไป 633–1,900 เมตร",
    "dr_p2": [
        f"ช่วงลอยกระทง ห้ามปล่อยโคมทั้งอำเภอเมืองเชียงใหม่และหางดง และบางตำบลในสารภี สันทราย แม่ริม สันป่าตอง รวม 39 ตำบลใน 6 อำเภอ ที่ใส่ประตูท่าแพไว้ในแผนที่ก็เพื่อให้เห็นว่าทำไม รันเวย์อยู่ห่างไป {AIR_KM:.1f} กม. เป็นเส้นตรง แค่ลมเบา ๆ จากทิศตะวันออก กับโคมที่ลอยอยู่ไม่กี่นาที ก็ไปถึง",
        "สนามบินนับโคมที่ตกในรั้วสนามบินไว้ ปี 2556 มี 1,425 ดวง ปี 2557 มี 142 ดวง ปี 2558 มี 59 ดวง",
    ],
    "yp_kick": "ยี่เป็ง 2569", "yp_h": "สองคืน มีเวลากำหนด",
    "yp_p": ["พระจันทร์เต็มดวงวันอังคารที่ 24 พฤศจิกายน 2569 เวลา 21:53 น. ประกาศของสำนักงานการบินพลเรือนแห่งประเทศไทยสำหรับเชียงใหม่และลำพูน ออกเมื่อ 23 กรกฎาคม 2569 กำหนดเวลาปล่อยโคมไว้ดังนี้"],
    "dates": [
        ("อ. 24 พ.ย. · 10:00–12:00", "ช่วงกลางวัน ปีก่อน ๆ เป็นเวลาปล่อยโคมควัน"),
        ("อ. 24 พ.ย. · 19:00–01:00", "โคมลอยกลางคืน"),
        ("พ. 25 พ.ย. · 19:00–01:00", "โคมลอยกลางคืน"),
    ],
    "yp_p2": [
        "ในช่วงเวลานี้สนามบินเชียงใหม่งดบิน ปี 2568 ยกเลิก 65 เที่ยว เลื่อนเวลา 96 เที่ยว ในสองคืน ปี 2566 ยกเลิก 101 เที่ยว เลื่อน 59 เที่ยว",
        "จะปล่อยโคมต้องขออนุญาตนายอำเภอล่วงหน้าอย่างน้อย 30 วัน ปี 2567 เชียงใหม่อนุญาตราว 62,000 ดวง ปี 2568 มีคนขอ 92,313 ดวง ปล่อยใกล้สนามบินผิดพระราชบัญญัติการเดินอากาศ โทษจำคุกถึง 5 ปี ปรับถึง 200,000 บาท",
        "ถึงวันที่ 3 ตุลาคม 2569 จังหวัดเชียงใหม่ยังไม่ออกประกาศของปีนี้ ปีก่อน ๆ ออกในเดือนตุลาคมหรือพฤศจิกายน",
    ],
    "words": [
        ("โคมลอย", "khom loi", "โคมที่ลอยขึ้นฟ้า แบบกลางคืนที่มีไฟ"),
        ("ยี่เป็ง", "yi peng", "วันเพ็ญเดือนยี่ของล้านนา"),
        ("ว่าวไฟ", "waao fai", "คำล้านนา โคมมีไฟ ปล่อยกลางคืน"),
        ("ว่าวฮม", "waao hom", "คำล้านนา โคมอัดควัน ปล่อยกลางวัน"),
        ("โคมควัน", "khom khwan", "คำที่ใช้ตอนนี้แทนว่าวฮม"),
        ("ลูกไฟ", "luk fai", "เชื้อเพลิงที่แขวนไว้กลางห่วง"),
        ("เชื้อเพลิง", "chuea phloeng", "คำที่ประกาศราชการใช้"),
        ("ปล่อยโคม", "ploi khom", "ปล่อยโคมขึ้นฟ้า"),
        ("โคมแขวน", "khom khwaen", "โคมที่แขวนไว้กับเสา ไม่ลอย"),
        ("โคมผัด", "khom phat", "โคมที่หมุนด้วยความร้อนจากไฟของมันเอง"),
        ("ผางประทีป", "phang prathip", "ถ้วยดินเผาจุดไฟในวันยี่เป็ง"),
        ("พระเกศแก้วจุฬามณี", "phra ket kaeo chulamani", "พระเกศาธาตุบนสวรรค์ชั้นดาวดึงส์"),
    ],
})

PHOTOS = json.load(open(os.path.join(HERE, "photos.json")))
SOURCES = [
    ("Royal Gazette, Samut Sakhon province notice on lanterns (size and fuel limits), 14 Nov 2016", "https://ratchakitcha.soc.go.th/documents/2089971.pdf"),
    ("MGR Online, Chiang Mai lantern limits and banned districts, 18 Oct 2023", "https://mgronline.com/local/detail/9660000094022"),
    ("Civil Aviation Authority of Thailand, AIP SUP A 27/26, Chiang Mai lantern hours, 24–25 Nov 2026", "https://aip.caat.or.th/2026-11-24/html/eSUP/VT-eSUP-26-27-A-en-GB.html"),
    ("US Naval Observatory, moon phases 2026", "https://aa.usno.navy.mil/api/moon/phases/year?year=2026"),
    ("Wattanakasiwich, Kongkhumbod & Pussadee, Heating up a lantern with a tealight candle, Revista Mexicana de Física E 19, 2022 (Chiang Mai University)", "https://doi.org/10.31349/RevMexFisE.19.010206"),
    ("Schuurman & Gransden, Sky Lantern Safety Flight Profile for Risk Assessment, AIAA 2017-3289 (TU Delft)", "https://repository.tudelft.nl/file/File_b7cf8f82-8735-4a86-acdd-2c99d78d77ee"),
    ("TU Delft Aerospace Engineering, Fiery romance: a risk model for sky lanterns", "https://www.tudelft.nl/en/ae/research/spotlight/fiery-romance-a-risk-model-for-sky-lanterns/"),
    ("Payap University Library, ประเพณียี่เป็ง (Lanna custom sheet)", "https://library.payap.ac.th/webin/NTIC/Lanna%20custom/word/pd00012.pdf"),
    ("กรมประชาสัมพันธ์ (Government Public Relations Department), ยี่เป็ง, 13 Jun 2026", "https://www.prd.go.th/th/content/category/detail/id/31/iid/510215"),
    ("ศิลปวัฒนธรรม, why Lanna's second month is central Thailand's twelfth, 11 Nov 2019", "https://www.silpa-mag.com/culture/article_4146"),
    ("Airports of Thailand, press release 89/2567 on lanterns and the Air Navigation Act, 11 Nov 2024", "https://motwebservice.mot.go.th/motpublichearing/uploads/19-11-24_3439_89_2567%20AOT%20ย้ำเตือนอันตรายจากการปล่อยโคม.pdf"),
    ("Thai PBS, Chiang Mai approves 62,000 lanterns, 12 Nov 2024", "https://www.thaipbs.or.th/news/content/346239"),
    ("Prachachat Turakij, Yi Peng 2025 figures, 23 Nov 2025", "https://www.prachachat.net/economic/local-economy/news-1924154"),
    ("Thansettakij, Chiang Mai airport flight changes for Yi Peng 2025, 1 Nov 2025", "https://www.thansettakij.com/business/tourism/642928"),
    ("The Nation via Asia News Network, 160 Chiang Mai flights cancelled or rescheduled, 24 Nov 2023", "https://asianews.network/160-chiang-mai-flights-cancelled-or-rescheduled-to-avoid-flaming-lanterns"),
    ("Matichon, lanterns collected inside Chiang Mai airport 2013–2015, 9 Nov 2016", "https://www.matichon.co.th/local/news_354114"),
    ("OpenStreetMap contributors (ODbL), map data via Protomaps", "https://www.openstreetmap.org/copyright"),
]
