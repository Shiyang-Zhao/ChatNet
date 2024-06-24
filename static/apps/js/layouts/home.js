import { handlePostSaveAndUnsaveButton } from "../../../components/js/posts/post_dropdown.js";
import { handlePostLikeAndDislikeButton } from "../../../components/js/posts/post_like_and_dislike_button.js";
import { handleStoryShowAndHideButton } from "../../../components/js/stories/story_item.js";

document.addEventListener('DOMContentLoaded', () => {
    const storiesContainer = document.querySelector('#stories-container');
    const sortSelect = document.querySelector('#sort-select');
    const postsContainer = document.querySelector('#posts-container');

    handleStoryShowAndHideButton(storiesContainer);
    handlePostSaveAndUnsaveButton(postsContainer);
    handlePostLikeAndDislikeButton(postsContainer);

    sortSelect.addEventListener('change', function () {
        window.location.href = this.value;
    });

    document.body.addEventListener('click', function (event) {
        if (event.target.matches('.dropdown-btn, .dropdown-btn *, .dropdown-item, .dropdown-menu, .card-author, .file-video, .file-download')) {
            event.stopPropagation();
            return;
        }
        const card = event.target.closest('.post-container');
        if (card) {
            window.location.href = card.getAttribute('data-href');
        }
    });

    document.body.addEventListener('mousedown', function (event) {
        if (event.button === 1) {
            const card = event.target.closest('.post-container');
            if (card) {
                window.open(card.getAttribute('data-href'), '_blank');
            }
        }
    });

});

document.addEventListener('DOMContentLoaded', function () {
    let isFetchingPosts = false;
    let page = 1;
    let hasMorePosts = true;

    const postsContainer = document.querySelector('#posts-container');
    const sentinel = document.createElement('div');
    sentinel.id = 'sentinel';
    postsContainer.appendChild(sentinel);

    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
            console.log("Sentinel is intersecting");
            fetchPosts();
        }
    }, {
        rootMargin: '50px',
        threshold: 0.2
    });

    observer.observe(sentinel);

    function fetchPosts() {
        if (isFetchingPosts || !hasMorePosts) {
            console.log("Fetching is already in progress or no more posts to fetch.");
            return;
        }
        console.log("Fetching posts:", page);
        isFetchingPosts = true;

        const nextPage = page + 1;
        const url = new URL(window.location.href);
        url.searchParams.set('page', nextPage);

        axios.get(url.toString(), {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        }).then(response => {
            const posts_html = response.data.posts_html;
            hasMorePosts = response.data.has_more;
            console.log("Posts fetched:", nextPage, "Has more posts:", hasMorePosts);
            if (posts_html) {
                sentinel.insertAdjacentHTML('beforebegin', posts_html);
                page = nextPage;
            } else {
                console.log("No more posts to fetch, disconnecting observer.");
                observer.disconnect();
            }
        }).catch(error => {
            console.error('Error fetching posts:', error);
        }).finally(() => {
            isFetchingPosts = false;
            console.log('Fetch complete, isFetching reset.');
        });
    }
});

