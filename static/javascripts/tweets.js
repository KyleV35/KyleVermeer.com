$(document).ready(function(){
})

function get_tweets(screen_name_user, num_tweets, tweet_box_id) {
    var tweet_box= $("#"+tweet_box_id)
    $.ajax({
        type:'GET',
        dataType: 'jsonp',
        url: 'https://api.twitter.com/1/statuses/user_timeline.json',
        data: {screen_name: screen_name_user, count: num_tweets, include_rts:1},
        success: function(data) {
            numTweets= data.length
            for (var i=0; i < numTweets; i++) {
                parsedTweet= data[i].text.parseURL().parseUsername().parseHashtag()
                tweet_box.append('<p class="tweet_item">'+ (i+1)+ ". " +parsedTweet + "</p>")
                tweet_box.append('<p class="padLeft10px">---------------------------------------------------------------------</p>')
            }
        },
        error: function(data) {
            alert("There was an error with the tweet")
        }
    })
}

String.prototype.parseURL = function() {
	return this.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&~\?\/.=]+/g, function(url) {
		return url.link(url);
	});
};

String.prototype.parseUsername = function() {
	return this.replace(/[@]+[A-Za-z0-9-_]+/g, function(u) {
		var username = u.replace("@","")
		return '<a href="http://twitter.com/'+username+'"><span class="tweet_blue">'+u+'<span></a>'
	});
};


String.prototype.parseHashtag = function() {
	return this.replace(/[#]+[A-Za-z0-9-_]+/g, function(t) {
		var tag = t.replace("#","%23")
		return '<a href="http://search.twitter.com/search?q='+tag+'"><span class="tweet_blue">'+t+'</span></a>'
	});
};