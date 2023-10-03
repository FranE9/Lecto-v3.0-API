
    // TEXT GET RESULTS

    function enviarTexto(event) {
      event.preventDefault();

      const form = document.getElementById('formText');
      const texto = form.elements.Texto.value;
      const idioma = form.elements.idioma.value;
      enviarDatosTexto(texto, idioma);
    }

    function enviarDatosTexto(texto, idioma) {

      const urlText = '/lecto/text';
      var datatext = new URLSearchParams();
      datatext.append('Texto', texto);
      datatext.append('Idioma', idioma);

      fetch(urlText, {
        method: 'POST',
        body: datatext
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

          var alertContainer = document.getElementById("alertContainerText");
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
