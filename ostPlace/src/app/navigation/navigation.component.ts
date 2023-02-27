import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faUser, faCog, faCompactDisc, faFolderPlus, faBell, faPowerOff, faShoppingBasket } from '@fortawesome/free-solid-svg-icons';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {
  userIcon = faUser;
  cog = faCog;
  disc = faCompactDisc;
  plus = faFolderPlus;
  bell = faBell;
  logout = faPowerOff;
  basket = faShoppingBasket;
  constructor(
    private _router:Router,
    private _cookie:CookieService

  ) { }

  ngOnInit(): void {

  }

  logOut(){
    this._router.navigateByUrl('');
    this._cookie.deleteAll();
  }

  changeDir(dir:string){
    this._router.navigateByUrl(dir);
  }

}
