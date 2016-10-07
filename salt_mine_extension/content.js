var currTimeout = 1000;
var count = 5;

var patterns = [
  [ /[tT]he Lab(oratory)?/, 'The Salt Mine' ],
  [ /(?:(?:Ernest\sOrlando\s)?Lawrence\s)?Berkeley\s(?:National\s)?Lab(?:oratory)?/,
    'Salt Mine of Science' ],
];

function switchem(patterns) {
  var elements = document.getElementsByTagName('*');
  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    for (var j = 0; j < element.childNodes.length; j++) {
      var node = element.childNodes[j];
      if (node.nodeType === 3) {
        var text = node.nodeValue;
        var newText = text;
        for (var k=0;k<patterns.length; k++) {
          newText = newText.replace(patterns[k][0],patterns[k][1]);
        }
        if (newText !== text) {
          element.replaceChild(document.createTextNode(newText), node);
        }
      }
    }
  }
}

function run() {
  switchem(patterns);
  count -= 1;
  if (count) {
    setTimeout(run,currTimeout);
    currTimeout *= 1.5;
  }
}

setTimeout(run, currTimeout);
