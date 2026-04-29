import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScenarioWidgetComponent } from './scenario-widget.component';

describe('ScenarioWidgetComponent', () => {
  let component: ScenarioWidgetComponent;
  let fixture: ComponentFixture<ScenarioWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ScenarioWidgetComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScenarioWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
