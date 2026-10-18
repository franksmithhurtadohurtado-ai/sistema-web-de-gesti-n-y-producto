/*
 * Validaciones del lado del cliente para los formularios de productos y pedidos.
 * Estas validaciones mejoran la experiencia del usuario, pero NO reemplazan a las
 * de Django: el servidor vuelve a validar todo.
 */
(function () {
  "use strict";

  // ---------- Utilidades ----------
  function mostrarError(campo, mensaje) {
    campo.classList.add("is-invalid");
    campo.classList.remove("is-valid");
    // Quita el error que haya puesto el servidor para ese campo
    const contenedor = campo.closest(".mb-3");
    contenedor.querySelectorAll(".server-error").forEach(function (el) { el.remove(); });

    let aviso = contenedor.querySelector(".js-error");
    if (!aviso) {
      aviso = document.createElement("div");
      aviso.className = "invalid-feedback js-error";
      contenedor.appendChild(aviso);
    }
    aviso.textContent = mensaje;
  }

  function marcarValido(campo) {
    campo.classList.remove("is-invalid");
    campo.classList.add("is-valid");
    const aviso = campo.closest(".mb-3").querySelector(".js-error");
    if (aviso) aviso.remove();
  }

  function esNumero(texto) {
    return texto !== "" && !isNaN(Number(texto)) && isFinite(Number(texto));
  }

  // ---------- Reglas por campo ----------
  // Cada regla recibe el valor (sin espacios sobrantes) y devuelve
  // un mensaje de error, o "" si el valor es correcto.
  const reglasProducto = {
    nombre: function (v) {
      if (v === "") return "El nombre es obligatorio.";
      if (v.length < 3) return "El nombre debe tener al menos 3 caracteres.";
      return "";
    },
    descripcion: function (v, campo) {
      const max = campo.maxLength > 0 ? campo.maxLength : 500;
      if (v.length > max) return "La descripción no puede superar los " + max + " caracteres.";
      return "";
    },
    precio: function (v) {
      if (v === "") return "El precio es obligatorio.";
      if (!esNumero(v)) return "El precio debe ser un número.";
      if (Number(v) <= 0) return "El precio debe ser mayor que cero.";
      return "";
    },
    cantidad_disponible: function (v) {
      if (v === "") return "La cantidad disponible es obligatoria.";
      if (!esNumero(v)) return "La cantidad debe ser un número.";
      if (!Number.isInteger(Number(v))) return "La cantidad debe ser un número entero.";
      if (Number(v) < 0) return "La cantidad no puede ser negativa.";
      return "";
    }
  };

  const reglasPedido = {
    numero_pedido: function (v) {
      if (v === "") return "El número del pedido es obligatorio.";
      return "";
    },
    cliente: function (v) {
      if (v === "") return "El nombre del cliente es obligatorio.";
      return "";
    },
    descripcion: function (v, campo) {
      if (v === "") return "La descripción del pedido es obligatoria.";
      const max = campo.maxLength > 0 ? campo.maxLength : 500;
      if (v.length > max) return "La descripción no puede superar los " + max + " caracteres.";
      return "";
    },
    valor_total: function (v) {
      if (v === "") return "El valor total es obligatorio.";
      if (!esNumero(v)) return "El valor total debe ser un número.";
      if (Number(v) <= 0) return "El valor total debe ser mayor que cero.";
      return "";
    },
    estado: function (v, campo) {
      const permitidos = Array.from(campo.options).map(function (o) { return o.value; });
      if (permitidos.indexOf(v) === -1) return "Selecciona un estado válido.";
      return "";
    }
  };

  // ---------- Conexión con el formulario ----------
  function activar(form, reglas) {
    if (!form) return;

    function validarCampo(campo) {
      const nombre = campo.name;
      if (!reglas[nombre]) return true;
      const mensaje = reglas[nombre](campo.value.trim(), campo);
      if (mensaje) {
        mostrarError(campo, mensaje);
        return false;
      }
      marcarValido(campo);
      return true;
    }

    // Al salir de un campo y mientras se corrige, se vuelve a validar
    Object.keys(reglas).forEach(function (nombre) {
      const campo = form.elements[nombre];
      if (!campo) return;
      campo.addEventListener("blur", function () { validarCampo(campo); });
      campo.addEventListener("input", function () {
        if (campo.classList.contains("is-invalid") || campo.classList.contains("is-valid")) {
          validarCampo(campo);
        }
      });
      campo.addEventListener("change", function () { validarCampo(campo); });
    });

    // Al enviar: si hay errores, se detiene el envío y se enfoca el primer campo inválido
    form.addEventListener("submit", function (evento) {
      let primerError = null;
      Object.keys(reglas).forEach(function (nombre) {
        const campo = form.elements[nombre];
        if (campo && !validarCampo(campo) && !primerError) primerError = campo;
      });
      if (primerError) {
        evento.preventDefault();
        primerError.focus();
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    activar(document.getElementById("form-producto"), reglasProducto);
    activar(document.getElementById("form-pedido"), reglasPedido);
  });
})();