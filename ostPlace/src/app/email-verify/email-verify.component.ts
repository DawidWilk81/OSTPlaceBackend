import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-email-verify',
  templateUrl: './email-verify.component.html',
  styleUrls: ['./email-verify.component.scss']
})
export class EmailVerifyComponent implements OnInit {
  token:any;
  constructor(private _AR:ActivatedRoute) { }

  ngOnInit(): void {
    this.token = this._AR.snapshot.paramMap.get('token');
  }

}
