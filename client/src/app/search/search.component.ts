import { analyzeAndValidateNgModules } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { SearchServiceService } from '../search-service.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  public region: String = "";
  public wifi: boolean = true;
  public park: boolean = false;
  public clim: boolean = false;
  public adapt: boolean = false;
  public spa: boolean = false;
  public piscine: boolean = false;
  public espacev: boolean = false;
  public centreF: boolean = false;
  public dej: boolean = false;
  public souhait: string = "";
  public requete: any = [];
  public id:any = -1
  public hotels:any = [];
  public recherche:boolean = false;
  constructor(private searchService: SearchServiceService) { }

  ngOnInit(): void {
  }
  setRegion(value: any) {
    this.region = value.target.value


  }
  checkWifi(event) {
    this.wifi = event.target.checked
  }

  checkSpa(event) {
    this.wifi = event.target.checked
  }
  checkDej(event) {
    this.spa = event.target.checked
  }
  checkCentre(event) {
    this.centreF = event.target.checked
  }
  checkEspace(event) {
    this.espacev = event.target.checked
  }
  checkPiscine(event) {
    this.piscine = event.target.checked
  }
  checkAdapt(event) {
    this.adapt = event.target.checked
  }
  checkClim(event) {
    this.clim = event.target.checked
  }
  checkPark(event) {
    this.park = event.target.checked
  }

  setSouhait(event) {
    this.souhait = event.target.value
  }

  rechercher(id) {
    this.id = id
    this.recherche = true;
    this.requete =[]
    console.log(this.souhait)
    this.requete.push({ souhait: this.souhait })
    let selectors = []
    if(this.wifi == true){
      selectors.push("wifi")
    }
    if(this.park == true){
      selectors.push("parking")
    }
    if(this.clim == true){
      selectors.push("climatisation")
    }
    if(this.adapt==true){
      selectors.push("jeu")
    }
    if(this.spa== true)
    selectors.push("spa")
    if(this.piscine== true)
    selectors.push("piscine")
    if(this.espacev== true)
    selectors.push("espace vert")
    if(this.centreF== true)
    selectors.push("sport")
    if(this.dej== true)
    selectors.push("dejeuner")
    this.requete.push({ selector: selectors })
    this.requete.push({id:id})
    let req = JSON.stringify(this.requete)
    console.log(req)
    this.searchService.search(this.requete).subscribe(values => {
      this.recherche=false
      console.log(values)
      this.hotels=values
    })
  }
}
