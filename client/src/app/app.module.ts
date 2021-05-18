import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';


import { AboutusComponent } from './aboutus/aboutus.component';
import { ContactusComponent } from './contactus/contactus.component';
import { SearchComponent } from './search/search.component';
import { FootercComponent } from './footerc/footerc.component';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    
    FootercComponent,
    AboutusComponent,
    ContactusComponent,
    SearchComponent
  ],
  imports: [ 
    HttpClientModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
