class Skill {
    readonly name: string;
    readonly description: string;

    constructor(skillObj: { name: string, description: string }) {
        this.name = skillObj.name;
        this.description = skillObj.description;
    }
}

class CenterSkill {
    readonly id: number;
    readonly description: string;

    constructor(centerSkillObj: { id: number, description: string }) {
        this.id = centerSkillObj.id;
        this.description = centerSkillObj.description;
    }
}

export class CardEvent {
    readonly begin: Date = new Date();
    readonly end: Date = new Date();
    readonly eventType: number = 0;
    readonly id: number = 0;
    readonly name: string = '';

    constructor(eventObj?: any) {
        if (eventObj) {
            this.begin = new Date(eventObj.begin);
            this.end = new Date(eventObj.end);
            this.eventType = eventObj.eventType;
            this.id = eventObj.id;
            this.name = eventObj.name;
        }
    }

    getDeltaTime() {
        let now = new Date();
        let delta = this.end.valueOf() - now.valueOf();
        let result: number | boolean = false;

        if (delta > 0) {
            result = delta;
        }

        return result
    }
}

class CardStats {
    readonly life: number;
    readonly vocal: number;
    readonly dance: number;
    readonly visual: number;
    readonly awakeVocal: number;
    readonly awakeDance: number;
    readonly awakeVisual: number;
    readonly maxVocal: number;
    readonly maxDance: number;
    readonly maxVisual: number;
    readonly maxAwakeVocal: number;
    readonly maxAwakeDance: number;
    readonly maxAwakeVisual: number;
    readonly maxMasterRank: number;
    readonly vocalRankBonus: number;
    readonly danceRankBonus: number;
    readonly visualRankBonus: number;

    constructor(statsObj: any) {
        this.life = statsObj.life;
        this.vocal = statsObj.vocal;
        this.dance = statsObj.dance;
        this.visual = statsObj.visual;
        this.awakeVocal = statsObj.awakeVocal;
        this.awakeDance = statsObj.awakeDance;
        this.awakeVisual = statsObj.awakeVisual;
        this.maxVocal = statsObj.maxVocal;
        this.maxDance = statsObj.maxDance;
        this.maxVisual = statsObj.maxVisual;
        this.maxAwakeVocal = statsObj.maxAwakeVocal;
        this.maxAwakeDance = statsObj.maxAwakeDance;
        this.maxAwakeVisual = statsObj.maxAwakeVisual;
        this.maxMasterRank = statsObj.maxMasterRank;
        this.vocalRankBonus = statsObj.vocalRankBonus;
        this.danceRankBonus = statsObj.danceRankBonus;
        this.visualRankBonus = statsObj.visualRankBonus;
    }

    calcStatAtX(isAwaken: boolean, level: number, maxLevel: number, stat: "vocal" | "dance" | "visual") {
        let result: number;
        if (!isAwaken) {
            switch (stat) {
                case "vocal":
                    result = this.interpolate(level, 1, maxLevel, this.vocal, this.maxVocal);
                    break;
                case "dance":
                    result = this.interpolate(level, 1, maxLevel, this.dance, this.maxDance);
                    break;
                case "visual":
                    result = this.interpolate(level, 1, maxLevel, this.visual, this.maxVisual);
                    break;
            }
        } else {
            switch (stat) {
                case "vocal":
                    result = this.interpolate(level, 1, maxLevel, this.awakeVocal, this.maxAwakeVocal);
                    break;
                case "dance":
                    result = this.interpolate(level, 1, maxLevel, this.awakeDance, this.maxAwakeDance);
                    break;
                case "visual":
                    result = this.interpolate(level, 1, maxLevel, this.awakeVisual, this.maxAwakeVisual);
                    break;
            }
        }

        return result;
    }

    private interpolate(level: number, min: number, max: number, y0: number, y1: number) {
        return Math.floor(y0 + ((y1 - y0) / (max - min)) * (level - min));
    }
}

export class Card {
    readonly name: string = "";
    readonly rescId: string = "";
    readonly id: number = 0;
    readonly idolId: number = 0;
    readonly exType: number = 0;
    readonly rarity: number = 0;
    readonly idolType: number = 0;
    readonly release: Date = new Date();
    readonly skill: Skill | null = null;
    readonly centerSkill: CenterSkill | null = null;
    readonly costumes: string[] | null = null;
    readonly event: CardEvent | null = null;
    readonly stats: CardStats | null = null;

    constructor(cardObj?: any) {
        if (cardObj) {
            this.name = cardObj.cardName;
            this.rescId = cardObj.rescId;
            this.id = cardObj.id;
            this.idolId = cardObj.idolId;
            this.exType = cardObj.exType;
            this.rarity = cardObj.rarity;
            this.idolType = cardObj.idolType;
            this.release = new Date(cardObj.release);

            if (cardObj.skill) {
                this.skill = new Skill(cardObj.skill)
            } else {
                this.skill = null;
            }

            if (cardObj.centerSkill) {
                this.centerSkill = new CenterSkill(cardObj.centerSkill)
            } else {
                this.centerSkill = null;
            }

            if (cardObj.costumes) {
                this.costumes = cardObj.costumes;
            } else {
                this.costumes = null;
            }

            if (cardObj.event) {
                this.event = new CardEvent(cardObj.event);
            } else {
                this.event = null;
            }

            this.stats = new CardStats(cardObj.stats);
        }
    }

    getIconUrl() {
        return `https://theater.miriondb.com/icons/${this.rescId}_0.png`;
    }

    getCardImageUrl(isAwaken: boolean) {
        if (isAwaken && this.rescId) {
            return `https://theater.miriondb.com/card/${this.rescId}_1.png`;
        } else {
            return `https://theater.miriondb.com/card/${this.rescId}_0.png`;
        }
    }

    getCostumesUrl() {
        let urls: string[] = [];
        if (this.costumes) {
            this.costumes.forEach((costume) => {
                urls.push(`https://theater.miriondb.com/costumes/${costume}.png`);
            })
        } else {
            return null;
        }

        return urls;
    }

    getBgImageUrl(isAwaken: boolean) {
        if (this.rarity == 4) {
            if (isAwaken) {
                return `https://theater.miriondb.com/card_bg/${this.rescId}_1.png`;
            } else {
                return `https://theater.miriondb.com/card_bg/${this.rescId}_0.png`;
            }
        } else {
            return null;
        }
    }

    calcStatAtX(isAwaken: boolean, level: number, maxLevel: number, stat: "vocal" | "dance" | "visual") {
        return this.stats!.calcStatAtX(isAwaken, level, maxLevel, stat);
    }
}