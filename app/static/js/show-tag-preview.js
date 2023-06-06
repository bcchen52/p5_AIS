var showSampleTag = () => {
    var e = document.getElementById("tag-color");
    var selectedColor = e.options[e.selectedIndex].value;
    console.log(selectedColor);

    var tag = document.getElementById("tag");
    // var tagText = document.getElementById("tag-");
    var newTagName = document.getElementById("tag-name");

    if (selectedColor != "") {
        tag.className = "tag " + selectedColor +"-tag";
    } else {
        tag.className = "tag";
    }

    tag.innerHTML = newTagName.value;
};

let results = document.getElementById("tag-color");
results.addEventListener("change", showSampleTag);

let tagName = document.getElementById("tag-name");
tagName.addEventListener("input", showSampleTag);