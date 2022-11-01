const key = document.getElementById("keyword")
const submit = document.getElementById("keywordsubmit")

document.addEventListener("DOMContentLoaded", () => {
    console.log("dddd")
    let keyword = localStorage["Keyword"]
    if (keyword == null) {
        keyword = "";
    }
    
    submit.onclick = () => {
        console.log("clicked")
        localStorage.setItem("Keyword", key.value)
    }
    
})

