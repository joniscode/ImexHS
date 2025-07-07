# ImexHS
prueba para ImexHS


# 🧪 Angular Frontend App con Python - ImexHS

Este proyecto es una aplicación de inicio personalizada construida con Angular y Python. Contiene una landing page moderna y responsive con accesos directos a los 4 módulos de la prueba de Imex HS totalmente organizados.

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


## 📦 Tecnologías usadas

- Angular 17+
- Python 3+
- Standalone Components
- SQLite
- `ngModel` con `FormsModule`
- Estilos en SCSS
- Color dinámico con lógica TypeScript
- Metodologia Bem
- LocalStorage

## Instala las dependencias:
```bash
cd frontend-app
npm install
ng serve      # http://localhost:4200

- instalar extensión para imagenes de ser necesario

## Backend
uvicorn medical_api:app --reload #en la base del proyecto
# directamente servicial en el frontend