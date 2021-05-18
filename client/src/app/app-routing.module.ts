import { NgModule } from '@angular/core';
import { SearchComponent } from './search/search.component';
import { Routes, RouterModule } from '@angular/router';
const routes: Routes = [
  {
    path : 'search',
    component:SearchComponent
  }
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
