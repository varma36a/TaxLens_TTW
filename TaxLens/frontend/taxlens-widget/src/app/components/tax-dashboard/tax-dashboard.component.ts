// src/app/components/tax-dashboard/tax-dashboard.component.ts

import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { ChartConfiguration, ChartOptions } from 'chart.js';

interface UploadedTaxRecord {
  company_name?: string;
  company?: string;
  name?: string;
  state_code?: string;
  jurisdiction?: string;
  entity_type?: string;
  effective_tax_rate?: number;
  tax_liability?: number;
  taxable_income?: number;
  total_revenue?: number;
  revenue?: number;
  deductions?: number;
  credits?: number;
  uploaded_at?: string;
  created_at?: string;
}

interface RecentUploadView {
  company: string;
  jurisdiction: string;
  entityType: string;
  effectiveRate: number;
  liability: number;
  taxableIncome: number;
}

interface JurisdictionExposure {
  name: string;
  count: number;
  liability: number;
}

@Component({
  selector: 'app-tax-dashboard',
  templateUrl: './tax-dashboard.component.html',
  styleUrls: ['./tax-dashboard.component.scss']
})
export class TaxDashboardComponent implements OnInit {

  totalUploads = 0;
  totalComparisons = 0;
  totalScenarios = 0;
  avgEffectiveRate = 0;
  totalTaxLiability = 0;
  totalTaxableIncome = 0;
  totalRevenue = 0;
  planningCoverage = 0;
  highRiskCount = 0;
  moderateRiskCount = 0;
  optimizedCount = 0;
  recentUploads: RecentUploadView[] = [];
  jurisdictionExposure: JurisdictionExposure[] = [];

  barChartType: 'bar' = 'bar';
  doughnutChartType: 'doughnut' = 'doughnut';

  barChartData: ChartConfiguration<'bar'>['data'] = {
    labels: ['Uploads', 'Comparisons', 'Scenarios'],
    datasets: [
      {
        data: [0, 0, 0],
        label: 'Platform Activity',
        backgroundColor: ['#38bdf8', '#34d399', '#f59e0b'],
        borderRadius: 10,
        borderSkipped: false
      }
    ]
  };

  barChartOptions: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#a8b3c7'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(148, 163, 184, 0.12)'
        },
        ticks: {
          color: '#a8b3c7',
          precision: 0
        }
      }
    }
  };

  riskChartData: ChartConfiguration<'doughnut'>['data'] = {
    labels: ['Optimized', 'Monitor', 'High Rate'],
    datasets: [
      {
        data: [0, 0, 0],
        backgroundColor: ['#34d399', '#f59e0b', '#fb7185'],
        borderColor: 'rgba(15, 23, 42, 0.95)',
        borderWidth: 4,
        hoverOffset: 6
      }
    ]
  };

  doughnutChartOptions: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '68%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#d8e0ef',
          boxWidth: 10,
          boxHeight: 10,
          usePointStyle: true
        }
      }
    }
  };

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.api.getUploads().subscribe((res: any) => {
      this.totalUploads = res.count || 0;
      const uploads = this.normalizeUploads(res.uploads || []);

      this.calculateUploadInsights(uploads);

      this.updateChart();
    });

    this.api.getComparisons().subscribe((res: any) => {
      this.totalComparisons = res.count || 0;
      this.updateChart();
    });

    this.api.getScenarios().subscribe((res: any) => {
      this.totalScenarios = res.count || 0;
      this.updateChart();
    });
  }

  updateChart(): void {
    this.barChartData = {
      labels: ['Uploads', 'Comparisons', 'Scenarios'],
      datasets: [
        {
          data: [
            this.totalUploads,
            this.totalComparisons,
            this.totalScenarios
          ],
          label: 'Platform Activity',
          backgroundColor: ['#38bdf8', '#34d399', '#f59e0b'],
          borderRadius: 10,
          borderSkipped: false
        }
      ]
    };

    this.planningCoverage = this.totalUploads
      ? Math.min(100, ((this.totalComparisons + this.totalScenarios) / (this.totalUploads * 2)) * 100)
      : 0;
  }

  formatCurrency(value: number): string {
    if (!value) {
      return '$0';
    }

    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: Math.abs(value) >= 1000000 ? 'compact' : 'standard',
      maximumFractionDigits: Math.abs(value) >= 1000000 ? 1 : 0
    }).format(value);
  }

  get efficiencyRatio(): number {
    return this.totalRevenue ? (this.totalTaxLiability / this.totalRevenue) * 100 : this.avgEffectiveRate;
  }

  private normalizeUploads(uploads: UploadedTaxRecord[]): UploadedTaxRecord[] {
    return Array.isArray(uploads) ? uploads : [];
  }

  private calculateUploadInsights(uploads: UploadedTaxRecord[]): void {
    const rates = uploads
      .map((upload) => Number(upload.effective_tax_rate || 0))
      .filter((rate) => rate > 0);

    this.avgEffectiveRate = rates.length
      ? rates.reduce((sum, rate) => sum + rate, 0) / rates.length
      : 0;

    this.totalTaxLiability = uploads.reduce(
      (sum, upload) => sum + Number(upload.tax_liability || 0),
      0
    );

    this.totalTaxableIncome = uploads.reduce(
      (sum, upload) => sum + Number(upload.taxable_income || 0),
      0
    );

    this.totalRevenue = uploads.reduce(
      (sum, upload) => sum + Number(upload.total_revenue || upload.revenue || 0),
      0
    );

    this.optimizedCount = rates.filter((rate) => rate < 18).length;
    this.moderateRiskCount = rates.filter((rate) => rate >= 18 && rate < 25).length;
    this.highRiskCount = rates.filter((rate) => rate >= 25).length;

    this.riskChartData = {
      labels: ['Optimized', 'Monitor', 'High Rate'],
      datasets: [
        {
          data: [this.optimizedCount, this.moderateRiskCount, this.highRiskCount],
          backgroundColor: ['#34d399', '#f59e0b', '#fb7185'],
          borderColor: 'rgba(15, 23, 42, 0.95)',
          borderWidth: 4,
          hoverOffset: 6
        }
      ]
    };

    this.recentUploads = uploads.slice(0, 5).map((upload) => ({
      company: upload.company_name || upload.company || upload.name || 'Unnamed company',
      jurisdiction: upload.state_code || upload.jurisdiction || 'Multi-state',
      entityType: upload.entity_type || 'Corporate',
      effectiveRate: Number(upload.effective_tax_rate || 0),
      liability: Number(upload.tax_liability || 0),
      taxableIncome: Number(upload.taxable_income || 0)
    }));

    const exposureMap = uploads.reduce((map, upload) => {
      const key = upload.state_code || upload.jurisdiction || 'Multi-state';
      const current = map.get(key) || { name: key, count: 0, liability: 0 };
      current.count += 1;
      current.liability += Number(upload.tax_liability || 0);
      map.set(key, current);
      return map;
    }, new Map<string, JurisdictionExposure>());

    this.jurisdictionExposure = Array.from(exposureMap.values())
      .sort((a, b) => b.liability - a.liability)
      .slice(0, 4);
  }
}
