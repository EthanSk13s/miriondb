import re

from dataclasses import dataclass
from typing import List


@dataclass
class NameTl:
    org_name: str
    tl_name: str
    id: int

    def match_name(self, query: str) -> bool:
        try:
            match = bool(re.search(r"\A({0})|\s({0})".format(query), self.tl_name.lower()))
        except re.error:
            return False

        if match:
            return True
        else:
            return False


@dataclass
class NameList:
    names: List[NameTl]

    def find_tl_name(self, query: str) -> str:
        found = False
        name = ""
        for name in self.names:
            if found:
                break
            else:
                if name.match_name(query) is True:
                    name = name.tl_name
                    found = True

        return name

    def get_id(self, query: str) -> int:
        found = False
        id = 0

        for name in self.names:
            if found:
                break
            else:
                if name.match_name(query) is True:
                    id = name.id
                    found = True

        return id


tl_names = [
    NameTl('天海春香', 'Amami Haruka', 1),
    NameTl('如月千早', 'Kisaragi Chihaya', 2),
    NameTl('星井美希', 'Hoshii Miki', 3),
    NameTl('萩原雪歩', 'Hagiwara Yukiho', 4),
    NameTl('高槻やよい', 'Takatsuki Yayoi', 5),
    NameTl('菊地真', 'Kikuchi Makoto', 6),
    NameTl('水瀬伊織', 'Minase Iori', 7),
    NameTl('四条貴音', 'Shijou Takane', 8),
    NameTl('秋月律子', 'Akizuki Ritsuko', 9),
    NameTl('三浦あずさ', 'Miura Azusa', 10),
    NameTl('双海亜美', 'Futami Ami', 11),
    NameTl('双海真美', 'Futami Mami', 12),
    NameTl('我那覇響', 'Ganaha Hibiki', 13),
    NameTl('春日未来', 'Kasuga Mirai', 14),
    NameTl('最上静香', 'Mogami Shizuka', 15),
    NameTl('伊吹翼', 'Ibuki Tsubasa', 16),
    NameTl('田中琴葉', 'Tanaka Kotoha', 17),
    NameTl('島原エレナ', 'Shimabara Elena', 18),
    NameTl('佐竹美奈子', 'Satake Minako', 19),
    NameTl('所恵美', 'Tokoro Megumi', 20),
    NameTl('徳川まつり', 'Tokugawa Matsuri', 21),
    NameTl('箱崎星梨花', 'Hakozaki Serika', 22),
    NameTl('野々原茜', 'Nonohara Akane', 23),
    NameTl('望月杏奈', 'Mochizuki Anna', 24),
    NameTl('ロコ', 'Handa Roco', 25),
    NameTl('七尾百合子', 'Nanao Yuriko', 26),
    NameTl('高山紗代子', 'Takayama Sayoko', 27),
    NameTl('松田亜利沙', 'Matsuda Arisa', 28),
    NameTl('高坂海美', 'Kousaka Umi', 29),
    NameTl('中谷育', 'Nakatani Iku', 30),
    NameTl('天空橋朋花', 'Tenkubashi Tomoka', 31),
    NameTl('エミリー', 'Stewart Emily', 32),
    NameTl('北沢志保', 'Kitazawa Shiho', 33),
    NameTl('舞浜歩', 'Maihama Ayumu', 34),
    NameTl('木下ひなた', 'Kinoshita Hinata', 35),
    NameTl('矢吹可奈', 'Yabuki Kana', 36),
    NameTl('横山奈緒', 'Yokoyama Nao', 37),
    NameTl('二階堂千鶴', 'Nikaido Chizuru', 38),
    NameTl('馬場このみ', 'Baba Konomi', 39),
    NameTl('大神環', 'Ogami Tamaki', 40),
    NameTl('豊川風花', 'Toyokawa Fuka', 41),
    NameTl('宮尾美也', 'Miyao Miya', 42),
    NameTl('福田のり子', 'Fukuda Noriko', 43),
    NameTl('真壁瑞希', 'Makabe Mizuki', 44),
    NameTl('篠宮可憐', 'Shinomiya Karen', 45),
    NameTl('百瀬莉緒', 'Momose Rio', 46),
    NameTl('永吉昴', 'Nagayoshi Subaru', 47),
    NameTl('北上麗花', 'Kitakami Reika', 48),
    NameTl('周防桃子', 'Suou Momoko', 49),
    NameTl('ジュリア', 'Julia', 50),
    NameTl('白石紬', 'Shiraishi Tsumugi', 51),
    NameTl('桜守歌織', 'Sakuramori Kaori', 52),
    NameTl('音無小鳥', 'Otonashi Kotori', 101),
    NameTl('青羽美咲', 'Aoba Misaki', 102),
    NameTl('詩花', 'Shika', 201),
    NameTl('玲音', 'Leon', 202),
    NameTl('宮本フレデリカ', 'Miyamoto Frederica', 204),
    NameTl('一ノ瀬志希', 'Ichinose Shiki', 205)
]

NAMES = NameList(tl_names)

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
    9: "Multi-Bonus",
    10: "Overclock",
    11: "Overload",
    12: "Double Effect",
    17: "Fusion Score",
    18: "Fusion Combo"
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
    9: "of boosting combo bonus by {value[0]}% while also restoring {value[1]} life for every {evaluation2}",
    10: "of consuming {value[1]} lives, and increasing {evaluation} score by {value[0]}%",
    11: "of consuming {value[1]} lives, and increasing combo bonus by {value[0]}%",
    12: "of boosting score and combo bonuses by {value[0]}%",
    17: "that your {evaluation} score will increase by {value[0]}. When there are two or more Score Up cards in the unit, the score of {evaluation2} is increased to {value[1]}, and when there are one or more cards that are Fusion Combo, {evaluation3} is set to Perfect",
    18: "that the combo bonus will increase by {value[0]}% for 5 seconds. When there are two or more Combo Bonus cards in the unit, the skill activation rate will increase by {value[1]}%, and where are one or more cards that are Fusion Score, {evaluation3} is set to Perfect"
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


def get_rarity(query: str):
    for i in RARITIES.keys():
        rarity = RARITIES[i].lower()
        if rarity == query:
            value = i
            break
        else:
            value = False

    return value
