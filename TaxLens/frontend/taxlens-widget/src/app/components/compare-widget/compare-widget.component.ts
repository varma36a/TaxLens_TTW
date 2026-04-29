import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

interface CompanyOption {
  company_name: string;
}

@Component({
  selector: 'app-compare-widget',
  templateUrl: './compare-widget.component.html',
  styleUrls: ['./compare-widget.component.scss']
})
export class CompareWidgetComponent implements OnInit {
  companies: CompanyOption[] = [];
  company1 = '';
  company2 = '';
  comparisonResult: any;

  private readonly dummyCompanies: CompanyOption[] = [
    { company_name: 'Acme Manufacturing Pvt Ltd' },
    { company_name: 'Nimbus Retail Group' },
    { company_name: 'Vertex Software Solutions' },
    { company_name: 'Evergreen Logistics Inc' },
    { company_name: 'Apex Financial Services' }
  ];

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.api.getCompanyList().subscribe({
      next: (res: CompanyOption[]) => {
        this.companies = res?.length ? res : this.dummyCompanies;
      },
      error: () => {
        this.companies = this.dummyCompanies;
      }
    });
  }

  compare(): void {
    this.api.compareCompanies(this.company1, this.company2).subscribe((res) => {
      this.comparisonResult = res;
    });
  }
}
