const key = document.getElementById("keyword");
const submit = document.getElementById("keywordsubmit");

let serverhost = "http://127.0.0.1:8000" 
console.log("hello")

submit.onclick = () => {
    var search_topic = $("#keyword").val();
    console.log(search_topic);

    let url =
    serverhost +
    "/twitter/get_twitter_sentiment/$?query=" +
    encodeURIComponent(search_topic);

    if (search_topic) {
        fetch(url)
        .then((response) => response.json())
        .then((response) => {
            let placeholder = document.querySelector("#data-output");
            let out = "";
            out += `
                <tr>
                    <td>${search_topic}</td>
                    <td>${response.rating}</td>
                    <td>${response.distribution}</td>
                <tr>
            `
        })
        .catch((error) => console.log(error));
    
      return true; // Will respond asynchronously.
    }

    $("#keyword").val("");
  };