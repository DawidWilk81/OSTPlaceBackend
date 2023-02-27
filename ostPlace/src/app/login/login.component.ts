import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { UserService } from '../user.service';
class loginData {
  constructor(
    public username:string = '', 
    public password:string = '',
  ){}
}


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  errorLogin = false;
  userInfo:loginData = new loginData();

  constructor(
    private _US:UserService,
    // private _CS:CookieService
  ) { }

  ngOnInit(): void {
  }

  loginUser(){
    return this._US.login({username:this.userInfo.username, password: this.userInfo.password});
    
  }

}
