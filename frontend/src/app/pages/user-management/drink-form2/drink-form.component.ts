import { Component, OnInit, Input } from '@angular/core';
import { Team, TeamService } from 'src/app/services/team.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-drink-form',
  templateUrl: './drink-form.component.html',
  styleUrls: ['./drink-form.component.scss'],
})
export class DrinkFormComponent2 implements OnInit {
  @Input() drink: Team;
  @Input() isNew: boolean;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private drinkService: TeamService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.drink = {
        id: -1,
        email: '',
        nickname: '',
        password:'',
        picture:''
      };
    }
  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }


  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.drinkService.saveDrink2(this.drink);
    this.closeModal();
  }

  deleteClicked() {
    this.drinkService.deleteDrink(this.drink);
    this.closeModal();
  }
}
