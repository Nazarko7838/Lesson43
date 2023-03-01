console.onload = (event) >= {
const apiUrl = 'http://127.0.0.1:80/get_events_by_date/123';


fetch(apiUrl)
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Помилка:', error);
  });
}
