document.getElementById("name-form").value  = getSavedValue("name-form");
document.getElementById("id-form").value    = getSavedValue("id-form");
document.getElementById("price-form").value = getSavedValue("price-form");

//Save the value function - save it to localStorage as (ID, VALUE)
function saveValue(e){
    var id = e.id;  // get the sender's id to save it . 
    var val = e.value; // get the value. 
    localStorage.setItem(id, val);// Every time user writing something, the localStorage's value will override
}

//get the saved value function - return the value of "v" from localStorage. 
function getSavedValue(v){
    if (!localStorage.getItem(v)) {
        return "";
    }
    return localStorage.getItem(v);
}

function DeleteRow(currentrow) {
    var table = currentrow.parentNode.parentNode;
    var name = $(currentrow).closest('tr').find('#name-td').text()

    table.parentNode.removeChild(table);
    $.ajax({
      type: "POST",
      url: "/delete-item",
      contentType: 'application/json',
      data: JSON.stringify({
          "name":name
      }),
      success: function (response) {
        console.log(response);
        setInterval('location.reload()', 1000);
      },
    });
}

function AddItem() {

  var name  = document.getElementById('name-form').value
  var id    = document.getElementById('id-form').value
  var price = document.getElementById('price-form').value

  var table         = document.getElementById('fancytable')
  var newRow        = table.insertRow()
  var newCellName   = newRow.insertCell(0)
  var newCellId     = newRow.insertCell(1)
  var newCellPrice  = newRow.insertCell(2)
  var newCellDelBtn = newRow.insertCell(3)

  newCellName.innerHTML   = name
  newCellId.innerHTML     = id
  newCellPrice.innerHTML  = price
  newCellDelBtn.innerHTML = '<input type="button" value="Delete Row" onclick="DeleteRow(this)">'

  $.ajax({
    type: "POST",
    url: "/add-item",
    contentType: 'application/json',
    data: JSON.stringify({
        "name": name,
        "id": id,
        "price": price
    }),
    success: function (response) {
      console.log(response);
      setInterval('location.reload()', 1000);
    },
  });
}

function clear_form() {
  document.getElementById("add-item-form").reset(); 
}