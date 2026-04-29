import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxDashboardComponent } from './tax-dashboard.component';

describe('TaxDashboardComponent', () => {
  let component: TaxDashboardComponent;
  let fixture: ComponentFixture<TaxDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TaxDashboardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaxDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
