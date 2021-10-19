function toggleArt(id) {
    var header = document.getElementById(`${id}`);
    var status = header.getAttribute("data-awaken");
    var level = document.getElementById(`level-input-${id}`);
    var limit = header.getAttribute("data-max-level");

    if (status == "0") {
        header.setAttribute("data-awaken", "1");
        limit = Number(limit) + 10;

    } else {
        header.setAttribute("data-awaken", "0");
        if (Number(level.value) > Number(limit)) {
            level.value = limit;
        }
    }

    var cardImage = document.getElementById(`card-image-${id}`);
    var oldImg = cardImage.src;
    cardImage.src = cardImage.getAttribute("data-awaken");
    cardImage.setAttribute("data-awaken", oldImg);

    var bgImage = document.getElementById(`bg-art-${id}`);
    if (bgImage !== null) {
        var oldBgImg = bgImage.src;
        bgImage.src = bgImage.getAttribute("data-awaken");
        bgImage.setAttribute("data-awaken", oldBgImg);
    }

    changeAllStats(id);
    changeValues(id, level.value, limit);
}

function changeArt(element, char, index) {
    element.src = replaceAt(element.src, index, char);
}

function replaceAt(str, index, char) {
    if (index > str.length - 1) return str;
    return str.substring(0, str.length - index - 1) + char + str.substring(str.length - index + 1);
}

function changeAllStats(id) {
    var stats = ["vo", "da", "vi"];

    for (var i = 0; i < stats.length; i++) {
        changeStat(id, stats[i]);
    }
}

function changeStat(id, stat_type) {
    var stat = document.getElementById(`${stat_type}-${id}`);
    var unawakened = stat.getAttribute("data-default");
    var current = stat.textContent;

    if (current == unawakened) {
        stat.textContent = stat.getAttribute("data-awaken");
    } else {
        stat.textContent = unawakened;
    }
}

function interpolate(level, min, max, y0, y1) {
    return Math.floor(y0 + ((y1 - y0) / (max - min)) * (level - min));
}

function increaseLevel(id, limit) {
    var inputValue = document.getElementById(`level-input-${id}`);
    var isAwaken = checkifAwakened(id);
    if (isAwaken === true) {
        limit = Number(limit) + 10;
    }

    if (Number(inputValue.value) != Number(limit)) {
        changeValues(id, (Number(inputValue.value) + 1), limit);

        inputValue.value = Number(inputValue.value) + 1;
    }
}

function decreaseLevel(id, limit) {
    var inputValue = document.getElementById(`level-input-${id}`);
    var isAwaken = checkifAwakened(id);
    if (isAwaken === true) {
        limit = Number(limit) + 10;
    }

    if (Number(inputValue.value) > 1) {
        changeValues(id, (Number(inputValue.value) - 1), limit)

        inputValue.value = Number(inputValue.value) - 1;
    }
}

function listenForLevel(id, limit) {
    var inputValue = document.getElementById(`level-input-${id}`);
    var isAwaken = checkifAwakened(id);
    if (isAwaken === true) {
        limit = Number(limit) + 10;
    }

    if (Number(inputValue.value) <= limit) {
        changeValues(id, Number(inputValue.value), limit);
    } else {
        changeValues(id, limit, limit);

        inputValue.value = limit;
    }
    
}

function increaseRank(id, levelLimit) {
    var rank = document.getElementById(`rank-input-${id}`);
    var limit = rank.getAttribute("data-max");
    var isAwaken = checkifAwakened(id);

    if (isAwaken === true) {
        levelLimit = Number(levelLimit) + 10;
    }

    if (rank.value != limit) {
        var level = Number(document.getElementById(`level-input-${id}`).value);
        rank.value = Number(rank.value) + 1;

        changeValues(id, level, levelLimit)
    }
}

function decreaseRank(id, levelLimit) {
    var rank = document.getElementById(`rank-input-${id}`);
    var isAwaken = checkifAwakened(id);

    if (isAwaken === true) {
        levelLimit = Number(levelLimit) + 10;
    }

    if (rank.value > 0) {
        var level = Number(document.getElementById(`level-input-${id}`).value);
        rank.value = rank.value - 1;

        changeValues(id, level, levelLimit)
    }
}

function listenForRank(id, levelLimit) {
    var rank = document.getElementById(`rank-input-${id}`);
    var limit = rank.getAttribute("data-max");
    var isAwaken = checkifAwakened(id);

    if (isAwaken === true) {
        levelLimit = Number(levelLimit) + 10;
    }

    if (rank.value <= limit) {
        var level = Number(document.getElementById(`level-input-${id}`).value);
        changeValues(id, level, levelLimit);
    } else {
        changeValues(id, levelLimit, levelLimit);

        rank.value = limit;
    }
} 

function changeValues(id, value, limit) {
    var stats = ["vo", "da", "vi"];
    var isAwaken = checkifAwakened(id);

    for (var i = 0; i < stats.length; i++) {
        var stat = document.getElementById(`${stats[i]}-${id}`);
        var rankBonus = document.getElementById(`rank-input-${id}`);

        var rankValue = rankBonus.getAttribute(`data-${stats[i]}`);

        if (isAwaken == false) {
            var min = Number(stat.getAttribute("data-default"));
            var max = Number(stat.getAttribute("data-default-max"));
        } else {
            var min = Number(stat.getAttribute("data-awaken"));
            var max = Number(stat.getAttribute("data-awaken-max"));
        }

        stat.textContent = interpolate(value, 1, limit, min, max) + calcBonus(rankBonus.value, rankValue);
        stat.setAttribute("data-level", value.toString());
    };
}

function checkifAwakened(id) {
    var isAwaken = document.getElementById(`${id}`).getAttribute('data-awaken');

    if (isAwaken == "1") {
        return true;
    } else {
        return false;
    }
}

function calcBonus(bonus, value) {
    return bonus * value;
}