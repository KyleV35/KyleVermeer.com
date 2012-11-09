$(document).ready(function(){
    addLikeButtons()
})

var addLikeButtons= function() {
    $('.like_button').click(function(){
        var me = $(this)
        var video_id= me.attr("videoID")
        var likes= me.prev()
        $.ajax({
            type:"POST",
            dataType: 'json',
            url:"/family/videos/like",
            data: { videoID: video_id },
            success: function(data) {
                var count= data
                likes.html("Likes: "+count)
            },
            error: function(data) {
                alert("There was an error with the like")
            }
        })
    })
}