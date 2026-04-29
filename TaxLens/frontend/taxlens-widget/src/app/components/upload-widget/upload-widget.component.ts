import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-upload-widget',
  templateUrl: './upload-widget.component.html'
})
export class UploadWidgetComponent {
  selectedFile!: File;
  uploadResult: any;

  constructor(private api: ApiService, private toastr: ToastrService) { }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.toastr.warning('Please select an Excel file');
      return;
    }

    this.api.uploadExcel(this.selectedFile).subscribe({
      next: (res) => {
        this.uploadResult = res;
        this.toastr.success('Excel uploaded successfully');
      },
      error: () => this.toastr.error('Upload failed')
    });
  }
}