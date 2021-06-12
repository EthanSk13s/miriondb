function toggleArt(id) {
    var header = document.getElementById(`card-${id}`);
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

    var card_image = document.getElementById(`card-image-${id}`);
    changeArt(card_image, `${header.getAttribute('data-awaken')}_`, 6);

    var bg_image = document.getElementById(`bg-art-${id}`);
    if (bg_image !== null) {
        changeArt(bg_image, `${header.getAttribute('data-awaken')}.`, 4);
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
        changeValues(id, inputValue.value, limit);

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

function changeValues(id, value, limit) {
    var stats = ["vo", "da", "vi"];
    var isAwaken = checkifAwakened(id);

    for (var i = 0; i < stats.length; i++) {
        var stat = document.getElementById(`${stats[i]}-${id}`);
        if (isAwaken == false) {
            var min = Number(stat.getAttribute("data-default"));
            var max = Number(stat.getAttribute("data-default-max"));
        } else {
            var min = Number(stat.getAttribute("data-awaken"));
            var max = Number(stat.getAttribute("data-awaken-max"));
        }

        stat.textContent = interpolate(value, 1, limit, min, max);
        stat.setAttribute("data-level", value.toString());
    };
}

function checkifAwakened(id) {
    var isAwaken = document.getElementById(`card-${id}`).getAttribute('data-awaken');

    if (isAwaken == "1") {
        return true;
    } else {
        return false;
    }
}
