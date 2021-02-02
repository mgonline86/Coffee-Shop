import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { DrinkMenuPage } from './drink-menu.page';
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { DrinkFormComponent2 } from './drink-form2/drink-form.component';

const routes: Routes = [
  {
    path: '',
    component: DrinkMenuPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [DrinkFormComponent,DrinkFormComponent2],
  declarations: [DrinkMenuPage, DrinkFormComponent,DrinkFormComponent2],
})
export class DrinkMenuPageModule {}
