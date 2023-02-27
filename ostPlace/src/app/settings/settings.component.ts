import { Component, OnInit } from '@angular/core';
import { faCog, faPenAlt, faUser } from '@fortawesome/free-solid-svg-icons';
import { UserService } from '../user.service';
@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  changeEmail = false;
  changePassword = false;

  //FONT AWESOME ICONS
  cog = faCog;
  change = faPenAlt;
  user = faUser;

  //FORM VALUES
  password:any;
  constructor(
    private _US:UserService
  ) { }

  ngOnInit(): void {
  }

  showEmail(){
    this.changeEmail = !this.changeEmail;
  }

  showPassword(){
    this.changePassword = !this.changePassword;
  }

  updatePassword(){
    this._US.ChangePassword(this.password).subscribe(
      Response =>{
        console.log(Response);
      }, error =>{
        console.log(error);
      }
    )
  }
}
