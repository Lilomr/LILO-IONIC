import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpService } from './http.service';

interface Publicacao {
  conteudo: string;
}

@Injectable({
  providedIn: 'root'
})
export class PublicacaoService {

  constructor(private http: HttpService){ }

  async listar(): Promise<any> {
    return await this.http.get('http://localhost:5000/api/publicacoes');
  }
  async publicar(publicacao: Publicacao){
    return await this.http.post('http://localhost:5000/api/publicar', publicacao);
  }
}
