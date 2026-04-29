import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompareWidgetComponent } from './compare-widget.component';

describe('CompareWidgetComponent', () => {
  let component: CompareWidgetComponent;
  let fixture: ComponentFixture<CompareWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CompareWidgetComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CompareWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
