angular.module('myidentity_services',[])

.service('MyidentityShareData',function(){
 var editshare=this;
 var getdata ={};

editshare.setdata = function(data){
    getdata = data;
}
 editshare.getdata = function(){
     return getdata;
 }
})
