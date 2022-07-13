var google_api_key = "AIzaSyDh9y6QlDDx3Ij9TYBty21KxNASjwg_wpc"; // upwrdz
var google_api_server_key = "AIzaSyBAxux0qqKXcy2SpY8-7mHmSoHE-5_9U5M"; // upwrdz
var current_pincode = null;

// Intializing the Google Map
function initMap(){
  var geocoder = new google.maps.Geocoder;
  if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function (position) {
              var accuracy = position.coords.accuracy;
              geocodeLatLng(geocoder,position.coords.latitude,position.coords.longitude)
              get_postal_code(position.coords.latitude, position.coords.longitude, function(postal_code) {
                  if(current_pincode == null){
                    current_pincode = postal_code.postalCodes[0].postalCode;
                    $('#current_pincode').val(current_pincode);
                  }
                  //Commented for future use
                  // console.log("postal_code",postal_code.postalCodes[0].postalCode);
                  // console.log("Place ",postal_code.postalCodes[0].adminName2);
                  // $('#place_name').text(postal_code.postalCodes[0].adminName2);
                  // if($('#postal_code').text() == "z"){
                  //     $('#postal_code').text(postal_code.postalCodes[0].postalCode);
                  // }
              });
          }, function error(msg){
              alert('Please enable your GPS position feature.');
          }, {
              maximumAge:600000,
              timeout:5000,
              enableHighAccuracy: true
          });
      } else {
          alert('Geo Location feature is not supported in this browser.');
      }
}

// Getting Longitude and Latitude of user
function geocodeLatLng(geocoder, latlat,lnglng) {
    var latlng = {lat: parseFloat(latlat), lng: parseFloat(lnglng)};
    var postal_array = {};
    geocoder.geocode({'location': latlng}, function(results, status) {
        if (status === 'OK') {
            if (results[0]) {
                var arr = _.filter(results[0].address_components, function(crr){
                    _.filter(crr, function(num){
                        if(num.constructor === Array){
                            if(_.contains(num,'postal_code')){
                                postal_array = crr;
                            }
                        }
                    });
                    if(postal_array['long_name']){
                        postal_array = postal_array['long_name'];
                        current_pincode = postal_array;
                        $('#current_pincode').val(current_pincode);
                    }
                });
            } else {
            window.alert('No results found');
            }
        } else {
        window.alert('Geocoder failed due to: ' + status);
        }
    });
    return postal_array;
}

// Getting User current Location Pincode
var get_postal_code = function (lat, long, cb){
    var username = "kantanand";
    var url = "/api/get-geo-location/?lat="+lat+"&lng="+long+"&key="+username;
    $.getJSON(url, function(result){
      cb(result);
    });
};
