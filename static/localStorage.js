function saveData(result) {
    var jsonString = JSON.stringify(result);
    localStorage.setItem(result.ticket, jsonString);
    console.log('Data saved to local storage.');
    console.log("Showing Data Saved");

    var data = localStorage.getItem(result.ticket);
    var retrievedObject = JSON.parse(data);
    console.log(retrievedObject);
}

function getAllLocalStorageElements() {
    var numElements = localStorage.length;

    if (numElements === 0) {
        console.log('No elements found in local storage.');
        return;
    }

    for (var i = 0; i < numElements; i++) {
        var key = localStorage.key(i);
        var data = localStorage.getItem(key);
        var result = JSON.parse(data);

        printList(result);
    }
}

var deleteFlag = false;
var key = '';

function mostrarAlerta(ticket) {
  deleteFlag = false; 
  key = ticket
  $('#confirmModal').modal('show');
}


function deleteItem() {
    localStorage.removeItem(key);
    location.reload();
}