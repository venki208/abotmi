angular.module('reiaapp.services', [])
 .service('mainServices', mainServices);
 
 function mainServices(){
    var otp=0;
    var data_update='';
    return {
        setItem: function(value){
            otp = value;
        },
        getItem: function(){
            return otp;
        },
        resetItem: function(){
            otp = 0;
            return otp;
        },

        DataUpdate: function(value1){
            data_update = value1;
        },
        DataUpdateItem: function(){
            return data_update;
        },
        DataUpdateResetItem: function(){
            data_update = '';
            return data_update;
        }
    }
 }

 