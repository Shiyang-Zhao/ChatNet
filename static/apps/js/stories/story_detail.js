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
                stories.forEach(story => {
                    story.style.display = 'none';
                    const video = story.querySelector('video');
                    if (video) {
                        video.pause();
                        video.currentTime = 0;
                    }
                });
                if (currentStoryIndex >= stories.length - 1) {
                    currentStoryIndex = 0;
                    stories[0].style.display = 'block';
                }
            });
        });

        function navigateStory(direction) {
            let newIndex = currentStoryIndex + direction;
            if (newIndex >= 0 && newIndex < stories.length) {
                // Pause the current video if it exists
                const currentVideo = stories[currentStoryIndex].querySelector('video');
                if (currentVideo) {
                    currentVideo.pause();
                }

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
                story.style.display = idx === index ? 'block' : 'none';
                if (idx === index) {
                    const video = story.querySelector('video');
                    if (video) {
                        video.currentTime = 0;
                        video.play().catch(error => {
                            console.log("Error auto-playing video:", error);
                            video.muted = true; // Handle the case where autoplay fails
                            video.play(); // Try playing again with mute enabled
                        });
                    }
                }
            });

            const video = stories[index].querySelector('video');
            const duration = video && video.duration ? video.duration * 1000 : defaultStoryDuration;

            resetProgressBars();
            animateProgressBar(index, duration);
            startStoryTimer(index, duration);
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
