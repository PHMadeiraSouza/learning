const likebutton = document.createElement('button')
likebutton.type = "button"
likebutton.className = "btn btn-primary"

function likepost(post_id){

    fetch('/likepost/' + post_id, {
        method: 'POST',
    })

    var like_quantity = parseInt(document.querySelector(`#quantity_like_${post_id}`).innerHTML);
    like_quantity += 1;
    document.querySelector(`#quantity_like_${post_id}`).innerHTML = like_quantity;

    var unlike_button = document.createElement('button')
    unlike_button.type = 'button'
    unlike_button.className = "btn btn-danger"
    unlike_button.innerHTML = 'unlike'

    unlike_button.addEventListener('click', () => unlikepost(post_id));
    document.querySelector(`#like_button_div_${post_id}`).innerHTML = ''
    document.querySelector(`#like_button_div_${post_id}`).append(unlike_button);

}

function unlikepost(post_id){

    fetch('/unlikepost/' + post_id, {
        method: 'POST',
    })

    var like_quantity = parseInt(document.querySelector(`#quantity_like_${post_id}`).innerHTML);
    like_quantity -= 1;
    document.querySelector(`#quantity_like_${post_id}`).innerHTML = like_quantity;

    var like_button = document.createElement('button')
    like_button.type = 'button'
    like_button.className = "btn btn-primary"
    like_button.innerHTML = 'like'

    like_button.addEventListener('click', () => likepost(post_id));
    document.querySelector(`#like_button_div_${post_id}`).innerHTML = ''
    document.querySelector(`#like_button_div_${post_id}`).append(like_button);

}

function editpost(post_id){
    document.querySelector(`#submit_button_div_${post_id}`).innerHTML = ''
    const post_content = document.querySelector(`#post_content${post_id}`).innerHTML
    document.querySelector(`#post_content_div${post_id}`).innerHTML=''

    var textarea = document.createElement('textarea')
    textarea.className = "form-control"
    textarea.innerHTML = post_content
    var submitbutton = document.createElement('input')
    submitbutton.type = 'button'
    submitbutton.className = "btn btn-primary"
    submitbutton.innerHTML = "save"

    submitbutton.addEventListener('click', function () {
        fetch('/editpost/' + post_id, {
            method: 'POST',
            body: JSON.stringify({
                content: textarea.value
            })
        })

        var post_content = document.createElement('p')
        post_content.className = "card-text"
        post_content.innerHTML = textarea.value

        document.querySelector(`#post_content_div${post_id}`).innerHTML = ''
        document.querySelector(`#post_content_div${post_id}`).append(post_content)
        document.querySelector(`#like_button_div_${post_id}`).style.display = 'block'
        document.querySelector(`#submit_button_div_${post_id}`).style.display = 'none'
        document.querySelector(`#submit_button_div_${post_id}`).innerHTML = ''
        document.querySelector(`#edited_div${post_id}`).innerHTML = ''
        document.querySelector(`#edited_div${post_id}`).innerHTML = `<h5><span class="badge bg-secondary" style="color:white; padding: 7px;">edited</span></h5>`



    })

    document.querySelector(`#post_content_div${post_id}`).append(textarea);
    document.querySelector(`#like_button_div_${post_id}`).style.display = 'none'
    document.querySelector(`#submit_button_div_${post_id}`).append(submitbutton)

}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#post_form').onsubmit = function () {
        fetch('/createpost', {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector('#post_content').value
            })
        })
    };

})