import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-scenario-widget',
  templateUrl: './scenario-widget.component.html'
})
export class ScenarioWidgetComponent {
  payload: any = {
    company_name: '',
    new_state_code: '',
    new_entity_type: '',
    additional_deductions: 0,
    additional_credits: 0
  };

  result: any;

  constructor(private api: ApiService) { }

  runScenario(): void {
    this.api.runScenario(this.payload).subscribe((res) => {
      this.result = res;
    });
  }
}