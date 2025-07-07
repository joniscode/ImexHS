import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule }   from '@angular/common';
import { FormsModule }    from '@angular/forms';
import { HttpClient, HttpClientModule, HttpParams } from '@angular/common/http';

interface Entry {
  id: string;
  device_name: string;
  avg_before: number;
  avg_after:  number;
  data_size:  number;
  created_date: string;
  updated_date: string;

  edit_id: string;
  edit_device: string; 
}

@Component({
  selector: 'app-question-3',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './question-3.component.html',
  styleUrls:  ['./question-3.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class Question3Component implements OnInit {

  /* UI */
  selectedFile: File | null = null;
  loading = false;
  error   = '';
  message = '';
  result: any = null;
  showJson = true;

  /* Tabla & filtros */
  entries: Entry[] = [];
  filters = { averageMin: 0, averageMax: 1 };

  private API = 'http://localhost:8000/api/elements';

  constructor(private http: HttpClient) {}
  ngOnInit(): void { this.fetchEntries(); }

  /* ───────── carga de archivo ───────── */
  onFileChange(evt: Event): void {
    const file = (evt.target as HTMLInputElement).files?.[0];
    if (!file) return;

    if (file.type === 'application/json' || file.name.endsWith('.json')) {
      this.selectedFile = file;
      this.error = '';
    } else {
      this.error = '❌ El archivo debe ser .json';
      this.selectedFile = null;
    }
  }

  onUpload(): void {
    if (!this.selectedFile) return;

    const reader = new FileReader();
    reader.onload = () => {
      try {
        
        let txt = (reader.result as string).replace(/,(?=\d)/g, '.');

        
        let data: any = JSON.parse(txt);

        if (Array.isArray(data)) {
          const tmp: any = {};
          data.forEach((el, i) => tmp[(i + 1).toString()] = el);
          data = tmp;
        }

        this.loading = true;

        this.http.post(this.API + '/', data).subscribe({
          next: res => {
            this.result  = res;
            this.loading = false;
            this.fetchEntries();
          },
          error: err => {
            const detail = err.error?.detail ?? 'Error desconocido';
            this.error   = `❌ ${detail}`;
            this.loading = false;
          }
        });

      } catch {
        this.error = '❌ El contenido no es un JSON válido.';
      }
    };
    reader.readAsText(this.selectedFile);
  }

  fetchEntries(): void {
    const params = new HttpParams()
      .set('avg_before_min', this.filters.averageMin)
      .set('avg_before_max', this.filters.averageMax);

    this.http.get<any[]>(this.API + '/', { params }).subscribe({
      next: rows => {
        
        this.entries = rows.map(r => ({
          ...r,
          edit_id: r.id,
          edit_device: r.device_name
        }));
      },
      error: err => console.error('❌ Error al cargar', err)
    });
  }

  onFilter(): void { this.fetchEntries(); }

  onUpdate(row: Entry): void {
    
    const payload: any = {};
    if (row.edit_device && row.edit_device !== row.device_name) {
      payload.device_name = row.edit_device;
    }
    if (row.edit_id && row.edit_id !== row.id) {
      payload.new_id = row.edit_id;
    }
    if (Object.keys(payload).length === 0) {
      this.message = '⚠️ Sin cambios';
      return;
    }

    this.http.put(`${this.API}/${row.id}`, payload, { responseType: 'text' })
      .subscribe({
        next: ()  => { this.message = '✅ Guardado'; this.fetchEntries(); },
        error: e => {
          const detail = e.error?.detail ?? 'Error';
          this.message = `❌ ${detail}`;
        }
      });
  }

  onDelete(id: string): void {
    if (!confirm('¿Deseas eliminar este registro?')) return;
    this.http.delete(`${this.API}/${id}`, { responseType: 'text' }).subscribe({
      next: ()  => { this.message = '✅ Eliminado'; this.fetchEntries(); },
      error: () => this.message = '❌ Error al eliminar'
    });
  }

  clear(): void {
    this.selectedFile = null;
    this.result = null;
    this.error = this.message = '';
    this.loading = false;
  }
}
