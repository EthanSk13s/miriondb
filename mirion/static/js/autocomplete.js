// Bless StackOverflow
function autocomplete(text, names) {
    var currentFocus;

    text.addEventListener("input", function(e) {
        var a, b, i, val = this.value;

        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autcomplete-list");
        a.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(a);

        for (i = 0; i < names.length; i++) {
            if (names[i].substr(0, val.length).toLowerCase() == val.toLowerCase()) {
                b = document.createElement("DIV");

                b.innerHTML = "<strong>" + names[i].substr(0, val.length) + "</strong>";
                b.innerHTML += names[i].substr(val.length)

                b.innerHTML += "<input type='hidden' value='" + names[i] + "'>";

                b.addEventListener("click", function(e) {
                    text.value = this.getElementsByTagName("input")[0].value;

                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != text) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}

var idolNames = ['Haruka', 'Chihaya', 'Miki', 'Yukiho', 'Yayoi', 'Makoto', 'Iori', 'Takane', 'Ritsuko', 'Azusa', 'Ami', 'Mami', 'Hibiki', 'Mirai', 'Shizuka', 'Tsubasa', 'Kotoha', 'Elena', 'Minako', 'Megumi', 'Matsuri', 'Serika', 'Akane', 'Anna', 'Roco', 'Yuriko', 'Sayoko', 'Arisa', 'Umi', 'Iku', 'Tomoka', 'Emily', 'Shiho', 'Ayumi', 'Hinata', 'Kana', 'Nao', 'Chizuru', 'Konomi', 'Tamaki', 'Fuka', 'Miya', 'Noriko', 'Mizuki', 'Karen', 'Rio', 'Subaru', 'Reika', 'Momoko', 'Julia', 'Tsumugi', 'Kaori', 'Shika', 'Leon', 'Frederica', 'Shiki'];

autocomplete(document.getElementById("card1"), idolNames);