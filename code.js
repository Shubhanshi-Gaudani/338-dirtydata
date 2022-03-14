const showPostDetail = ev => {
    const html = `
            <div class ="modal-bg">
                <div class ="modal">
                    The data is getting cleaned
                </div>    
            </div>`;
    document.querySelector('#modal-container').innerHTML = html;
    setTimeout(function() { CloseModal(); }, 5000);
};

const CloseModal = ev => {
    const html = '';
    document.querySelector('#modal-container').innerHTML = html;
};