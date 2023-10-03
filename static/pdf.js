// POST PDF
const form = document.getElementById('PDF');
const dataContainer = document.getElementById('dataContainer');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const url = '/lecto/pdf';
  const formData = new FormData(form);

  fetch(url, {
    method: 'POST',
    body: formData
  })
    .then(response => {
      console.log(response)
      if (!response.ok) {
        console.log(response)
        return response.json().then(error => {
          console.log(error)
          throw new Error(error.detail);
        })
      }
      return response.json()
    })
    .then(result => {

      printList(result);

      // Saving to local Storage
      saveData(result);

    })
    .catch(error => {
      // Alerta de error
      console.error(error);

      var alertContainer = document.getElementById("alertContainer");
      var alertHtml = `
     <div class="alert alert-danger alert-dismissible fade show" role="alert">
       ${error}
       <button type="button" class="close" data-dismiss="alert" aria-label="Close">
         <span aria-hidden="true">&times;</span>
       </button>
     </div>
   `;

      alertContainer.innerHTML = alertHtml;

      // Cierra automáticamente la alerta después de 3 segundos
      setTimeout(function () {
        alertContainer.innerHTML = '';
      }, 4000);
    });
})

function printList(result) {
  const dataContainer = document.getElementById('dataContainer');

  //  Creando Fila
  const row = document.createElement('tr');

  // Creando Ticket
  const ticket = document.createElement('td');
  ticket.textContent = result.ticket
  // Creando Tiempo
  const tiempo = document.createElement('td');
  tiempo.textContent = result.tiempo_estimado;

  // Creando fecha
  var dateTime = new Date(result.Fecha);
  var formattedDate = formatDate(dateTime);
  const Fecha = document.createElement('td');
  Fecha.textContent = formattedDate

  // Creando Hora
  var formattedTime = formatTime(dateTime);
  const Hora = document.createElement('td');
  Hora.textContent = formattedTime

  // Creando nombre
  const Nombre = document.createElement('td');
  Nombre.textContent = result.Nombre

  // Creando Idioma
  const idioma = document.createElement('td');
  if (result.idioma == "eng") {
    idioma.textContent = "Ingles"
  }
  else{
    idioma.textContent = "Español"
  }

  // Creando Boton Consultar
  const consult = document.createElement('td');
  const button = document.createElement('button');
  button.classList.add('btn', 'btn-info', 'btn-sm');
  button.textContent = 'Consultar';
  button.onclick = function () {
    enviarDatos(result.ticket, result.idioma);
  };

  consult.appendChild(button)

  // Creando Boton Eliminar
  const deleteRow = document.createElement('td');
  const deletebtn = document.createElement('button');
  deletebtn.classList.add('btn', 'btn-danger', 'btn-sm');

  var deleteIcon = document.createElement('i');
  deleteIcon.classList.add('fas', 'fa-trash');
  deletebtn.appendChild(deleteIcon);

  deletebtn.onclick = function () {
    mostrarAlerta(result.ticket);
  };

  deleteRow.appendChild(deletebtn)

  row.appendChild(ticket)
  row.appendChild(tiempo)
  row.appendChild(Fecha)
  row.appendChild(Hora)
  row.appendChild(Nombre)
  row.appendChild(idioma)
  row.appendChild(consult)
  row.appendChild(deleteRow)

  dataContainer.appendChild(row);
}

function formatDate(date) {
  var options = { year: "numeric", month: "long", day: "numeric" };
  return date.toLocaleDateString("es-ES", options);
}

function formatTime(date) {
  var options = { hour: "numeric", minute: "numeric", second: "numeric" };
  return date.toLocaleTimeString("es-ES", options);
}
