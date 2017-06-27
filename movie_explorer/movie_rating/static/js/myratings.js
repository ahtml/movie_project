//------For the stars---------
function highlightStar(obj,id) {
	removeHighlight(id);
	$('#stars-new-'+id+' li').each(function(index) {
		$(this).addClass('highlight');
		if(index == $('#stars-new-'+id+' li').index(obj)) {
			return false;
		}
	});
}

function removeHighlight(id) {
	$('#stars-new-'+id+' li').removeClass('selected');
	$('#stars-new-'+id+' li').removeClass('highlight');
}

function addRating(obj,id) {
	$('#stars-new-'+id+' li').each(function(index) {
		$(this).addClass('selected');
		$('#stars-new-'+id+' #rating').val((index));
		if(index == $('#stars-new-'+id+' li').index(obj)) {
			return false;
		}
	});
    var rating = $('#stars-new-' + id + ' #rating').val();
    console.log(rating);
    $.ajax({
        method: 'POST',
        data: {
            csrfmiddlewaretoken: document.cookie.split('=')[1],
            action: "rate_movie",
            rating: rating,
            movie_id: id,
        },
		success: function(){
            var movie_list = $('#id-movie-rating');
            movie_list.load(' #id-movie-rating', function (){
                movie_list.children('#id-movie-rating').unwrap();
            });
        }
    });
    // if (rating == 0){
     //    // From http://stackoverflow.com/questions/8075463/in-ajax-data-is-deleted-from-database-but-disappear-from-screen-when-refreshed
     //    if (http.status == 200) { //on successful server response
     //        location.reload();
     //    }
     //    location.href="/myratings/";
    //
	// }
}

function resetRating(id) {
	if($('#stars-new-'+id+' #rating').val() != 0) {
		$('#stars-new-'+id+' li').each(function(index) {
			$(this).addClass('selected');
			if((index) == $('#stars-new-'+id+' #rating').val()) {
				return false;
			}
		});
	}
}