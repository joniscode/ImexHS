import { Component } from '@angular/core';
import { RecursiveBoxComponent } from './recursive-box.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-hanoi',
  standalone: true,
  imports: [CommonModule, FormsModule, RecursiveBoxComponent],
  templateUrl: './hanoi.component.html',
  styleUrls: ['./hanoi.component.scss']
})
export class HanoiComponent {
  depth = 6;
  pythonCommand = 'cd Question-1 && python recursion_with_colors.py';

  showPythonHint() {
  const pythonCommand = 'cd Question-1 && python recursion_with_colors.py';
  navigator.clipboard.writeText(pythonCommand).then(() => {
    console.info('📌 Comando copiado. Ahora puedes ir a tu terminal y pegarlo.');
    console.info(pythonCommand);
    alert(
      '✅ Comando copiado al portapapeles:\n\n' +
      pythonCommand +
      '\n\n💡 Abre tu terminal (cmd o PowerShell), pégalo y presiona ENTER.'
    );
  }).catch(err => {
    console.error('❌ Error al copiar el comando', err);
    alert('❌ No se pudo copiar el comando al portapapeles. Intenta copiarlo manualmente:\n\n' + pythonCommand);
  });
}
}
