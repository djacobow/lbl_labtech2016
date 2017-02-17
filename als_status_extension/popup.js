// convert the ALS JSON blob to a minimally
// formatted table, then drop it where it belongs
function createTable(d,where) {
      var t = document.createElement('table');

      var row = t.insertRow(0);
      var x0  = row.insertCell(0);
      var x1  = row.insertCell(1);
      var x2  = row.insertCell(2);
      x0.textContent = 'Label';
      x1.textContent = 'Value';
      x2.textContent = 'Last Update';

      for (var i=0;i<d.length;i++) {
        row  = t.insertRow(i+1);
        row.className = i % 2 ? 'even' : 'odd';
        x0   = row.insertCell(0);
        x1   = row.insertCell(1);
        x2   = row.insertCell(2);
        var name = d[i].label;
        var val  = d[i].val;
        if (!isNaN(val)) {
          val *= 10000;
          val = Math.round(val);
          val /= 10000;
        }
        var ts   = d[i].tstamp;
        var dt   = new Date(ts*1000); 
        x0.textContent = name;
        x0.className = 'label';
        x1.textContent = val;
        x1.className = 'value';
        x2.textContent = dt.toLocaleString();
        x2.className = 'date';
      }
      document.getElementById(where).appendChild(t);
}

// send a message to the background script and ask it
// to send back the ALS status, then make a table with it
function askToBePopulated() {
  chrome.runtime.sendMessage({'message': 'update_popup'},function cb(resp) {
    if (resp.message == 'OK') {
      var d = resp.data;
      if (d !== undefined) createTable(d,'topdiv');
    }
    // console.log(resp);
    return true;
  });
}


askToBePopulated();

