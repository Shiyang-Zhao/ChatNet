document.addEventListener('DOMContentLoaded', () => {
    const defaultStoryDuration = 3000;

    const storyContainers = document.querySelectorAll('.story-container');
    storyContainers.forEach(storyContainer => {
        let currentStoryIndex = 0;
        let storyTimer;

        const progressBarSegments = storyContainer.querySelectorAll('.progress-bar');
        const stories = storyContainer.querySelectorAll('.story-content');
        const modals = storyContainer.querySelectorAll('.profile-modal');
        const leftAreas = storyContainer.querySelectorAll('.left-area');
        const rightAreas = storyContainer.querySelectorAll('.right-area');

        // Initialize stories and progress bar styles
        progressBarSegments.forEach(segment => {
            Object.assign(segment.style, {
                width: '100%',
                marginRight: '5px',
                background: 'linear-gradient(to right, rgba(255, 255, 255, 1) 50%, rgba(255, 255, 255, 0.5) 50%)',
                backgroundSize: '200% 100%',
                backgroundPosition: 'right center'
            });
        });

        stories.forEach((story, idx) => {
            story.style.display = idx === currentStoryIndex ? 'block' : 'none';
        });

        leftAreas.forEach(leftArea => {
            leftArea.addEventListener('click', () => navigateStory(-1));
        });

        rightAreas.forEach(rightArea => {
            rightArea.addEventListener('click', () => navigateStory(1));
        });

        modals.forEach(modal => {
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
            stories.forEach((story, idx) => {
                story.style.display = idx === currentStoryIndex ? 'block' : 'none';
            });
            stories[index].style.display = 'block';

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
});
