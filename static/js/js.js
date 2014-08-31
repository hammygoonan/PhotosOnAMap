(function($){

	var map = {}

	$(document).ready(function(){
		function initialize(center) {
			$.post('/get_center/', function(data){
				var mapOptions = {
					center: new google.maps.LatLng(data.lat, data.lng),
					zoom: 6,
				//	scrollwheel: false,
					styles: [ { stylers : [
						{ "saturation": -100 },
						{ "lightness": 0 },
						{ "gamma": 0.5 }
					] } ]
				};
				map = new google.maps.Map(document.getElementById("map"), mapOptions);
				$.post('/get_markers/', function(data){
					$(data.markers).each(function(){
						if(this.latlng){
							var marker = new google.maps.Marker({
								position: new google.maps.LatLng(this.latlng.lat, this.latlng.lng),
								map: map,
								title: this.name
							});
						}
					})
				});
			});
		}
		google.maps.event.addDomListener(window, 'load', initialize);

	});
})(jQuery)
