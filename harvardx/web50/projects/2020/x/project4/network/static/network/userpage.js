function sign_in() {
    document.querySelector('#alert_div').innerHTML = '';

    const alert = document.createElement('div')
    alert.className = "alert alert-danger"
    alert.role = "alert"
    alert.style.display = "flex"
    alert.innerHTML = `you need to be signed in — <a class="alert-link" href="/login"> Log In</a>`

    document.querySelector('#alert_div').append(alert);
}

function follow_user(user_id) {

    fetch('/followuser/' + user_id, {
        method: 'POST',
    })

    let followers_number = parseInt(document.querySelector('#followers_number').innerHTML);
    followers_number += 1;
    document.querySelector('#followers_number').innerHTML = followers_number;


    document.querySelector('#follow_btn_div').innerHTML = ''

    const unfollow_btn = document.createElement('a')
    unfollow_btn.className = "btn btn-dark"
    unfollow_btn.innerHTML = `unfollow`
    unfollow_btn.style.color = 'white'

    unfollow_btn.addEventListener('click', () => unfollow_user(user_id));
    document.querySelector('#follow_btn_div').append(unfollow_btn);
}

function unfollow_user(user_id) {

    fetch('/unfollowuser/' + user_id, {
        method: 'POST',
    })

    let followers_number = parseInt(document.querySelector('#followers_number').innerHTML);
    followers_number -= 1;
    document.querySelector('#followers_number').innerHTML = followers_number;

    document.querySelector('#follow_btn_div').innerHTML = ''

    const follow_btn = document.createElement('a')
    follow_btn.className = "btn btn-primary"
    follow_btn.innerHTML = `follow`
    follow_btn.style.color = 'white'

    follow_btn.addEventListener('click', () => follow_user(user_id));
    document.querySelector('#follow_btn_div').append(follow_btn);
}

document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#followers').addEventListener('click', followers)
    document.querySelector('#following').addEventListener('click', following)
    document.querySelector('#posts_made').addEventListener('click', posts)

    posts()

    function posts() {
        document.querySelector('#posts_feed').style.display = 'block';
        document.querySelector('#followers_profiles').style.display = 'none';
        document.querySelector('#following_profiles').style.display = 'none';
        document.querySelector('#posts_made_div').style.color = 'crimson';
        document.querySelector('#followers_top_div').style.color = 'black';
        document.querySelector('#following_top_div').style.color = 'black';
    }

    function followers() {
        document.querySelector('#posts_feed').style.display = 'none';
        document.querySelector('#followers_profiles').style.display = 'block';
        document.querySelector('#following_profiles').style.display = 'none';
        document.querySelector('#posts_made_div').style.color = 'black';
        document.querySelector('#followers_top_div').style.color = 'crimson';
        document.querySelector('#following_top_div').style.color = 'black';

    }

    function following() {
        document.querySelector('#posts_feed').style.display = 'none';
        document.querySelector('#followers_profiles').style.display = 'none';
        document.querySelector('#following_profiles').style.display = 'block';
        document.querySelector('#posts_made_div').style.color = 'black';
        document.querySelector('#followers_top_div').style.color = 'black';
        document.querySelector('#following_top_div').style.color = 'crimson';

    }
})