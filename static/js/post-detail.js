Array.from(document.getElementsByClassName('comment-create-btn')).forEach(btn => {
  btn.addEventListener('click', e => {
    const targetBtn = e.target;
    const postId = targetBtn.closest('.comment-area').dataset.postId;

    const contentTextarea = targetBtn.closest('.comment-create-area').getElementsByClassName('comment-content-textarea')[0]

    const content = contentTextarea.value

    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

    const data = JSON.stringify({
      content: content,
    })

    fetch(`/blog/post/${postId}/comment/create`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: data
    })
        .then(response => {
          return response.json();
        })
        .then(response => {
          const status = response.status;

          if (status === 'success') {
            contentTextarea.value = '';
            toastr["success"]("Add comment");
          } else if (status === 'post does not exist') {
            contentTextarea.value = '';
            toastr["error"]("Post does not exist");
          } else if (status === 'content is empty') {
            toastr["error"]("Content is required");
          }
        })
  })
})

toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-bottom-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "3000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}