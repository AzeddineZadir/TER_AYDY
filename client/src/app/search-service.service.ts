import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';


const httpOptions = {
  headers: new HttpHeaders({
    "Access-Control-Allow-Methods": "GET,POST",	  
    "Access-Control-Allow-Headers": "Content-type",  
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  })
};
@Injectable({
  providedIn: 'root'
})
export class SearchServiceService {
  private baseURL: string = "http://localhost:5000/";
  constructor(private http: HttpClient) { }

  search(request): Observable<any> {
    return this.http.post(this.baseURL+'releated', JSON.stringify(request), httpOptions);
}
}
