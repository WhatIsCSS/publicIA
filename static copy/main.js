//FOR TROUBLESHOOTING
console.log("JavaScript file loaded");

//Navbar Function
function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:none;");
    navigation.classList.remove("hide");
}

function showIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:block;");
    navigation.classList.add("hide");
}


//LOGGED IN AND SIGNED UP
function showLogin() {
  console.log('Show Login');
  document.getElementById('login-form').classList.remove('hidden');
  document.getElementById('signup-form').classList.add('hidden');
  document.getElementById('login-btn').classList.add('active');
  document.getElementById('signup-btn').classList.remove('active');
}

function showSignup() {
  console.log('Show Signup');
  document.getElementById('signup-form').classList.remove('hidden');
  document.getElementById('login-form').classList.add('hidden');
  document.getElementById('signup-btn').classList.add('active');
  document.getElementById('login-btn').classList.remove('active');
}


//COMMENTING FUNCION
function showCommentModal() {
  document.getElementById('comment-modal').style.display = 'block';
}

function closeCommentModal() {
  document.getElementById('comment-modal').style.display = 'none';
}

//CREATING THE POSTS

document.getElementById('comment-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission
  
    // Get form values
    const condition = document.getElementById('surf-condition').value;
    const title = document.getElementById('title').value;
    const location = document.getElementById('location').value;
    const description = document.getElementById('description').value;
    const username = "{{ session['username'] }}";  // Get the username from the session
    const date = new Date().toLocaleDateString();  // Get current date
  
    // Determine the icon class based on the selected condition
    let iconClass = '';
    switch (condition) {
        case 'very_big_waves':
            iconClass = 'giant-waves-icon';
            break;
        case 'great_conditions_for_surfing':
            iconClass = 'surfing-icon';
            break;
        case 'great_conditions_for_kite_and_windsurfing':
            iconClass = 'kitesurfing-icon';
            break;
        case 'bad_overall_conditions':
            iconClass = 'bad-conditions-icon';
            break;
        case 'too_windy':
            iconClass = 'too-windy-icon';
            break;
        case 'amazing_overall_conditions':
            iconClass = 'amazing-conditions-icon';
            break;
    }
  
    // Create a new post row
    const newPost = `
        <div class="table-row">
            <div class="status">
                <i class="${iconClass}">
                    <span class="material-symbols-outlined"></span>
                </i>
            </div>
            <div class="subjects">
                <a href="#">${title}</a>
                <br>
                <span>${description}<b><a href="#"></a></b>.</span>
            </div>
            <div class="replies">
                ${location}
            </div>
            <div class="last-reply">
                Posted on ${date}
                <br>
                By <b><a href="#">${username}</a></b>
            </div>
        </div>
    `;
    
    // Prepend the new post to the posts container (new posts appear on top)
    document.getElementById('posts-container').insertAdjacentHTML('afterbegin', newPost);
  
    // Clear the form
    document.getElementById('comment-form').reset();
  
    // Now, we submit the form so that Flask can handle the redirect
    e.target.submit();
});
