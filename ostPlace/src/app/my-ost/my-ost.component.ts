import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { SongService } from '../song.service';
import { faPen, faRemove } from '@fortawesome/free-solid-svg-icons';
import { Router } from '@angular/router';
import { faPlayCircle } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-my-ost',
  templateUrl: './my-ost.component.html',
  styleUrls: ['./my-ost.component.scss']
})
export class MyOstComponent implements OnInit {
  @ViewChild('audio') audio!:ElementRef;
  @ViewChild('audioBox') audioBox!:any;
  @ViewChild('title') title!:ElementRef;

  deleteAlert:boolean = false;
  OSTS:any;
  pen = faPen;
  remove = faRemove;
  id:any;
  modalPop:boolean = false;
  playHover = faPlayCircle
  //MUSIC PLAYER
  isPlaying:boolean = false;
  settedMusic:any = '';

  constructor(
    private _myOSTS: SongService,
    private _router:Router
  ) { }

  ngOnInit(): void {
    
    this._myOSTS.getMyOSTS().subscribe(    
    Response =>{
      console.table(Response);
      this.OSTS = Response;
    }, error =>{
      console.log(error);
    })
  }
  waitForSec = (time:any) => new Promise(x => setTimeout(x, time));
  toggleAlert(id:any){
    this.deleteAlert = !this.deleteAlert;
  }
  hideAlert(){
    this.deleteAlert = !this.deleteAlert;
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

  removeOST(){
    this._myOSTS.deleteOST(this.id).subscribe(
      Response =>{
        console.log(Response);
        this.modalPop = true;
        this.waitForSec(2000);
        location.reload();
        this.modalPop = false;
      }, error =>{
        console.log(error);
      }
    )
  }

}
