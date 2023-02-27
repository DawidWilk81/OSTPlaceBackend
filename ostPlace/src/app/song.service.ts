import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class SongService {
  token = this._cookies.get('token');
  tags:any;
  OST:any;

  headers = new HttpHeaders(
    {
      'Authorization': `Token ${this.token}`
    }
  );
  
  backEndUrl = 'http://localhost:8000/';
  constructor(
    private _http:HttpClient,
    private _cookies:CookieService
  ) { }

  addToBasket(body:any):Observable<any>{
    return this._http.post(this.backEndUrl + 'api/userBasket/', body, {headers:this.headers})
  }

  GetTheBasket():Observable<any>{
    return this._http.get(this.backEndUrl + 'api/getUserBasket/', {headers: this.headers})
  }

  delItemBasket(id:any):Observable<any>{
    return this._http.delete(this.backEndUrl + `api/userBasket/${id}/`, {headers: this.headers})
  }

  sendOST(body:any):Observable<any>{
    return this._http.post(this.backEndUrl + 'api/ostAdd/', body, {headers:this.headers});
  }

  getOST(id:any):Observable<any>{
    return this._http.get(this.backEndUrl + `api/getOST/${id}/`, {headers:this.headers});
  }

  deleteOST(id:any):Observable<any>{
    let param:any = new HttpParams().set('primary', id);
    return this._http.delete(this.backEndUrl + `api/deleteOST/${id}/`, {headers:this.headers, params:param});
  }

  //UPDATE WHOLE OST 
  putOST(id:any, body:any):Observable<any>{
    let param:any = new HttpParams().set('primary', id);
    return this._http.put(this.backEndUrl + `api/updateOST/${id}/`, body, {headers:this.headers, params:param});
  }

  //UPDATE OST TAGS
  updateTags(id:any, tags:any):Observable<any>{
    return this._http.put(this.backEndUrl + `api/updateTagsOST/${id}/`, tags, {headers:this.headers})
  }

  getTags():Observable<any>{
    return this._http.get(this.backEndUrl + 'api/tags/');
  }

  getOSTS(pageNum:any):Observable<any>{
    let param:any = new HttpParams().set('pageNum', pageNum);
    return this._http.get(this.backEndUrl + 'api/ostPaginate/', {params: param, headers:this.headers});
  }
  getUnloggedOSTS():Observable<any>{
    return this._http.get(this.backEndUrl + 'api/getUnloggedOSTS/');
  }

  getMyOSTS():Observable<any>{
    return this._http.get(this.backEndUrl + 'api/myOSTS/', {headers: this.headers})
  }

  filterTags(searchCall:any):Observable<any>{
    let params:any = new HttpParams().set('search', searchCall);
    return this._http.get(this.backEndUrl + 'api/tagsFilter/', {params: params, headers:this.headers});
  }

  filterOSTS(tagsCall:any):Observable<any>{
    let params:any = new HttpParams().set('tags', tagsCall);
    return this._http.get(this.backEndUrl + 'api/filterOST/', {params: params, headers:this.headers})
  }

  // STRIPE PAY
  stripeCode(){
    return this._http.get(this.backEndUrl + 'api/stripeConf/', {headers:this.headers});
  }

}
