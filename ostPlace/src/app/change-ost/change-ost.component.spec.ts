import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeOSTComponent } from './change-ost.component';

describe('ChangeOSTComponent', () => {
  let component: ChangeOSTComponent;
  let fixture: ComponentFixture<ChangeOSTComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChangeOSTComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangeOSTComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
