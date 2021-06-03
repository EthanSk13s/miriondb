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
    var stats = ["vo", "da", "vi"];
    var levelText = document.getElementById(`lvl-${id}`);
    if (Number(levelText.textContent) != Number(limit)) {
        for (var i = 0; i < stats.length; i++) {
            var stat = document.getElementById(`${stats[i]}-${id}`);
            var level = stat.getAttribute("data-level");
            var min = Number(stat.getAttribute("data-default"));
            var max = Number(stat.getAttribute("data-awaken"));
    
            stat.textContent = interpolate((Number(level) + 1), 1, 80, min, max);
            stat.setAttribute("data-level", ((Number(level)) + 1).toString());
        };

        levelText.textContent = Number(level) + 1;
    }
}

function decreaseLevel(id) {
    var levelText = document.getElementById(`lvl-${id}`);
    if (Number(levelText.textContent) > 1) {
        var stats = ["vo", "da", "vi"];
        for (var i = 0; i < stats.length; i++) {
            var stat = document.getElementById(`${stats[i]}-${id}`);
            var level = stat.getAttribute("data-level");
            var min = Number(stat.getAttribute("data-default"));
            var max = Number(stat.getAttribute("data-awaken"));

            stat.textContent = interpolate((Number(level) - 1), 1, 80, min, max);
            stat.setAttribute("data-level", ((Number(level)) - 1).toString());
        };

        levelText.textContent = Number(level) - 1;
    }
}