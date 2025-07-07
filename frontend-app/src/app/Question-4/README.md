### README – Ejercicio 4  
*(colócalo en `Question-4/README.md`)*  

```md
# Ejercicio 4 – Estimación de Área de Mancha

Angular 17 · Canvas API · LocalStorage  
**Solo front-end** (no requiere servidor backend)

---

## Descripción

Calcula el área aproximada de una mancha blanca en una imagen binaria usando un método tipo Monte Carlo:

1. Subes una imagen (PNG/JPG) blanca-sobre-negro.  
2. El sistema genera _n_ puntos aleatorios.  
3. Cuenta cuántos caen dentro de la mancha → `Área ≈ (nᵢ / n) * Área imagen`.  
4. Guarda cada resultado en el Historial (LocalStorage).

---

## Instalación y arranque

```bash
cd frontend-app
npm install
ng serve      # http://localhost:4200