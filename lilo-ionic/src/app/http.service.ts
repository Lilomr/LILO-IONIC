import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private http: HttpClient) { }
  
  async post(url:string,data:any){
    return await firstValueFrom(this.http.post(url,data));
  }
  
  async get(url:string){
    return await firstValueFrom(this.http.get(url));
  }
}
