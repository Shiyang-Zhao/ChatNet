document.addEventListener('DOMContentLoaded', () => {
    const progressBarSegments = document.querySelectorAll('.progress-bar');
    const stories = document.querySelectorAll('.story-content');
    const modal = document.getElementById('storyModal');
    const leftArea = document.querySelector('.left-area');
    const rightArea = document.querySelector('.right-area');
    const defaultStoryDuration = 3000;
    let currentStoryIndex = 0;
    let storyTimer;

    progressBarSegments.forEach(segment => {
        Object.assign(segment.style, {
            width: '100%',
            marginRight: '5px',
            background: 'linear-gradient(to right, rgba(255, 255, 255, 1) 50%, rgba(255, 255, 255, 0.5) 50%)',
            backgroundSize: '200% 100%',
            backgroundPosition: 'right center'
        });
    });

    leftArea.addEventListener('click', () => navigateStory(-1));
    rightArea.addEventListener('click', () => navigateStory(1));

    modal.addEventListener('shown.bs.modal', () => {
        startStory(currentStoryIndex);
    });
    modal.addEventListener('hidden.bs.modal', () => {
        clearTimeout(storyTimer);
        resetProgressBars();
        stories.forEach(story => story.style.display = 'none');
        if (currentStoryIndex >= stories.length - 1) {
            currentStoryIndex = 0;
            stories[0].style.display = 'block';
        }
    });

    function navigateStory(direction) {
        let newIndex = currentStoryIndex + direction;
        if (newIndex >= 0 && newIndex < stories.length) {
            clearTimeout(storyTimer);
            currentStoryIndex = newIndex;
            startStory(currentStoryIndex);
        }
    }

    function resetProgressBars() {
        progressBarSegments.forEach(segment => {
            segment.style.transition = 'none';
            segment.style.backgroundPosition = 'right center';
        });
    }

    function animateProgressBar(index, duration) {
        setTimeout(() => {
            progressBarSegments[index].style.transition = `background-position ${duration}ms linear`;
            progressBarSegments[index].style.backgroundPosition = 'left center';
        }, 10);
    }

    function startStory(index) {
        // First, show the current story
        stories[index].style.display = 'block';

        // Then, hide all other stories
        stories.forEach((story, idx) => {
            if (idx !== index) {
                story.style.display = 'none';
            }
        });

        let video = stories[index].querySelector('video');
        if (video) {
            const videoStoryDuration = video.duration ? video.duration * 1000 : defaultStoryDuration;
            resetProgressBars();
            animateProgressBar(index, videoStoryDuration);
            startStoryTimer(index, videoStoryDuration);
        } else {
            resetProgressBars();
            animateProgressBar(index, defaultStoryDuration);
            startStoryTimer(index, defaultStoryDuration);
        }
    }

    function startStoryTimer(index, duration) {
        clearTimeout(storyTimer);
        storyTimer = setTimeout(() => {
            if (index + 1 < stories.length) {
                currentStoryIndex = index + 1;
                startStory(currentStoryIndex);
            }
        }, duration);
    }
});