import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Team {
  id: number;
  email: string;
  nickname: string;
  password: string;
  picture: string
}

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  url = environment.apiServerUrl;
  public items: {[key: number]: Team} = {};

  constructor(private auth: AuthService, private http: HttpClient) { }


  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getDrinks() {
   
    if (this.auth.can('get:manager')) {
      
      this.http.get(this.url + '/users', this.getHeaders())
      .subscribe((res: any) => {console.log(res.users)
        this.drinksToItems(res.users);
        console.log(res);
      });
    } else if (this.auth.can('get:barista')){
      this.http.get(this.url + '/users/baristas', this.getHeaders())
      .subscribe((res: any) => {
        this.drinksToItems(res.users);
        console.log(res);
      });
    }
  }

  saveDrink(drink: Team) {
    if (drink.id != -1) { // patch
      this.http.patch(this.url + '/users/' + drink.id, drink, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.getDrinks();
        }
      });
    } else { // insert
      this.http.post(this.url + '/users', drink, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.getDrinks();
        }
      });
    }
  }

  saveDrink2(drink: Team) {
    if (drink.id != -1) { // patch
      this.http.patch(this.url + '/users/' + drink.id, drink, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.getDrinks();
        }
      });
    } else { // insert
      this.http.post(this.url + '/users/baristas', drink, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.getDrinks();
        }
      });
    }
  }


  deleteDrink(drink: Team) {
    delete this.items[drink.id];
    this.http.delete(this.url + '/users/' + drink.id, this.getHeaders())
    .subscribe( (res: any) => {

    });
  }

  drinksToItems( drinks: Array<Team>) {
    for (const drink of drinks) {
      this.items[drink.id] = drink;
    }
  }
}