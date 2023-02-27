import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { SongService } from '../song.service';
import { faX } from '@fortawesome/free-solid-svg-icons';
@Component({
  selector: 'app-basket',
  templateUrl: './basket.component.html',
  styleUrls: ['./basket.component.scss']
})
export class BasketComponent implements OnInit {
  @ViewChild('audio') audio!:ElementRef;
  @ViewChild('audioBox') audioBox!:any;
  @ViewChild('title') title!:ElementRef;
  MyBasket:any;
  xSign = faX;
  tagList:any;

  //MUSIC PLAYER
  isPlaying = false;
  settedMusic:any = '';

  constructor(
    private _OSTS:SongService,
  ) { 
    this._OSTS.getTags().subscribe(
      Response =>{
        this.tagList = Response;
      }, error =>{
        console.log(error);
      }
    )
  }

  ngOnInit(): void {
    this._OSTS.GetTheBasket().subscribe(
      Response =>{
        this.MyBasket = Response;
        console.log('MY BASKET: ', this.MyBasket);
      }, error =>{
        console.log(error);
      }
    )
  }

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

  delItem(id:any){
   this._OSTS.delItemBasket(id).subscribe(
    Response =>{
      alert('item has been removed properly');
      window.location.reload();
    }, error =>{
      console.log(error);
    }
   )
  }

  stripeCode(){
    this._OSTS.stripeCode().subscribe(
      Response=>{
        console.log(Response);
      }, error =>{
        console.log(error);
      }
    );
  }
}
