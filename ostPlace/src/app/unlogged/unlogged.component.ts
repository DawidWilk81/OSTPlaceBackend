import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { faUser, faCartShopping, faPlayCircle  } from '@fortawesome/free-solid-svg-icons';
import { SongService } from '../song.service';
@Component({
  selector: 'app-unlogged',
  templateUrl: './unlogged.component.html',
  styleUrls: ['./unlogged.component.scss']
})
export class UnloggedComponent implements OnInit {
  @ViewChild('audio') audio!:ElementRef;
  @ViewChild('audioBox') audioBox!:any;
  @ViewChild('title') title!:ElementRef;

  userIcon = faUser;
  cart = faCartShopping;
  tags:any=[];
  songs:any;
  playHover = faPlayCircle
  //MUSIC PLAYER
  isPlaying:boolean = false;
  settedMusic:any = '';
  constructor(
    private _OSTS:SongService,
    private _router:Router
  ) { }

  ngOnInit(): void {
    this._OSTS.getTags().subscribe(
      Response =>{
        this.tags = Response;
        console.log(this.tags);
      }
    )
    this._OSTS.getUnloggedOSTS().subscribe(
      Response =>{
        this.songs = Response;
        console.log(Response);
      }, error =>{console.log(error)}
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

  GoTologIn(){
    this._router.navigateByUrl('login');
  }
}
