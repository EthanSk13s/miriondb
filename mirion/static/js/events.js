function changeBgArt(id, current_url, post_url) {
    var image = document.getElementById(`bg-art-${id}`);

    if (image.src.match(current_url)) {
        image.src = post_url;
    } else {
        image.src = current_url;
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

        inputValue.value = limit
    }
    
}

function changeValues(id, value, limit) {
    var stats = ["vo", "da", "vi"];
    for (var i = 0; i < stats.length; i++) {
        var stat = document.getElementById(`${stats[i]}-${id}`);
        var min = Number(stat.getAttribute("data-default"));
        var max = Number(stat.getAttribute("data-awaken"));

        stat.textContent = interpolate(value, 1, limit, min, max);
        stat.setAttribute("data-level", value.toString());
    };
}
