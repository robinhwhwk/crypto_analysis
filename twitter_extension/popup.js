const key = document.getElementById("keyword");
const submit = document.getElementById("keywordsubmit");

function ping() {
  chrome.runtime.sendMessage("ping", (response) => {
    if (chrome.runtime.lastError) {
      setTimeout(ping, 1000);
    } else {
      // Do whatever you want, background script is ready now
      console.log("in ping function");

      submit.onclick = () => {
        var search_topic = $("#keyword").val();
        console.log(search_topic);

        if (search_topic) {
          chrome.runtime.sendMessage(
            chrome.runtime.id,
            { query: search_topic },
            (response) => {
              result = response.farewell;
              alert("rating: " + result.rating.toString() + "/100");

              var notifOptions = {
                type: "basic",
                iconUrl: "/images/review_icon64.png",
                title: "Rating for your query",
                message: "rating: " + result.rating.toString() + "/100"
              };

              chrome.notifications.create("WikiNotif", notifOptions);
            }
          );
        }

        $("#keyword").val("");
      };
    }
  });
}

ping();
