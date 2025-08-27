import { IMAGE_URL } from "./consts";

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

export enum CardStatType {
    VOCAL,
    DANCE,
    VISUAL
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

    calcStatAtX(isAwaken: boolean, level: number, maxLevel: number, stat: CardStatType) {
        let result: number;
        let vocal: number = this.vocal;
        let dance: number = this.dance;
        let visual: number = this.visual;

        let maxVocal: number = this.maxVocal;
        let maxDance: number = this.maxDance;
        let maxVisual: number = this.maxVisual;

        if (isAwaken) {
            vocal = this.awakeVocal;
            dance = this.awakeDance;
            visual = this.awakeVisual;

            maxVocal = this.maxAwakeVocal;
            maxDance = this.maxAwakeDance;
            maxVisual = this.maxAwakeVisual;
        }

        switch (stat) {
            case CardStatType.VOCAL:
                result = this.interpolate(level, 1, maxLevel, vocal, maxVocal);
                break;
            case CardStatType.DANCE:
                result = this.interpolate(level, 1, maxLevel, dance, maxDance);
                break;
            case CardStatType.VISUAL:
                result = this.interpolate(level, 1, maxLevel, visual, maxVisual);
                break;
        }

        return result;
    }

    private interpolate(level: number, min: number, max: number, y0: number, y1: number) {
        return Math.floor(y0 + ((y1 - y0) / (max - min)) * (level - min));
    }
}

export class MiniCard {
    readonly name: string = "";
    readonly rescId: string = "";
    readonly id: number = 0;
    readonly idolId: number = 0;
    readonly exType: number = 0;
    readonly rarity: number = 0;
    readonly idolType: number = 0;
    readonly release: Date = new Date();
    readonly event: CardEvent | null = null;

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

            if (cardObj.event) {
                this.event = new CardEvent(cardObj.event);
            } else {
                this.event = null;
            }
        }
    }

    getIconUrl() {
        return `${IMAGE_URL}/icons/${this.rescId}_0.png`;
    }
}

export class Card extends MiniCard {
    readonly skill: Skill | null = null;
    readonly centerSkill: CenterSkill | null = null;
    readonly costumes: string[] | null = null;
    readonly stats: CardStats | null = null;

    constructor(cardObj?: any) {
        super(cardObj);
        if (cardObj) {
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

            this.stats = new CardStats(cardObj.stats);
        }
    }

    getCardImageUrl(isAwaken: boolean) {
        if (isAwaken && this.rescId) {
            return `${IMAGE_URL}/card/${this.rescId}_1.png`;
        } else {
            return `${IMAGE_URL}/card/${this.rescId}_0.png`;
        }
    }

    getCostumesUrl() {
        let urls: string[] = [];
        if (this.costumes) {
            this.costumes.forEach((costume) => {
                urls.push(`${IMAGE_URL}/costumes/${costume}.png`);
            })
        } else {
            return null;
        }

        return urls;
    }

    getBgImageUrl(isAwaken: boolean) {
        if (this.rarity == 4) {
            if (isAwaken) {
                return `${IMAGE_URL}/card_bg/${this.rescId}_1.png`;
            } else {
                return `${IMAGE_URL}/card_bg/${this.rescId}_0.png`;
            }
        } else {
            return null;
        }
    }

    calcStatAtX(isAwaken: boolean, level: number, maxLevel: number, stat: CardStatType) {
        return this.stats!.calcStatAtX(isAwaken, level, maxLevel, stat);
    }
}