    
const contenidoCocina = document.getElementById('contenedor_cocinas');
const contenidoInventario = document.getElementById('contenedor_inventario');
const contenidoMissiones = document.getElementById('contenedor_missiones');
const contenidoInicio = document.getElementById('contenedor_inicio');
//inicio las constantes con el valor de los contenedores para dar un efecto de oculto

function buttonOpcion(dato) {
    //cada que se toca el button se ocultan los contenedores    
    contenidoCocina.style.display = 'none';
    contenidoInventario.style.display = 'none';
    contenidoMissiones.style.display = 'none';
    contenidoInicio.style.display = 'none';
    //y dependiendo de la eleccion se ve el contenedor elegido
    if(dato === 'inventario') {
        contenidoInventario.style.display = 'block';
    } else if(dato === 'cocina') {
        contenidoCocina.style.display = 'block';
    } else if(dato === 'missiones') {
        contenidoMissiones.style.display = 'block';
    } else if(dato === 'inicio') {
        contenidoInicio.style.display = 'block';
    }
    
}
//funcion cocina imlementada en el app.py donde se utiliza el metodo post para agregar el producto
function cocinar(productoId) {
    fetch('/cocinar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({
            'producto_id': productoId
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultadoDiv = document.getElementById('resultado');
        if (data.success) {
            resultadoDiv.innerHTML = `<div>${data.message}</div>`;
        }//mensaje de estado
    })
    .catch(error => {
        console.error('Error:', error);
        const resultadoDiv = document.getElementById('resultado');
        resultadoDiv.innerHTML = `<div>Error al procesar la solicitud.</div>`;
    });
}
//llama a la funcion missiones dependiendo la eleccion elegida
function completarMision(misionId) {
    fetch(`/misiones/${misionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`mensaje${misionId.slice(-1)}`).innerText = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
//por un lado un button que inicia la funcion para que despues devuelva un dato
//dicho resultado se envia al html para que se vea la info
document.addEventListener('DOMContentLoaded', function() {
    const gatchaButton = document.getElementById('gatchaButton');
    const resultadoGatcha = document.getElementById('resultadoGatcha');

    function buildImageUrl(cartaImagen) {
        return `/static/img/cartas/${cartaImagen}.png`;
    }
    gatchaButton.addEventListener('click', function() {
        fetch('/gatcha', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Muestra la carta ganada
                const cartaImagenUrl = buildImageUrl(data.carta.imagen);
                    resultadoGatcha.innerHTML = `
                        <div class="carta" >
                            <img src="${cartaImagenUrl}" alt="${data.carta.nombre}">
                            <p>${data.carta.nombre}</p>
                        </div>
                    `;
            } else {
                // Muestra el error si ocurrió
                resultadoGatcha.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultadoGatcha.innerHTML = `<p>Error al realizar la tirada gatcha.</p>`;
        });
    });
});
