import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faCheck } from '@fortawesome/free-solid-svg-icons';
import { UserService } from '../user.service';

class Signup {
  constructor(
    public username:string = '', 
    public email:string = '', 
    public password:string = '',
  ){}
}

class email {
  constructor(
    public subject='Activate your account',
    public toEmail='',
  ){}
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})

export class RegisterComponent implements OnInit {


  check = faCheck;
  userInfo:Signup = new Signup();
  emailForm:email = new email();
  //form validator box's
  logFocus=false;
  passFocus=false;

  test(ev:any){
    console.log(ev);
  }


  constructor(
    private _US:UserService,
    private _router:Router
  ) { }

  ngOnInit(): void {
    
  }

  registerUser(){
    return this._US.register(this.userInfo).subscribe(
      Response =>{
        alert('User registered correctly');
        this._router.navigateByUrl('');
      }, error =>{
        console.log(error);
        alert('Email already in use by another account');
      }
    )
  }

}
