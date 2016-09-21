var currTimeout = 1000;
var maxTimeout = 120000;
var count = 5;

function switchem() {
    var elements = document.getElementsByTagName('*');
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        for (var j = 0; j < element.childNodes.length; j++) {
            var node = element.childNodes[j];

            if (node.nodeType === 3) {
                var text = node.nodeValue;
                var replacedText = text.replace(/(?:(?:Ernest\sOrlando\s)?Lawrence\s)?Berkeley\s(?:National\s)?Lab(?:oratory)?/,
                    'Salt Mine of Science');
                if (replacedText !== text) {
                    element.replaceChild(document.createTextNode(replacedText), node);
                }
            }
        }
    }
    count -= 1;
    if (count) {
        setTimeout(switchem,currTimeout);
        if (currTimeout < maxTimeout) currTimeout *= 2;
    }
}

setTimeout(switchem, currTimeout);
if (currTimeout < maxTimeout) currTimeout *= 2;
