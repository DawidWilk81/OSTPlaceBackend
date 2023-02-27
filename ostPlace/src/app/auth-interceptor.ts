import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpEvent, HttpResponse, HttpRequest, HttpHandler } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
import { UserService } from './user.service';
import { Router } from '@angular/router';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    constructor(
        private _cookie: CookieService,
        private _router: Router
    ){}
  intercept(request: HttpRequest<any>, next: HttpHandler):
   Observable<HttpEvent<any>> {
    let token = this._cookie.get('token');
    console.log('INTERCEPT TOKEN: ', token);
    console.log('URL NOW: ', this._router.routerState.snapshot.url);
    //  If on main page without token
    if (token) {
      request = request.clone({
        setHeaders: {
        Authorization: `Token ${token}`
      }
      });

      if(this._router.routerState.snapshot.url == '/' || this._router.routerState.snapshot.url == 'register' || this._router.routerState.snapshot.url == 'login'){
        this._router.navigateByUrl('home');
      }

    // If on main page with token
      return next.handle(request);
    }if(!token){
      if(this._router.routerState.snapshot.url == 'register' || this._router.routerState.snapshot.url == 'login'){
        return next.handle(request)      
      }else{
        this._router.navigateByUrl('');
      }
      return next.handle(request)
    }
    return next.handle(request);
  }
}

