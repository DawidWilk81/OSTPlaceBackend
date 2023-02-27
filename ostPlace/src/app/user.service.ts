import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

class User {
  constructor(
    public username:string = '',
    public token:string = '',
  ){}
}

@Injectable({
  providedIn: 'root',
})
export class UserService {
  backendLink = 'http://localhost:8000/';
  userInfo:User = new User;

  constructor(
    private _http: HttpClient,
    private _cookie: CookieService,
    private _router: Router
  ) { }
// EMAIL VERIFICATION
    verifyEmail(form:HTMLInputElement): void {
      
    }

// API FUNCTIONS
  login(body:any){
// LOGIN CALL VARS
    console.log('body: ', body, 'username: ', body['username'] );
    this.userInfo.username = body['username'];

// LOGIN CALL
    return this._http.post(this.backendLink + 'api/auth/', body).subscribe(
      Response =>{
        this._cookie.set('token', Object(Response)['token']);
        this.userInfo.token = Object(Response)['token'];
        this._router.navigateByUrl('home');
      }, error =>{
        console.log(error);
        alert('Not found any active account with provided credentials');
      }
    )
  }

  register(userInfo:any): Observable<any> {
    return this._http.post(this.backendLink + 'api/users/', userInfo);
  }

  ChangePassword(userPassword:any):Observable<any>{
    let params = new HttpParams().set('inputed', userPassword);
    return this._http.put(this.backendLink + 'api/', userPassword)
  }


}
