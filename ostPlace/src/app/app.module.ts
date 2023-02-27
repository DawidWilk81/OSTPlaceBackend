import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { UnloggedComponent } from './unlogged/unlogged.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { RouterModule } from '@angular/router';
import { HttpClientModule, HTTP_INTERCEPTORS  } from '@angular/common/http';
import { EmailVerifyComponent } from './email-verify/email-verify.component';
import { LoggedHomeComponent } from './logged-home/logged-home.component';
import { UserService } from './user.service';
import { CookieService } from 'ngx-cookie-service';
import { AuthInterceptor } from './auth-interceptor';
import { SettingsComponent } from './settings/settings.component';
import { AddSongComponent } from './add-song/add-song.component';
import { MyOstComponent } from './my-ost/my-ost.component';
import { NavigationComponent } from './navigation/navigation.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { ChangeOSTComponent } from './change-ost/change-ost.component';
import { CartComponent } from './cart/cart.component';
import { BasketComponent } from './basket/basket.component';

@NgModule({
  declarations: [
    AppComponent,
    UnloggedComponent,
    LoginComponent,
    RegisterComponent,
    EmailVerifyComponent,
    LoggedHomeComponent,
    SettingsComponent,
    AddSongComponent,
    MyOstComponent,
    NavigationComponent,
    NotificationsComponent,
    ChangeOSTComponent,
    CartComponent,
    BasketComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    FormsModule,
    FontAwesomeModule,
    RouterModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [CookieService,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
