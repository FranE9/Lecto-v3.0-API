function spaResults() {
    // Obtener los parámetros de la cadena de consulta
    var params = new URLSearchParams(window.location.search);
    console.log(params)
    var resultParrafo = params.get('parrafo');
    var resultPazos = params.get('pazos');
    var resultHuerta = params.get('huerta');
    var resultMu = params.get('mu');

    // Creando parrafo
    var row = document.createElement('tr');
    var firstColumn = document.createElement('td');
    var secondColumn = document.createElement('td');

    firstColumn.textContent = "Parrafo";
    secondColumn.textContent = resultParrafo

    row.appendChild(firstColumn)
    row.appendChild(secondColumn)

    dataContainer.appendChild(row);

    // Creando pazos

    var rowPazos = document.createElement('tr');
    var firstPazos = document.createElement('td');
    var secondPazos = document.createElement('td');

    firstPazos.textContent = "Szigriszt-Pazos / INFLESZ";
    secondPazos.textContent = resultPazos

    rowPazos.appendChild(firstPazos)
    rowPazos.appendChild(secondPazos)

    dataContainer.appendChild(rowPazos);


    // Creando Huerta
    var rowHuerta = document.createElement('tr');
    var firstHuerta = document.createElement('td');
    var secondHuerta = document.createElement('td');

    firstHuerta.textContent = "Fernandez Huerta";
    secondHuerta.textContent = resultHuerta

    rowHuerta.appendChild(firstHuerta)
    rowHuerta.appendChild(secondHuerta)

    dataContainer.appendChild(rowHuerta);


    // Creando Mu
    var rowMu = document.createElement('tr');
    var firstMu = document.createElement('td');
    var secondMu = document.createElement('td');

    firstMu.textContent = "Legibilidad Mu";
    secondMu.textContent = resultMu

    rowMu.appendChild(firstMu)
    rowMu.appendChild(secondMu)

    dataContainer.appendChild(rowMu);
}

function engResults() {
    // Obtener los parámetros de la cadena de consulta
    var params = new URLSearchParams(window.location.search);
    console.log(params)
    var resultParrafo = params.get('parrafo');
    var resultFlesh = params.get('flesh');
    var resultFog = params.get('fog');
    var resultSmog = params.get('smog');

    // Creando parrafo
    var row = document.createElement('tr');
    var firstColumn = document.createElement('td');
    var secondColumn = document.createElement('td');

    firstColumn.textContent = "Parrafo";
    secondColumn.textContent = resultParrafo

    row.appendChild(firstColumn)
    row.appendChild(secondColumn)

    dataContainer.appendChild(row);

    // Creando flesh

    var rowFlesh = document.createElement('tr');
    var firstFlesh = document.createElement('td');
    var secondFlesh = document.createElement('td');

    firstFlesh.textContent = "Flesch Reading Easy";
    secondFlesh.textContent = resultFlesh

    rowFlesh.appendChild(firstFlesh)
    rowFlesh.appendChild(secondFlesh)

    dataContainer.appendChild(rowFlesh);


    // Creando Huerta
    var rowFog = document.createElement('tr');
    var firstFog = document.createElement('td');
    var secondFog = document.createElement('td');

    firstFog.textContent = "Fog Reading";
    secondFog.textContent = resultFog

    rowFog.appendChild(firstFog)
    rowFog.appendChild(secondFog)

    dataContainer.appendChild(rowFog);


    // Creando smog
    var rowSmog = document.createElement('tr');
    var firstSmog = document.createElement('td');
    var secondSmog = document.createElement('td');

    firstSmog.textContent = "Smog reading";
    secondSmog.textContent = resultSmog

    rowSmog.appendChild(firstSmog)
    rowSmog.appendChild(secondSmog)

    dataContainer.appendChild(rowSmog);

}