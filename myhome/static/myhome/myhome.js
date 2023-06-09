document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#like_post_btn') != null) {
        const like_post_btn = document.querySelector('#like_post_btn');
        post_id = like_post_btn.dataset.postid;
        like_post_btn.addEventListener('click', () => like_post(post_id));
    }
    
});

document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#register') != null){
        const usernameField = document.querySelector('#id_username');
        const emailField = document.querySelector('#id_email');
        const passwordField = document.querySelector('#id_password');
        const confirmationField = document.querySelector('#id_confirmation');
        const submitBtn = document.querySelector('#register');
        const msg = document.querySelector('#field-msg');
        
        submitBtn.addEventListener('click', function(event) {
            let messages =[]
          if (usernameField.value.length==0){ 
            messages.push('Username is required.');
          }
          if(passwordField.value != confirmationField.value){
            messages.push('Passwords do not match.');
          }
          if(passwordField.value.length < 8){
            messages.push('Password must be at least 8 characters long.');
          }
          if(emailField.value.length<5){
            messages.push('Email is required.');
          }
          if(messages.length > 0){
            event.preventDefault();
            msg.innerHTML = messages.join('<br>');
          }
        });     
        
        
    }

    function showErrorMessage(msg){
        document.querySelector('#field-msg').innerHTML = msg;
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
/* 
  document.getElementById('register-form').addEventListener('submit', function(event) {
    var usernameField = document.getElementById('id_username');
    var emailField = document.getElementById('id_email');
    var passwordField = document.getElementById('id_password');
    var confirmationField = document.getElementById('id_confirmation');
    
    var username = usernameField.value.trim();
    var email = emailField.value.trim();
    var password = passwordField.value;
    var confirmation = confirmationField.value;
    
    var errors = [];
    
    if (username === '') {
      errors.push('Username is required.');
    }
    
    if (email === '') {
      errors.push('Email is required.');
    } else if (!isValidEmail(email)) {
      errors.push('Invalid email address.');
    }
    
    if (password === '') {
      errors.push('Password is required.');
    } else if (password.length < 8) {
      errors.push('Password must be at least 8 characters long.');
    }
    
    if (confirmation === '') {
      errors.push('Confirmation is required.');
    } else if (password !== confirmation) {
      errors.push('Passwords do not match.');
    }
    
    if (errors.length > 0) {
      event.preventDefault(); // Prevent form submission
      
      // Display error messages
      var errorContainer = document.getElementById('error-container');
      errorContainer.innerHTML = '';
      errors.forEach(function(error) {
        var errorElement = document.createElement('p');
        errorElement.textContent = error;
        errorContainer.appendChild(errorElement);
      });
    }
  });
  
  function isValidEmail(email) {
    // Perform email validation logic here (e.g., using regular expressions)
    return true; // Replace with actual validation code
  }
 */