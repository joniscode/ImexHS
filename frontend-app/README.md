# 🧪 Angular Frontend App - ImexHS

Este proyecto es una aplicación de inicio personalizada construida con Angular. Contiene una landing page moderna y responsive con accesos directos a los 4 módulos de la prueba de Imex HS.

## 🚀 Características

- ✨ Diseño moderno basado en la plantilla oficial de Angular 17+
- 🎨 Estilos personalizados con SCSS y colores dinámicos
- 📱 Responsive adaptado para móviles y escritorio
- 🔗 Acceso rápido a los 4 módulos clave mediante botones llamativos
- 🧭 Estructura modular lista para escalar

## 📁 Estructura del proyecto

frontend-app/
├── src/ 
│ ├── app/
│ │  ├└─ features
│ │  │    ├── spp.html/ # Punto disponible para la pantalla inicial
│ │  │    └── app.scss/ # Estilos globales para la pantalla principal
│ │  ├── Question-1
│ │  ├── Question-2
│ │  ├── Question-3
│ │  └── Question-4
│ ├── assets/ # Imágenes y recursos estáticos
│ └── main.ts # Punto de entrada principal
├── angular.json # Configuración de Angular CLI
├── package.json # Dependencias y scripts
└── README.md

## ▶️ Cómo ejecutar localmente

1. Instala las dependencias:

- npm install
- ng serve


## EJERCICIO 1

Este módulo demuestra el uso de **componentes recursivos** en Angular mediante una visualización anidada de cajas de colores, donde cada componente hijo representa una menor profundidad en la recursión. El nivel de recursión se puede ajustarse dinámicamente desde el navegador.

---

## 📂 Ubicación del módulo

`src/app/Question-1/`

---

## 🚀 Cómo funciona

- Se ha creado un componente principal `HanoiComponent`.
- Este componente renderiza un componente hijo `RecursiveBoxComponent` recursivamente.
- Cada nivel de profundidad se representa visualmente con una caja anidada de diferente color.
- Un **control deslizante (slider)** permite cambiar dinámicamente la profundidad (`depth`) desde el navegador.

---

## 📸 Vista previa

- Cambia el valor del slider (`1 - 10`) y observa cómo se renderizan las cajas de forma anidada.
- Cada caja se genera con un color dinámico, usando el valor de `depth` como base.

---

## 🛠️ Archivos principales

- `hanoi.component.ts`: Componente principal del ejercicio.
- `hanoi.component.html`: Vista que incluye el control deslizante y renderiza el componente recursivo.
- `recursive-box.component.ts`: Componente recursivo, se llama a sí mismo según el valor de `depth`.
- `recursive-box.component.html`: Renderiza visualmente una caja y su hijo recursivo.
- `recursive-box.component.scss`: Estilos para la presentación anidada.

---

## 📦 Tecnologías usadas

- Angular 17+
- Standalone Components
- `ngModel` con `FormsModule`
- Estilos en SCSS
- Color dinámico con lógica TypeScript


