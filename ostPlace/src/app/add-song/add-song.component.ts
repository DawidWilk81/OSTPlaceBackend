import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { faXmark, faCircleCheck } from '@fortawesome/free-solid-svg-icons';
import { SongService } from '../song.service';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';



@Component({
  selector: 'app-add-song',
  templateUrl: './add-song.component.html',
  styleUrls: ['./add-song.component.scss']
})
export class AddSongComponent implements OnInit {
  @ViewChild('tags') tags!:ElementRef;
  searchTagsInputValue = ''
  getTags = false;
  choosedTags:any = [];
  FilteredTags:any = [];
  filterFunction:any;
  song:any;
  songSize:any;
  xmark=faXmark;
  checkMark=faCircleCheck;
  imageUrl:any;
  tagList:any = [];
  ostError:boolean = false;
  ostGood:boolean = false;
  coverError:boolean = false;
  coverGood:boolean = false;
  coverSizeError:boolean = false;

  //coverValues
  imgWidth:any;
  imgHeight:any;

  constructor(  
    private _OSTS:SongService,
    private _router:Router,
    private _renderer2:Renderer2
  ) { }

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
      title: '',
      ostFile: File,
      cover: File,
      desc: '',
      tags: '',
      price: ''
    }
  }

  showTags(){
    this.getTags = !this.getTags;
  }

  ConfirmTags(){
    this.getTags = !this.getTags;
  }

  hideTags(){
      this.getTags = false;
      this.choosedTags = [];
  }

  //FILTER FUNCTION
  filterTags(event:any){
    if(event.key == 'Enter'){
      console.log(event);
    }
    console.log(this.searchTagsInputValue);
    this._OSTS.filterTags(this.searchTagsInputValue).subscribe(
      Response =>{
        this.FilteredTags = Response;
      }, error =>{
        console.log(error);
      }
    )
  }

  //APPEND CHOOSED TAGS
  clickTag(id:number){
    console.log(id);
    if(!this.choosedTags.includes(this.tagList[id]['name'])){
      if(this.choosedTags.length === 4){
        alert('You cant assign more than 4 tags');
      }else if(this.choosedTags.length <= 3){
        this.choosedTags.push(this.tagList[id]['name']);
      }else{
        alert('error');
      }
    }else{
      alert('This tag is already in use');
    }
  }

  clickChoosedTag(id:number){
    if(id==0){
      this.choosedTags.shift();
    }else{
      this.choosedTags.splice(id, id);
    }
    console.log(id);
  }

  onImageChange(event:any){
    if(event.target.files[0].name.endsWith('.jpg') || event.target.files[0].name.endsWith('.png') ){
      let x = event.target.files;
      let reader = new FileReader();
      reader.readAsDataURL(x[0]);
      reader.onload=(event:any)=>{
        console.log(event);
        let cover = new Image();
        cover.src = event.target.result;

        cover.onload = () => {
          this.imgWidth = cover.width;
          this.imgHeight = cover.height;
          console.log(this.imgWidth, 'h', this.imgHeight);
          if(this.imgWidth > 2000 || this.imgHeight > 3000){
            this.coverSizeError = true;
          }else{
            this.coverSizeError = false;
            this.song.cover = event.target.files[0];
          }
          this.imageUrl = event.target.result;
        }

      }
      this.coverError = false;
      this.coverGood = true;
    }else{
      this.coverError = true;
      this.coverGood = false;
    }



  }

  onSongChange(event:any){
    console.log(event.target.files[0]);
    let check = event.target.files[0].name;
    let check2 = event.target.files[0].size;
    this.songSize = check2;
    console.log(event.target.files[0].size);
    if(check.endsWith('.mp3') || check.endsWith('.wav')){
      this.song.ostFile = event.target.files[0];
      this.ostError = false;
      this.ostGood = true;
    }else{
      this.ostError = true;
      this.ostGood = false;
    }
  }

  sendSong(addSongForm:NgForm){
    console.log(this.choosedTags.length);
    if(this.choosedTags.length == 0){
      console.log('You need to assign tags');
      alert('I found no tags in request');
      this._renderer2.setStyle(this.tags.nativeElement, "color", "red")
    }else{
      console.log(addSongForm);
      let body = new FormData;
      body.append('title', this.song.title);
      body.append('desc', this.song.desc);
      body.append('ost', this.song.ostFile);
      body.append('cover', this.song.cover);
      body.append('tags', this.choosedTags);
      body.append('price', this.song.price);
      
      this._OSTS.sendOST(body).subscribe(
        Response =>{
          console.log(Response);
          alert('Wyslano');
          this._router.navigateByUrl('home');
        }, error =>{
          console.log(error);
        }
      )
    }
  } 
}
