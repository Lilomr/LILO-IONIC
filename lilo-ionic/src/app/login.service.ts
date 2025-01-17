import { Injectable } from '@angular/core';
import { HttpService } from './http.service';

interface Login {
  email: string;
  senha: string;
}

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private http: HttpService) { }

  async logar(login: Login): Promise<any> {
    return await this.http.post('http://localhost:5000/api/login', login);
  }

}
