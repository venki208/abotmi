angular.module('mygrowth_factories',['mygrowth_constants'])
.factory('mygrowth_factory', function($http, $location,MYGROWTH_LIST, $q) {
    var domain_url = $location.protocol() + "://" + $location.host() + ":" + $location.port();
    return {
       get_advisor_list : get_advisor_list
    }

    function get_advisor_list(){
        var touchpromise="";
        var url = domain_url+MYGROWTH_LIST;
        var trans = $http({
            method : "POST",
            url : url,
            data : $.param({'req_type': "mobile" }),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).then(function(res){
            return res.data;
        },function(error){
            return $q.reject(error);
        });
        return trans;
    }
})
