var last_data = []; // data stored/kept from the last iteration

// to be called whenever a fetch goes badly
function whoops(e) {
  console.log(e);
  chrome.browserAction.setTitle({'title': 'ALS Status could not contact feed data feed.'});
  chrome.browserAction.setIcon({'path': 'question.png'});
  chrome.browserAction.setBadgeText({ 'text': ''});
}

// function that will listen for requests from any
// popups, asking to have the last fetched ALS 
// data send back.
chrome.runtime.onMessage.addListener(
  function(request, sender, resp_cb) {
    console.log("onMessage");
    if (request.message == 'update_popup') {
      resp_cb({'message': 'OK', 'data': last_data });
    } else {
      resp_cb({'message': 'not_for_me'});
    }
  }
);

// take the data returned by the xhr and 
// store a copy, and adjust the toolbar icon
// as appropriate
function handle_load_data() {
  if (this.status === 200) {
    data = JSON.parse(this.responseText);
    if (data !== null) {
      last_data = data;
      for (var i=0;i<data.length;i++) {
        var val = data[i].val;
        var label = data[i].label;
        if (label === 'Beam Available') {
          var icon = 'up.png';
          if (val) icon = 'down.png';
          chrome.browserAction.setIcon({'path': icon});
        } else if (label == 'Comment') {
          chrome.browserAction.setTitle({ 
            'title': val
          });
        } else if (label === 'Beam Current') {
          chrome.browserAction.setBadgeText({ 
            'text': Math.round(val).toString()
          });
        }
      }
      return;
    }
  }
  whoops(); // never get here in successful case
}

// query the ALS controls server and call handle_load_data
// with the result
function checkALS() {
 try {
   var xhr = new XMLHttpRequest();
   xhr.addEventListener('load',handle_load_data);
   xhr.addEventListener('abort',whoops);
   xhr.addEventListener('error',whoops);
   xhr.open('GET','https://controls.als.lbl.gov/als-beamstatus/curvals?v=1.23');
   xhr.send();
 } catch(e) {
   whoops();
 }
 setTimeout(checkALS, 60 * 1000);
}

checkALS();

