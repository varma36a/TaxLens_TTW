import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-chat-widget',
  templateUrl: './chat-widget.component.html'
})
export class ChatWidgetComponent {
  query = '';
  response = '';

  constructor(private api: ApiService) { }

  askAI(): void {
    this.api.explainTax(this.query).subscribe((res: any) => {
      this.response = res.explanation;
    });
  }
}