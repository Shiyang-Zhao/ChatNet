document.addEventListener('DOMContentLoaded', function () {
    const myModalElement = document.querySelector('#myModal');
    const myModal = new bootstrap.Modal(myModalElement, {
        keyboard: false
    });
    const createChatButton = document.querySelector('#create-chat-button')
    const createChatButtonPopover = new bootstrap.Popover(createChatButton, {
        trigger: 'manual',
        html: true,
        content: 'You must select at least one participant',
        placement: 'right',
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('group_chat_create_form') === 'true') {
        myModal.show();
    }

    myModalElement.addEventListener('shown.bs.modal', function () {
        let url = new URL(window.location);
        url.searchParams.set('group_chat_create_form', 'true');
        window.history.pushState({}, '', url);
    });

    document.querySelector('#group-chat-create-form').addEventListener('submit', function (event) {
        const checkboxes = document.querySelectorAll('.participant-checkbox');
        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (!isChecked) {
            event.preventDefault();
            createChatButtonPopover.show();
            setTimeout(() => { createChatButtonPopover.hide(); }, 3000);
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


