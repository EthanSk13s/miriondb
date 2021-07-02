import re

NAMES = {
    '天海春香': {'name': 'Amami Haruka', 'id': 1},
    '如月千早': {'name': 'Kisaragi Chihaya', 'id': 2},
    '星井美希': {'name': 'Hoshii Miki', 'id': 3},
    '萩原雪歩': {'name': 'Hagiwara Yukiho', 'id': 4},
    '高槻やよい': {'name': 'Takatsuki Yayoi', 'id': 5},
    '菊地真': {'name': 'Kikuchi Makoto', 'id': 6},
    '水瀬伊織': {'name': 'Minase Iori', 'id': 7},
    '四条貴音': {'name': 'Shijou Takane', 'id': 8},
    '秋月律子': {'name': 'Akizuki Ritsuko', 'id': 9},
    '三浦あずさ': {'name': 'Miura Azusa', 'id': 10},
    '双海亜美': {'name': 'Futami Ami', 'id': 11},
    '双海真美': {'name': 'Futami Mami', 'id': 12},
    '我那覇響': {'name': 'Ganaha Hibiki', 'id': 13},
    '春日未来': {'name': 'Kasuga Mirai', 'id': 14},
    '最上静香': {'name': 'Mogami Shizuka', 'id': 15},
    '伊吹翼': {'name': 'Ibuki Tsubasa', 'id': 16},
    '田中琴葉': {'name': 'Tanaka Kotoha', 'id': 17},
    '島原エレナ': {'name': 'Shimabara Elena', 'id': 18},
    '佐竹美奈子': {'name': 'Satake Minako', 'id': 19},
    '所恵美': {'name': 'Tokoro Megumi', 'id': 20},
    '徳川まつり': {'name': 'Tokugawa Matsuri', 'id': 21},
    '箱崎星梨花': {'name': 'Hakozaki Serika', 'id': 22},
    '野々原茜': {'name': 'Nonohara Akane', 'id': 23},
    '望月杏奈': {'name': 'Mochizuki Anna', 'id': 24},
    'ロコ': {'name': 'Handa Roco', 'id': 25},
    '七尾百合子': {'name': 'Nanao Yuriko', 'id': 26},
    '高山紗代子': {'name': 'Takayama Sayoko', 'id': 27},
    '松田亜利沙': {'name': 'Matsuda Arisa', 'id': 28},
    '高坂海美': {'name': 'Kousaka Umi', 'id': 29},
    '中谷育': {'name': 'Nakatani Iku', 'id': 30},
    '天空橋朋花': {'name': 'Tenkubashi Tomoka', 'id': 31},
    'エミリー': {'name': 'Stewart Emily', 'id': 32},
    '北沢志保': {'name': 'Kitazawa Shiho', 'id': 33},
    '舞浜歩': {'name': 'Maihama Ayumu', 'id': 34},
    '木下ひなた': {'name': 'Kinoshita Hinata', 'id': 35},
    '矢吹可奈': {'name': 'Yabuki Kana', 'id': 36},
    '横山奈緒': {'name': 'Yokoyama Nao', 'id': 37},
    '二階堂千鶴': {'name': 'Nikaido Chizuru', 'id': 38},
    '馬場このみ': {'name': 'Baba Konomi', 'id': 39},
    '大神環': {'name': 'Ogami Tamaki', 'id': 40},
    '豊川風花': {'name': 'Toyokawa Fuka', 'id': 41},
    '宮尾美也': {'name': 'Miyao Miya', 'id': 42},
    '福田のり子': {'name': 'Fukuda Noriko', 'id': 43},
    '真壁瑞希': {'name': 'Makabe Mizuki', 'id': 44},
    '篠宮可憐': {'name': 'Shinomiya Karen', 'id': 45},
    '百瀬莉緒': {'name': 'Momose Rio', 'id': 46},
    '永吉昴': {'name': 'Nagayoshi Subaru', 'id': 47},
    '北上麗花': {'name': 'Kitakami Reika', 'id': 48},
    '周防桃子': {'name': 'Suou Momoko', 'id': 49},
    'ジュリア': {'name': 'Julia', 'id': 50},
    '白石紬': {'name': 'Shiraishi Tsumugi', 'id': 51},
    '桜守歌織': {'name': 'Sakuramori Kaori', 'id': 52},
    '詩花': {'name': 'Shika', 'id': 201},
    '玲音': {'name': 'Leon', 'id': 202},
    '宮本フレデリカ': {'name': 'Miyamoto Frederica', 'id': 204},
    '一ノ瀬志希': {'name': 'Ichinose Shiki', 'id': 205}
}

RARITIES = {
    1: 'N',
    2: 'R',
    3: 'SR',
    4: 'SSR'
}

TYPES = {
    1: 'princess',
    2: 'fairy',
    3: 'angel',
    4: 'all-type',
    5: 'extra'
}

ATTRIBUTES = {
    1: "vocal",
    2: "dance",
    3: "visual",
    4: "all appeal",
    5: "life",
    6: "skill rate up"
}

CENTER_SKILL_STRING = "{0} idols' {1} value is increased by {2}%"
CENTER_BOOST_STRING = "When 3 idol types are present, {1} value is increased by {2}% and skill activation is boosted by {0}% "
SONG_STRING = "If playing an {0} song, an additional {1}% is added."

SKILL_TYPES = {
    1: "Score Up",
    2: "Combo Bonus",
    3: "Life Recover",
    4: "Damage Guard",
    5: "Combo Continue",
    6: "Judgment Strengthen",
    7: "Double Boost",
    8: "Multi Up",
    10: "Overclock",
    11: "Overload",
    12: "Double Effect"
}

LEVEL_LIMITS = {
    1: 20,
    2: 40,
    3: 60,
    4: 80
}

EVALUATIONS = {
    0: None,
    1: "Perfect",
    2: "Perfect/Great",
    3: "Great",
    4: "Great/Fast/Good/Slow",
    5: "Perfect/Great/Good",
    6: "Perfect/Great/Good/Fast/Slow",
    7: "Great/Good"
}

INTERVAL_STRING = "Every {interval} seconds, there is a {probability}% chance"
DURATION_STRING = "for {duration} seconds"
EFFECTS = {
    1: "of increasing {evaluation} scores by {value[0]}%",
    2: "of increasing the combo bonus by {value[0]}%",
    3: "of recovering {value[0]} lives while hitting {evaluation}",
    4: "of not losing life",
    5: "of maintaining the combo, while hitting {evaluation}",
    6: "of converting {evaluation} into Perfect",
    7: "of increasing the {evaluation} score by {value[0]} and the combo bonus by {value[1]}%",
    8: "of increasing {evaluation} score by {value[0]}% and recovering {value[1]} life with every {evaluation2}",
    10: "of consuming {value[1]} lives, and increasing {evaluation} score by {value[0]}%",
    11: "of consuming {value[1]} lives, and increasing combo bonus by {value[0]}%",
    12: "of boosting score and combo bonuses by {value[0]}%"
}


def set_enums(card):
    card.idol_type = TYPES.get(card.idol_type)
    card.level_max = LEVEL_LIMITS.get(card.rarity)
    card.text_rarity = RARITIES.get(card.rarity)
    # Modify skill_id, because adding attributes only applies to last index
    if card.skill is not None:
        card.skill_id = SKILL_TYPES.get(card.skill.effect_id)
    else:
        card.skill_id = None


def match_name(query: str):
    for i in NAMES:
        full_name = NAMES[i]['name'].lower()
        match = bool(re.search(r"\A({0})|\s({0})".format(query), full_name))
        if match:
            name = NAMES[i]['id']
            break
        else:
            name = False

    return name


def get_rarity(query: str):
    for i in RARITIES.keys():
        rarity = RARITIES[i].lower()
        if rarity == query:
            value = i
            break
        else:
            value = False

    return value
