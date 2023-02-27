import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UnloggedComponent } from './unlogged/unlogged.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LoggedHomeComponent } from './logged-home/logged-home.component';
import { MyOstComponent } from './my-ost/my-ost.component';
import { SettingsComponent } from './settings/settings.component';
import { AddSongComponent } from './add-song/add-song.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { ChangeOSTComponent } from './change-ost/change-ost.component';
import { BasketComponent } from './basket/basket.component';

const routes: Routes = [
  {path:'', component:UnloggedComponent},
  {path:'login', component:LoginComponent},
  {path:'register', component:RegisterComponent},
  {path:'home', component:LoggedHomeComponent},
  {path:'activateAccount/:token', component:RegisterComponent},
  
  // API sites
  {path:'notifications', component:NotificationsComponent},
  {path:'myOST', component:MyOstComponent},
  {path:'myOST/change/:id', component:ChangeOSTComponent},
  {path:'settings', component:SettingsComponent},
  {path:'addSong', component:AddSongComponent},
  {path:'basket', component:BasketComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
