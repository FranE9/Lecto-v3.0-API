function enviar(event) {
  console.log("en funcion enviar")
  event.preventDefault();

  const form = document.getElementById('formTicket');
  const ticket = form.elements.Ticket.value;
  const idioma = form.elements.idioma.value;
  enviarDatos(ticket, idioma);
}

// POST TICKET GET RESULTS

function enviarDatos(ticket, idioma) {

    const urlTicket = '/lecto/ticket';
    var data = new URLSearchParams();
    data.append('Ticket', ticket);

    fetch(urlTicket, {
      method: 'POST',
      body: data
    })
      .then(response => {
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

        console.log("Resultados del ticket")
        console.log(result)

        if (idioma == "spa") {
          var params = new URLSearchParams({
            parrafo: result.Parrafo,
            pazos: result.szigrisztPazos_INFLESZ,
            huerta: result.fernandezHuerta,
            mu: result.legibilidadMu
          });

          window.location.href = '/lecto/get-results?' + params.toString();
        }
        if (idioma == "eng") {
          var params = new URLSearchParams({
            parrafo: result.Parrafo,
            flesh: result.fleshReadingEasy,
            fog: result.fogReading,
            smog: result.smogReading
          });

          window.location.href = '/lecto/get-results-eng?' + params.toString();

        }


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
        }, 10000);
      });
  }
