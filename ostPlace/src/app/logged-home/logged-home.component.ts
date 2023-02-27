import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { faUser, faArrowCircleRight, faArrowCircleLeft , faCartShopping, faCog, faCompactDisc, faFolderPlus, faBell, faPowerOff, faBars, faPlayCircle } from '@fortawesome/free-solid-svg-icons';
import { CookieService } from 'ngx-cookie-service';
import { SongService } from '../song.service';

@Component({
  selector: 'app-logged-home',
  templateUrl: './logged-home.component.html',
  styleUrls: ['./logged-home.component.scss']
})

export class LoggedHomeComponent implements OnInit, AfterViewInit {
  @ViewChild('audio') audio!:ElementRef;
  @ViewChild('audioBox') audioBox!:any;
  @ViewChild('title') title!:ElementRef;

  // FONT AWESOME ICONS
  userIcon = faUser;
  cart = faCartShopping;
  cog = faCog;
  disc = faCompactDisc;
  plus = faFolderPlus;
  bell = faBell;  
  logout = faPowerOff;
  bars = faBars;
  arrowRight = faArrowCircleRight;
  arrowLeft = faArrowCircleLeft;


  playHover = faPlayCircle;
  tagList:any;
  hovered:boolean = false;
  clickedOST:boolean = false;
  OSTChecking:any;
  pickedTags:any = [];
  searchTagsInputValue:any;

  checkingOSTId:any;
  //pagination and get array
  songs:any;
  pageNum = 1;

  //MUSIC PLAYER
  isPlaying = false;
  settedMusic:any = '';
  

  constructor(
    private _OSTS:SongService,
  ) { 
    this._OSTS.getTags().subscribe(
      Response => {
        this.tagList = Response.slice(0, 12);
        // this.tagList = this.tagList[1:12];
      }, error =>{
        console.log(error);
      }
    )
  }

  ngOnInit(): void {
    this._OSTS.getOSTS(this.pageNum).subscribe(
      Response =>{
        this.songs = Response;
      }, error =>{
        console.log(error);
      }
    )

  }

  ngAfterViewInit(): void { 

  }
  FilterOSTS(){
    this._OSTS.filterOSTS(this.pickedTags).subscribe(
      Response =>{
        this.songs = Response;
      }, error =>{
        console.log(error);
      }
    )
  }
  clickTag(id:number){
    if(!this.pickedTags.includes(this.tagList[id]['name'])){
      if(this.pickedTags.length >= 4){
        alert('You cant assign more than 4 tags');
      }else if(this.pickedTags.length <= 3){
        //Put clicked tag into choosed tags
        this.pickedTags.push(this.tagList[id]['name']);
        this.FilterOSTS();
      }else{
        alert('error');
        this._OSTS.getMyOSTS().subscribe(
          Response =>{
            this.songs = Response;
          }, error =>{
            console.log(error);
          }
        )
      }
    }else{
      alert('This tag is already in use');
    }
  }
  // LOGGED HOME FUNCTIONS
  playAudio(audioSRC:any, titleOST:any){
    if(this.settedMusic == false){
      this.isPlaying = true;
      this.title.nativeElement.innerHTML = titleOST;
      this.audioBox.nativeElement.src = audioSRC;

      this.audioBox.nativeElement.play();
    }else if(this.settedMusic == true){
      this.isPlaying = false;
      this.audio.nativeElement.pause();
    }
    

  }

  checkOST(id:Number){
    this.clickedOST = !this.clickedOST;
    this._OSTS.getOST(id).subscribe(
      Response =>{
        this.OSTChecking = Response;
      }, error =>{
        console.log(error);
      }
    )
    
  }

  exitOST(){
    this.clickedOST = !this.clickedOST;
    
  }
  filterTags(event:any){
    if(event.key == 'Enter'){
      console.log(event);
    }
    console.log(this.searchTagsInputValue);
    this._OSTS.filterTags(this.searchTagsInputValue).subscribe(
      Response =>{
        this.tagList = Response;
      }, error =>{
        console.log(error);
      }
    )
  }
  clickChoosedTag(id:number){
    if(id==0){
      this.pickedTags.shift();
      this._OSTS.getMyOSTS().subscribe(
        Response =>{
          this.songs = Response;''
        }, error =>{
          console.log(error);
        }
      )
    }else if(id == this.pickedTags.length-1){
      this.pickedTags.splice(-1);
      this.FilterOSTS();
    }else{
      this.pickedTags.splice(id,id);
      this.FilterOSTS();
    }
  }

 addToBasket(){
  let body = new FormData();
  body.append('ostId', this.OSTChecking.id);
  return this._OSTS.addToBasket(body).subscribe(
    Response =>{
      console.log(Response);
      alert('added to basket.');
    }, error =>{
      alert("You've already added that into basket earlier or your basket is full.")
    }
  )
 }
}
