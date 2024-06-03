document.addEventListener('DOMContentLoaded', () => {
    let sortSelect = document.querySelector('#sortSelect');

    sortSelect.addEventListener('change', function () {
        window.location.href = this.value;
    });

    document.querySelectorAll('.home-card').forEach(card => {
        card.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-href');
        });
    });

    document.querySelectorAll('.card-author, .file-download-button, .dropdown-btn, .dropdown-item').forEach(element => {
        element.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    let isFetchingPosts = false;
    let page = 1;
    let hasMorePosts = true;

    const postsContainer = document.getElementById('posts-container');
    // Creating a sentinel element to observe
    const sentinel = document.createElement('div');
    postsContainer.appendChild(sentinel);

    function fetchPosts() {
        console.log('Fetching posts:', page);  // Log the current page before fetching
        if (isFetchingPosts || !hasMorePosts) {
            console.log('Fetch prevented:', isFetchingPosts, hasMorePosts);
            return;
        }
        isFetchingPosts = true;

        const nextPage = page + 1;
        const url = new URL(window.location.href);
        url.searchParams.set('page', nextPage);

        axios.get(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                const html = response.data.html;
                hasMorePosts = response.data.has_more;  // Update based on server response
                console.log('Posts fetched:', nextPage, 'Has more posts:', hasMorePosts);
                if (html) {
                    sentinel.insertAdjacentHTML('beforebegin', html);
                    page = nextPage;
                } else {
                    console.log('No more posts to fetch, disconnecting observer.');
                    observer.disconnect();  // Stop observing if no more posts
                }
            })
            .catch(error => {
                console.error('Error fetching posts:', error);
            })
            .finally(() => {
                isFetchingPosts = false;
                console.log('Fetch complete, isFetching reset.');
            });
    }

    const observer = new IntersectionObserver(entries => {
        // Check if the sentinel is currently visible in the viewport
        if (entries[0].isIntersecting) {
            console.log('Sentinel visible, triggering fetch');
            fetchPosts();
        }
    }, {
        rootMargin: '50px',
        threshold: 0.1  // Adjust threshold to your needs
    });

    // Start observing the sentinel
    observer.observe(sentinel);
});