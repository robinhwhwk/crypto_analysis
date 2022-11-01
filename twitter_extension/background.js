let serverhost = "http://127.0.0.1:8000" 

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  var url =
    serverhost +
    "/twitter/get_twitter_sentiment/$?query=" +
    encodeURIComponent(request.query);

  console.log(url);

  //var url = "http://127.0.0.1:8000/twitter/get_twitter_sentiment/?query=lebron"
  fetch(url)
    .then((response) => response.json())
    .then((response) => sendResponse({ farewell: response }))
    .catch((error) => console.log(error));

  return true; // Will respond asynchronously.
});
