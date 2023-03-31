window.onload = (event) => {


    const routes = [
        {path: '/', handler:homeHandler},
        {path: '/index.html', handler: homeHandler},
        {path: '/login', handler: loginHandler},
        {path: '/signup', handler: signupHandler}
    ]
    handleUrlChange()
    function handleUrlChange () {
        const path = window.location.pathname;
        const urlPath = routes.find(route => route.path === path)
        console.log(urlPath);
        if (urlPath){

            urlPath.handler();
        }else {
            homeHandler();
        }
    }
function homeHandler () {
        console.log("home works");
        const eventForm = document.getElementById("event-form");
        console.log(eventForm);
        const urlAddEvent = 'http://127.0.0.1:80/create_event';
        const date = new Date().toISOString();

        getEventsByDate(date);

        eventForm.addEventListener("submit", (event) => {
            event.preventDefault();

            sendRequestToServer(eventForm, urlAddEvent);
    })}

function loginHandler () {
        const loginForm = document.getElementById("login-form");
        const urlLogin = 'http://127.0.0.1:5000/login';

        loginForm.addEventListener("submit", (event) => {
            event.preventDefault();

            sendRequestToServer(loginForm, urlLogin)
            .then(data => {
                localStorage.setItem("token", data.token);
                console.log(localStorage.getItem("token"));
            });
    })
    }

    function signupHandler () {
        const signupForm = document.getElementById("signup-form");
        const urlSignup = 'http://127.0.0.1:5000/signup';

        signupForm.addEventListener("submit", (event) => {
            event.preventDefault();

            sendRequestToServer(eventForm, urlAddEvent);
    })
    }
    const urlLogin = 'http://127.0.0.1:80/login';
    const urlSignup = 'http://127.0.0.1:80/signup';


function getEventsByDate(date){
    const apiUrlGet = `http://127.0.0.1:80/get_events_by_date/${date}`;

    fetch(apiUrlGet, {
        method: "GET",})
      .then(response => response.json())
      .then(data => {
        console.log(data); // вивести дані в консоль
      })
      .catch(error => {
        console.error('Помилка:', error);
      });
}


    const signupForm = document.getElementById("signup-form");
    const loginForm = document.getElementById("login-form");



    function sendRequestToServer (form, url) {

        const formData = new FormData(form);
        const data = {};

        for (const[key, value] of formData.entries()) {
            data[key] = value;
        }

        fetch(url, {
            method: "POST",
            headers: {"Content-type": "application/json"},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .catch(error => console.error('Помилка:', error));
    }

}

