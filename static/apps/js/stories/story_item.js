// document.addEventListener('DOMContentLoaded', () => {
//     const storiesContainer = document.querySelector('.stories-container');
//     const defaultStoryDuration = 3000;

//     storiesContainer.addEventListener('click', function (event) {
//         const button = event.target.closest('button[data-bs-toggle="modal"]');
//         if (button) {
//             const storyContainer = button.closest('.story-container');
//             if (storyContainer && !storyContainer.dataset.initialized) {
//                 initializeStory(storyContainer);
//                 storyContainer.dataset.initialized = 'true';
//             }
//         }
//     });

//     function initializeStory(storyContainer) {
//         let currentStoryIndex = 0;
//         let storyTimer;
//         const modal = storyContainer.querySelector('.story-modal');
//         const progressBarSegments = storyContainer.querySelectorAll('.progress-bar');
//         const stories = storyContainer.querySelectorAll('.story-content');
//         const leftArea = storyContainer.querySelector('.left-area');
//         const rightArea = storyContainer.querySelector('.right-area');

//         progressBarSegments.forEach(segment => {
//             Object.assign(segment.style, {
//                 width: '100%',
//                 marginRight: '5px',
//                 background: 'linear-gradient(to right, rgba(255, 255, 255, 1) 50%, rgba(255, 255, 255, 0.5) 50%)',
//                 backgroundSize: '200% 100%',
//                 backgroundPosition: 'right center'
//             });
//         });

//         stories.forEach((story, idx) => {
//             story.style.display = idx === currentStoryIndex ? 'block' : 'none';
//         });

//         leftArea.addEventListener('click', () => navigateStory(-1));
//         rightArea.addEventListener('click', () => navigateStory(1));

//         modal.addEventListener('shown.bs.modal', () => {
//             startStory(currentStoryIndex);
//         });

//         modal.addEventListener('hidden.bs.modal', () => {
//             clearTimeout(storyTimer);
//             resetProgressBars();
//             stories.forEach(story => {
//                 story.style.display = 'none';
//                 const video = story.querySelector('video');
//                 if (video) {
//                     video.pause();
//                     video.currentTime = 0;
//                 }
//             });
//             if (currentStoryIndex >= stories.length - 1) {
//                 currentStoryIndex = 0;
//                 stories[0].style.display = 'block';
//             }
//         });

//         function resetProgressBars() {
//             progressBarSegments.forEach(segment => {
//                 segment.style.transition = 'none';
//                 segment.style.backgroundPosition = 'right center';
//             });
//         }

//         function navigateStory(direction) {
//             let newIndex = currentStoryIndex + direction;
//             if (newIndex >= 0 && newIndex < stories.length) {
//                 // Pause the current video if it exists
//                 const currentVideo = stories[currentStoryIndex].querySelector('video');
//                 if (currentVideo) {
//                     currentVideo.pause();
//                 }

//                 clearTimeout(storyTimer);
//                 currentStoryIndex = newIndex;
//                 startStory(currentStoryIndex);
//             }
//         }

//         function animateProgressBar(index, duration) {
//             setTimeout(() => {
//                 progressBarSegments[index].style.transition = `background-position ${duration}ms linear`;
//                 progressBarSegments[index].style.backgroundPosition = 'left center';
//             }, 10);
//         }

//         function startStory(index) {
//             stories.forEach((story, idx) => {
//                 story.style.display = idx === index ? 'block' : 'none';
//                 if (idx === index) {
//                     const video = story.querySelector('video');
//                     if (video) {
//                         video.currentTime = 0;
//                         video.play().catch(error => {
//                             console.log("Error auto-playing video:", error);
//                             video.muted = true;
//                             video.play();
//                         });
//                     }
//                 }
//             });

//             const video = stories[index].querySelector('video');
//             const duration = video && video.duration ? video.duration * 1000 : defaultStoryDuration;

//             resetProgressBars();
//             animateProgressBar(index, duration);
//             startStoryTimer(index, duration);
//         }

//         function startStoryTimer(index, duration) {
//             clearTimeout(storyTimer);
//             storyTimer = setTimeout(() => {
//                 if (index + 1 < stories.length) {
//                     currentStoryIndex = index + 1;
//                     startStory(currentStoryIndex);
//                 }
//             }, duration);
//         }
//     }
// });

const handleStoryShowAndHideButton = (container) => {
    const defaultStoryDuration = 3000;

    container.addEventListener('click', function (event) {
        const button = event.target.closest('button[data-bs-toggle="modal"]');
        if (button) {
            const storyContainer = button.closest('.story-container');
            if (storyContainer && !storyContainer.dataset.initialized) {
                initializeStory(storyContainer);
                storyContainer.dataset.initialized = 'true';
            }
        }
    });

    function initializeStory(storyContainer) {
        let currentStoryIndex = 0;
        let storyTimer;
        const modal = storyContainer.querySelector('.story-modal');
        const progressBarSegments = storyContainer.querySelectorAll('.progress-bar');
        const stories = storyContainer.querySelectorAll('.story-content');
        const leftArea = storyContainer.querySelector('.left-area');
        const rightArea = storyContainer.querySelector('.right-area');

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

        leftArea.addEventListener('click', () => navigateStory(-1));
        rightArea.addEventListener('click', () => navigateStory(1));

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

        function resetProgressBars() {
            progressBarSegments.forEach(segment => {
                segment.style.transition = 'none';
                segment.style.backgroundPosition = 'right center';
            });
        }

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
                            video.muted = true;
                            video.play();
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
    }
}

export { handleStoryShowAndHideButton }
