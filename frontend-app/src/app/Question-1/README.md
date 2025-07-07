# Ejercicio 1 – Recursión y Colores

Este ejercicio representa visual y lógicamente una solución al problema de las Torres de Hanoi con una regla adicional: **no se pueden apilar discos del mismo color**.

---

## 🧠 Lógica Recursiva en Python

Archivo: `recursion_with_colors.py`

Este script implementa una versión recursiva del problema con restricciones adicionales:
- Un disco más grande no puede ir encima de uno más pequeño.
- Discos del mismo color no pueden estar uno sobre otro.
- Usa recursión pura para calcular la secuencia de movimientos.


```bash
python recursion_with_colors.py

## 4.📦 Estructura del proyecto

Question-1/
├── hanoi.component.html/ # estructura del disco
├── hanoi.component.scss/ # estilos para el disco
├── hanoi.component.ts/ # Angular para los discos
├── index.ts # Lógica de procesamiento
├── recursion_with_colors.py # Back del proceso y logica profunda de la funcion a realizar de los discos
├── recursive-box.component.html # estructura de las cajas
├── recursive-box.component.scss # Estilos de de las cajas
├── recursive-box.component.tss # Angular de las cajas
└── README.md #Notas del archivo
