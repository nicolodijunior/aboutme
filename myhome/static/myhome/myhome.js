document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#like_post_btn') != null) {
        const like_post_btn = document.querySelector('#like_post_btn');
        post_id = like_post_btn.dataset.postid;
        like_post_btn.addEventListener('click', () => like_post(post_id));
    }
    
});

function like_post(post_id){
    fetch(`/myhome/blog/all/like_post/${post_id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        return Promise.resolve();
    })
    .then(() => update_post(post_id))
    .catch(error => console.log(error));
}

function update_post(post_id){
    fetch(`/myhome/blog/all/update_post/${post_id}`)
    .then(response => response.json())
    .then(data => {
        document.querySelector("#post_likes").textContent = data.likes_qty + " likes";
        if(data.liked) document.querySelector("#like_post_btn").innerHTML = "<ion-icon name='heart-dislike-outline'></ion-icon>";
        else document.querySelector("#like_post_btn").innerHTML = "<ion-icon name='heart-outline'></ion-icon>";
    })
    .catch(error => console.log(error));

}


