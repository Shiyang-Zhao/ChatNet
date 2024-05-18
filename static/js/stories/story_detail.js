document.addEventListener('DOMContentLoaded', () => {
    const progressBarSegments = document.querySelectorAll('.progress-bar');
    const stories = document.querySelectorAll('.story-content');
    const modal = document.getElementById('storyModal');
    const leftArea = document.querySelector('.left-area');
    const rightArea = document.querySelector('.right-area');
    const storyDuration = 3000;
    let currentStoryIndex = 0;
    let storyTimer;

    // Initialize progress bar styles directly
    progressBarSegments.forEach(segment => {
        Object.assign(segment.style, {
            width: '100%',
            marginRight: '5px',
            background: 'linear-gradient(to right, rgba(255, 255, 255, 1) 50%, rgba(255, 255, 255, 0.5) 50%)',
            backgroundSize: '200% 100%',
            backgroundPosition: 'right center'
        });
    });

    // Set up navigation listeners directly
    leftArea.addEventListener('click', () => navigateStory(-1));
    rightArea.addEventListener('click', () => navigateStory(1));

    modal.addEventListener('shown.bs.modal', () => startStory(currentStoryIndex));
    modal.addEventListener('hidden.bs.modal', resetStories);

    function startStory(index) {
        hideAllStories();
        displayStory(index);
        resetProgressBars();
        animateProgressBar(index);
        startStoryTimer(index);
    }

    function hideAllStories() {
        stories.forEach(story => story.style.display = 'none');
    }

    function displayStory(index) {
        stories[index].style.display = 'block';
    }

    function animateProgressBar(index) {
        setTimeout(() => {
            progressBarSegments[index].style.transition = `background-position ${storyDuration}ms linear`;
            progressBarSegments[index].style.backgroundPosition = 'left center';
        }, 10);
    }

    function resetProgressBars() {
        progressBarSegments.forEach(segment => {
            segment.style.transition = 'none';
            segment.style.backgroundPosition = 'right center';
        });
    }

    function startStoryTimer(index) {
        clearTimeout(storyTimer);
        storyTimer = setTimeout(() => {
            if (index + 1 < stories.length) {
                currentStoryIndex = index + 1;
                startStory(currentStoryIndex);
            }
        }, storyDuration);
    }

    function navigateStory(direction) {
        clearTimeout(storyTimer);
        let newIndex = currentStoryIndex + direction;
        if (newIndex >= 0 && newIndex < stories.length) {
            currentStoryIndex = newIndex;
            startStory(currentStoryIndex);
        }
    }

    function resetStories() {
        clearTimeout(storyTimer);
        resetProgressBars();
        currentStoryIndex = 0;
    }
});
