$(document).ready(function () {
    $('.like-btn, .dislike-btn').click(function () {
        var postId = $(this).data('post-id');
        var actionUrl = $(this).data('url');

        $.ajax({
            type: "POST",
            url: actionUrl,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                post_id: postId,  // You can remove this if your URL already includes the post ID
            },
            success: function (response) {
                if (response.success) {
                    $('#likes-count-' + postId).text(response.likes_count + ' Likes');
                    $('#dislikes-count-' + postId).text(response.dislikes_count + ' Dislikes');
                }
            },
            error: function () {
                alert('Error: Could not update post.');
            }
        });
    });
});