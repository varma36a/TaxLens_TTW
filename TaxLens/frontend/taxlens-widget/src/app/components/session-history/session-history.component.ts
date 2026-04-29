import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-session-history',
  templateUrl: './session-history.component.html'
})
export class SessionHistoryComponent implements OnInit {
  sessions: any[] = [];

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.api.getSessions().subscribe((res: any) => {
      this.sessions = res.sessions;
    });
  }
}