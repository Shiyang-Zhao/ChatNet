document.addEventListener('DOMContentLoaded', function () {
    const modalButton = document.querySelector('#openModalButton');
    const myModalElement = document.querySelector('#myModal');
    const myModal = new bootstrap.Modal(myModalElement, {
        keyboard: false
    });
    const createChatButton = document.querySelector('#create-chat-button')
    const createChatButtonPopover = new bootstrap.Popover(createChatButton, {
        trigger: 'manual',
        html: true
    });

    // Event listener for opening the modal
    modalButton.addEventListener('click', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('group_chat_create_form', 'open');
        window.history.pushState({}, '', window.location.pathname + '?' + urlParams.toString());
        myModal.show();
    });

    // Check if the modal should be opened based on URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('group_chat_create_form') === 'open') {
        myModal.show();
    }

    // Listen for the hidden event on the modal
    myModalElement.addEventListener('hidden.bs.modal', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.delete('group_chat_create_form'); // Remove the query parameter
        let newUrl = window.location.pathname;
        if (urlParams.toString()) {
            newUrl += '?' + urlParams.toString();
        }
        window.history.pushState({}, '', newUrl);
    });

    document.querySelector('#group-chat-create-form').addEventListener('submit', function (event) {
        const checkboxes = document.querySelectorAll('.participant-checkbox');
        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (!isChecked) {
            event.preventDefault();
            createChatButtonPopover.show();
        }
    });

    document.querySelectorAll('.participant-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (document.querySelector('.participant-checkbox:checked')) {
                createChatButtonPopover.hide();
            }
        });
    });
});


