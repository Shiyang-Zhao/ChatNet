document.addEventListener('DOMContentLoaded', () => {
    const progressBarSegments = document.querySelectorAll('.progress-bar');
    const stories = document.querySelectorAll('.story-content');
    const modal = document.getElementById('storyModal');
    const leftArea = document.querySelector('.left-area');
    const rightArea = document.querySelector('.right-area');
    let currentStoryIndex = 0;
    let storyTimer;
    const storyDuration = 3000; // Story duration in milliseconds

    // Function to show a specific story
    const showStory = (index) => {
        stories.forEach(story => story.style.display = 'none');
        stories[index].style.display = 'block';

        progressBarSegments.forEach((segment, idx) => {
            segment.style.transition = 'none';  // Disable transition initially
            segment.style.backgroundPosition = '100% center';  // Set all to unfilled state
        });

        setTimeout(() => {  // Delay to allow CSS to settle before starting animation
            progressBarSegments[index].style.transition = `background-position ${storyDuration}ms linear`;
            progressBarSegments[index].style.backgroundPosition = '0% center';  // Start animation for current segment
        }, 10);

        startStoryTimer(index);
    };

    // Timer to automatically progress stories
    const startStoryTimer = (index) => {
        if (storyTimer) clearTimeout(storyTimer);
        storyTimer = setTimeout(() => {
            const nextIndex = index + 1;
            if (nextIndex < stories.length) {
                showStory(nextIndex);
            } else {
                // Handle end of stories, maybe loop or close modal
            }
        }, storyDuration);
    };

    // Navigation through stories
    const navigateStory = (direction) => {
        const newIndex = currentStoryIndex + direction;
        if (newIndex >= 0 && newIndex < stories.length) {
            currentStoryIndex = newIndex;
            showStory(currentStoryIndex);
        }
    };

    leftArea.addEventListener('click', () => navigateStory(-1));
    rightArea.addEventListener('click', () => navigateStory(1));

    // Handle modal open event to start progress bar animation
    modal.addEventListener('shown.bs.modal', function () {
        if (stories.length > 0) {
            showStory(currentStoryIndex); // Start with the first story or current story
        }
    });

    modal.addEventListener('hidden.bs.modal', function () {
        if (storyTimer) {
            clearTimeout(storyTimer); // Stop the story timer
        }
        progressBarSegments.forEach(segment => {
            segment.style.transition = 'none';
            segment.style.backgroundPosition = '100% center';  // Reset progress bar to unfilled state
        });
        currentStoryIndex = 0; // Reset to the first story if desired
    });
});
