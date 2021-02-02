import { Component, OnInit } from '@angular/core';
import { TeamService, Team } from '../../services/team.service';
import { ModalController } from '@ionic/angular';
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { DrinkFormComponent2 } from './drink-form2/drink-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-drink-menu',
  templateUrl: './drink-menu.page.html',
  styleUrls: ['./drink-menu.page.scss'],
})
export class DrinkMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public drinks: TeamService
    ) { }

  ngOnInit() {
    this.drinks.getDrinks();
  }

  form(activedrink: Team = null){
    if(this.auth.can('get:manager')) {
      this.openForm(activedrink);
    }
    else{
    this.openForm2(activedrink);}

  }

  async openForm(activedrink: Team = null) {
    if (!this.auth.can('get:manager')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: DrinkFormComponent,
      componentProps: { drink: activedrink, isNew: !activedrink }
    });

    modal.present();
  }

  async openForm2(activedrink: Team = null) {
    if (!this.auth.can('get:barista')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: DrinkFormComponent2,
      componentProps: { drink: activedrink, isNew: !activedrink }
    });

    modal.present();
  }

}
