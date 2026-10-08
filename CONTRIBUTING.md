# Guía de contribución

Este repositorio forma parte de un proyecto de investigación. Los cambios deben ser revisables, reproducibles y trazables.

## Ramas recomendadas

- `main`: versión estable y revisada.
- `develop`: rama de integración opcional si el equipo crece.
- `feature/<nombre>`: una funcionalidad por rama.
- `fix/<nombre>`: correcciones de errores.
- `docs/<nombre>`: cambios exclusivamente documentales.

## Antes de modificar

1. Actualiza tu rama local.
2. Crea una rama nueva.
3. No trabajes directamente sobre `main` salvo una corrección excepcional autorizada.
4. No modifiques el perfil científico fijo `IW + GRD_HD + VV+VH` sin aprobación del equipo investigador.

## Solicitudes de incorporación de cambios (Pull Request)

Cada Pull Request debe incluir:

- descripción clara del cambio;
- motivo del cambio;
- archivos o módulos afectados;
- comando exacto utilizado para probarlo;
- evidencia de que las pruebas pasan;
- impacto esperado sobre el flujo de adquisición;
- confirmación de que no se incluyeron credenciales ni productos descargados.

## Convención sugerida para commits

Se mantiene el prefijo técnico habitual y la descripción se escribe en español:

- `feat: agregar validación del AOI`
- `fix: validar que la fecha final no sea anterior a la inicial`
- `docs: actualizar guía para investigadores`
- `test: agregar casos de selección del manifiesto`
- `refactor: simplificar construcción de consultas ASF`

## Pruebas

Antes de solicitar revisión:

```bash
pytest
```

Para comprobar la interfaz de línea de comandos:

```bash
deforest-s1 --help
deforest-s1 diagnostico
```
