Array.from(document.getElementsByClassName('post-delete-btn')).forEach(btn => {
  btn.addEventListener('click', e => {
    const targetBtn = e.target;
    const postId = targetBtn.closest('.post-area').dataset.postId;

    document.getElementById('postDeleteForm').action = `/blog/post/${postId}/delete`;
  })
})

Array.from(document.getElementsByClassName('bookmark-create-btn')).forEach(btn => {
  btn.addEventListener('click', e => {
    const targetBtn = e.target;
    const postId = targetBtn.closest('.post-area').dataset.postId;

    fetch(`/blog/post/${postId}/bookmark/create`)
        .then(response => {
          targetBtn.classList.add('d-none');
          targetBtn.closest('.post-area').getElementsByClassName('bookmark-delete-btn')[0].classList.remove('d-none');
        })
  })
})

Array.from(document.getElementsByClassName('bookmark-delete-btn')).forEach(btn => {
  btn.addEventListener('click', e => {
    const targetBtn = e.target;
    const postId = targetBtn.closest('.post-area').dataset.postId;

    fetch(`/blog/post/${postId}/bookmark/delete`)
        .then(response => {
          targetBtn.classList.add('d-none');
          targetBtn.closest('.post-area').getElementsByClassName('bookmark-create-btn')[0].classList.remove('d-none');
        })
  })
})