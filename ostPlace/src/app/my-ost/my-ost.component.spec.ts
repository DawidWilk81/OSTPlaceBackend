import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyOstComponent } from './my-ost.component';

describe('MyOstComponent', () => {
  let component: MyOstComponent;
  let fixture: ComponentFixture<MyOstComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MyOstComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MyOstComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
