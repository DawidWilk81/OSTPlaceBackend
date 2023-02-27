import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { faXmark } from '@fortawesome/free-solid-svg-icons';
import { SongService } from '../song.service';
import { NgForm } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-change-ost',
  templateUrl: './change-ost.component.html',
  styleUrls: ['./change-ost.component.scss']
})
export class ChangeOSTComponent implements OnInit {
  id:any;
  @ViewChild('tags') tags!:ElementRef;
  searchTagsInputValue = ''
  getTags = false;
  choosedTags:any = [];
  FilteredTags:any = [];
  filterFunction:any;
  song:any;
  xmark=faXmark;
  imageUrl:any;

  ostError:boolean = false;
  ostGood:boolean = false;
  coverError:boolean = false;
  coverGood:boolean = false;
  tagsSplitted:any;
  tagList:any = [];
  oldTags:any = []
  constructor(  
    private _OSTS:SongService,
    private _router:Router,
    private _renderer2:Renderer2,
    private _routes:ActivatedRoute,
  ) { 
    this.id = this._routes.snapshot.paramMap.get('id');
    console.log(this.id);
  }

  ngOnInit(): void {
    this._OSTS.getTags().subscribe(
      Response =>{
        this.tagList = Response;
        this.FilteredTags = Response;
        console.log(this.tagList);
      }, error =>{
        console.log(error);
      }
    )
    this.song = {
      id: Number,
      title: '',
      ost: File,
      cover: File,
      desc: '',
      price: '',
    }

    this._OSTS.getOST(this.id).subscribe(
      Response =>{
        this.song = Response;
        this.imageUrl = Response['cover'];
        this.song.tags = Response['tags']
        this.tagsSplitted = this.song.tags.toString().split(",", 5);
        console.log(this.tagsSplitted.length);
        for(let i=0; i<=this.tagsSplitted.length - 1; i++){
          let check = this.tagsSplitted[i];
          this.choosedTags.push(this.tagList[check]['name']);
          this.oldTags.push(this.tagList[check]['name']);
        }
        console.table(this.tagList);
      }, error =>{
        console.log(error);
      }
    )
  }

  showTags(){
    this.getTags = !this.getTags;
  }

  hideTags(){
    this.getTags = !this.getTags;
  }

  //FILTER FUNCTION
  filterTags(event:any){
    if(event.key != 'Delete' && event.key != 'Backspace'){    
    console.log(this.searchTagsInputValue);
    this._OSTS.filterTags(this.searchTagsInputValue).subscribe(
      Response =>{
        this.FilteredTags = Response;
      }, error =>{
        console.log(error);
      }
    )
  }
  }
  //APPEND CHOOSED TAGS
  clickTag(id:number){
    console.log(id);
    if(!this.choosedTags.includes(this.tagList[id]['name'])){
      if(this.choosedTags.length === 4){
        alert('You cant assign more than 4 tags');
      }else if(this.choosedTags.length <= 3){
        //Put clicked tag into choosed tags
        this.choosedTags.push(this.tagList[id]['name']);
      }else{
        alert('error');
      }
    }else{
      alert('This tag is already in use');
    }
  }


  onImageChange(event:any){
    if(event.target.files[0].name.endsWith('.jpg') || event.target.files[0].name.endsWith('.png') ){
      this.song.cover = event.target.files[0];
      this.coverError = false;
      this.coverGood = true;
    }else{
      this.coverError = true;
      this.coverGood = false;
    }

    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onload=(event:any)=>{
      this.imageUrl = event.target.result;
    }
  }
  clickChoosedTag(id:number){
    if(id==0){
      this.choosedTags.shift();
    }else if(id == this.choosedTags.length-1){
      this.choosedTags.splice(-1);
    }else{
      this.choosedTags.splice(id,id);
    }
    console.log(id);
  }
  onSongChange(event:any){
    let check = event.target.files[0].name;
    if(check.endsWith('.mp3') || check.endsWith('.wav')){
      this.song.ost = event.target.files[0];
      this.ostError = false;
      this.ostGood = true;
    }else{
      this.ostError = true;
      this.ostGood = false;
    }
  }


  updateSong(addSongForm:NgForm){
      console.log(this.choosedTags.length);
      console.log(addSongForm);
      let body = new FormData;
      body.append('title', this.song.title);
      body.append('desc', this.song.desc);
      body.append('price', this.song.price);
      if(this.song.ost instanceof File){
        body.append('ost', this.song.ost);
        console.log('songL', this.song.ost);
      }
      if(this.song.cover instanceof File){
        console.log('TYPE: ', typeof(this.song.cover));
        body.append('cover', this.song.cover);
        console.log(this.song.cover);
      }
      console.log('COVER: ', this.song.cover);
      console.log('OST: ', this.song.ost);

      this._OSTS.putOST(this.song.id, body).subscribe(
        Response =>{
          console.log(Response);
          alert('Wyslano');
          // this._router.navigateByUrl('home');
        }, error =>{
          console.log(error);
        }
      )
  }
  updateTags(){
    let body = new FormData;
    body.append('id', this.song.id);
    body.append('tags', this.choosedTags);
    this._OSTS.updateTags(this.song.id, body).subscribe(
      Response =>{
        console.log(Response);
        this.getTags = !this.getTags;
      }, error =>{
        console.log(error);
      }
    )
  }

  resetForm(){
    this._OSTS.getOST(this.id).subscribe(
      Response =>{
        this.song = Response;
        this.imageUrl = Response['cover'];
        this.song.tags = Response['tags']
        this.tagsSplitted = this.song.tags.toString().split(",", 5);
        console.log(this.tagsSplitted.length);
        for(let i=0; i<=this.tagsSplitted.length - 1; i++){
          let check = this.tagsSplitted[i];
          this.choosedTags.push(this.tagList[check]['name']);
          this.oldTags.push(this.tagList[check]['name']);
        }
        console.table(this.tagList);
      }, error =>{
        console.log(error);
      }
    )
  }
}


// UPDATE 