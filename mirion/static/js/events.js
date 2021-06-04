function toggleArt(id) {
    var header = document.getElementById(`card-${id}`);
    var status = header.getAttribute("data-awaken");
    if (status == "0") {
        header.setAttribute("data-awaken", "1");
    } else {
        header.setAttribute("data-awaken", "0");
    }
    changeAllStats(id);

    var limit = header.getAttribute("data-max-level");
    var level = document.getElementById(`level-input-${id}`).value;

    changeValues(id, level, limit);

    var card_image = document.getElementById(`card-image-${id}`);
    changeArt(card_image);

    var bg_image = document.getElementById(`bg-art-${id}`);
    if (bg_image !== null) {
        changeArt(bg_image);
    }
}

function changeArt(element) {
    var current = element.getAttribute('data-default');
    if (element.src.match(current)) {
        element.src = element.getAttribute("data-awaken");
    } else {
        element.src = element.getAttribute("data-default");
    }
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
    if (Number(inputValue.value) != Number(limit)) {
        changeValues(id, inputValue.value, limit);

        inputValue.value = Number(inputValue.value) + 1;
    }
}

function decreaseLevel(id, limit) {
    var inputValue = document.getElementById(`level-input-${id}`);
    if (Number(inputValue.value) > 1) {
        changeValues(id, (Number(inputValue.value) - 1), limit)

        inputValue.value = Number(inputValue.value) - 1;
    }
}

function listenForLevel(id, limit) {
    var inputValue = document.getElementById(`level-input-${id}`);

    if (Number(inputValue.value) <= limit) {
        changeValues(id, Number(inputValue.value), limit);
    } else {
        changeValues(id, limit, limit);

        inputValue.value = limit;
    }
    
}

function changeValues(id, value, limit) {
    var stats = ["vo", "da", "vi"];
    var isAwaken = document.getElementById(`card-${id}`).getAttribute('data-awaken');
    for (var i = 0; i < stats.length; i++) {
        var stat = document.getElementById(`${stats[i]}-${id}`);
        if (isAwaken == "0") {
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
