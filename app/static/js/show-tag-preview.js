var showSampleTag = () => {
    var e = document.getElementById("tag-color");
    var selectedColor = e.options[e.selectedIndex].value;
    console.log(selectedColor);

    var tag = document.getElementById("sample-tag");
    var tagText = document.getElementById("tag-text");
    var newTagName = document.getElementById("tag-name");

    if (selectedColor != "") {
        tag.className = "tag-span " + selectedColor +"-tag";
    } else {
        tag.className = "tag-span";
    }

    tagText.innerHTML = newTagName.value;
};

let results = document.getElementById("tag-color");
results.addEventListener("change", showSampleTag);

let tagName = document.getElementById("tag-name");
tagName.addEventListener("input", showSampleTag);